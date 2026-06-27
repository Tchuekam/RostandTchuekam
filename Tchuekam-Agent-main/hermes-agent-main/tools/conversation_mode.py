"""
Conversation Mode — Ultra-fast voice conversation engine for Tchuekam.

Architecture:
    Mic (VAD) → STT (existing provider) → LLM (existing provider) → TTS (Edge TTS) → Speaker

No external API key dependencies beyond what Tchuekam already has configured.
Supports English, French, and Cameroonian local languages (Fulfulde, Ewondo, Douala).
Response cache avoids redundant lookups.

This module is ONLY invoked via `/voice live` and has zero effect on the rest
of the agent pipeline.
"""

import asyncio
import hashlib
import io
import logging
import os
import re
import sys
import tempfile
import threading
import time
import wave
from collections import OrderedDict
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# ── Audio constants ──────────────────────────────────────────────────────────
SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = "int16"
CHUNK_FRAMES = 1024
# VAD: energy threshold for voice activity detection
VAD_ENERGY_THRESHOLD = 500
VAD_SILENCE_CHUNKS = 25  # ~1.6s of silence = end of utterance
VAD_MIN_SPEECH_CHUNKS = 5  # minimum speech to avoid micro-triggers

# ── Multilingual TTS voice map ───────────────────────────────────────────────
LANG_VOICE_MAP = {
    "en": "en-US-GuyNeural",
    "fr": "fr-FR-HenriNeural",
    "ff": "fr-FR-HenriNeural",    # Fulfulde → French voice + phonemes
    "ewo": "fr-FR-HenriNeural",   # Ewondo → French voice + phonemes
    "dua": "fr-FR-HenriNeural",   # Douala → French voice + phonemes
    "bbj": "fr-FR-HenriNeural",   # Ghomala → French voice + phonemes
    "auto": "en-US-GuyNeural",
}

# ── Response cache (LRU) ────────────────────────────────────────────────────
_CACHE_MAX = 200


class _ResponseCache:
    """Thread-safe LRU cache for LLM responses."""

    def __init__(self, max_size: int = _CACHE_MAX):
        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self._max = max_size
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0

    @staticmethod
    def _key(text: str) -> str:
        normalized = re.sub(r"\s+", " ", text.strip().lower())
        return hashlib.md5(normalized.encode("utf-8")).hexdigest()

    def get(self, query: str) -> Optional[Dict[str, Any]]:
        k = self._key(query)
        with self._lock:
            if k in self._cache:
                self._cache.move_to_end(k)
                self._hits += 1
                return self._cache[k]
            self._misses += 1
            return None

    def put(self, query: str, response: str, lang: str = "auto"):
        k = self._key(query)
        with self._lock:
            if k in self._cache:
                self._cache.move_to_end(k)
            self._cache[k] = {"response": response, "lang": lang}
            while len(self._cache) > self._max:
                self._cache.popitem(last=False)


_response_cache = _ResponseCache()


# ── Language detection ───────────────────────────────────────────────────────

def _detect_response_language(text: str) -> str:
    """Detect whether a response is English, French, or local."""
    french_markers = {"je", "tu", "il", "elle", "nous", "vous", "les", "des",
                      "une", "est", "sont", "avec", "dans", "pour", "pas",
                      "oui", "non", "mais", "que", "qui", "cette", "merci",
                      "bonjour", "comment", "bien", "aussi"}
    words = set(re.sub(r"[^\w\s]", "", text.lower()).split())
    french_count = len(words & french_markers)
    if french_count >= 2:
        return "fr"
    return "en"


def _detect_input_language(text: str) -> str:
    """Detect user input language including Cameroonian local languages."""
    try:
        from tools.local_languages_helper import detect_language
        detected = detect_language(text)
        if detected != "auto":
            return detected
    except Exception:
        pass
    return _detect_response_language(text)


# ── Conversation system prompt ───────────────────────────────────────────────

CONVERSATION_SYSTEM_PROMPT = """You are TCHUEKAM in voice conversation mode. Rules:
- Respond in 1-3 SHORT sentences maximum. Be natural and conversational.
- Match the user's language: if they speak French, respond in French. If English, respond in English.
- NO markdown, NO code blocks, NO bullet points, NO headers, NO URLs.
- NO "As an AI" disclaimers. Just answer directly like a knowledgeable friend.
- If the user speaks a Cameroonian language (Fulfulde, Ewondo, Douala), respond in French with cultural awareness.
- Be concise. Every word counts. No filler."""


# ── Core engine ──────────────────────────────────────────────────────────────

class ConversationEngine:
    """Self-contained voice conversation loop.

    Mic → VAD → WAV → STT → (cache check) → LLM → TTS → Speaker
    """

    def __init__(self):
        self._running = False
        self._conversation_history: list[Dict[str, str]] = []

    def _record_utterance(self) -> Optional[str]:
        """Record a single utterance using VAD. Returns path to temp WAV or None."""
        import sounddevice as sd
        import numpy as np

        wav_path = os.path.join(
            tempfile.gettempdir(), "tchuekam_voice",
            f"utterance_{int(time.time() * 1000)}.wav"
        )
        os.makedirs(os.path.dirname(wav_path), exist_ok=True)

        frames: list[bytes] = []
        silence_count = 0
        speech_count = 0
        recording = False

        stream = sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype=DTYPE,
            blocksize=CHUNK_FRAMES,
        )
        stream.start()
        try:
            while self._running:
                data, overflowed = stream.read(CHUNK_FRAMES)
                audio_data = np.frombuffer(bytes(data), dtype=np.int16)
                energy = np.abs(audio_data).mean()

                if energy > VAD_ENERGY_THRESHOLD:
                    recording = True
                    speech_count += 1
                    silence_count = 0
                    frames.append(bytes(data))
                elif recording:
                    silence_count += 1
                    frames.append(bytes(data))
                    if silence_count >= VAD_SILENCE_CHUNKS:
                        break

            if speech_count < VAD_MIN_SPEECH_CHUNKS:
                return None

            # Write WAV
            with wave.open(wav_path, "wb") as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(b"".join(frames))

            return wav_path

        finally:
            stream.stop()
            stream.close()

    def _transcribe(self, wav_path: str) -> Optional[str]:
        """Transcribe a WAV file using existing STT infrastructure."""
        try:
            from tools.voice_mode import transcribe_recording
            result = transcribe_recording(wav_path)
            if result.get("success") and result.get("transcript", "").strip():
                return result["transcript"].strip()
        except Exception as e:
            logger.warning("STT failed: %s", e)
        return None

    def _get_llm_response(self, user_text: str) -> str:
        """Get a response from the agent's existing LLM provider."""
        # Check cache first
        cached = _response_cache.get(user_text)
        if cached:
            logger.info("[cache hit] Returning cached response")
            return cached["response"]

        # Build conversation messages
        messages = [{"role": "system", "content": CONVERSATION_SYSTEM_PROMPT}]
        # Keep last 10 exchanges for context
        messages.extend(self._conversation_history[-20:])
        messages.append({"role": "user", "content": user_text})

        try:
            # Use existing provider infrastructure
            api_key, base_url = self._resolve_provider_creds()

            from hermes_cli.config import load_config
            config = load_config()
            model_cfg = config.get("model", {})
            model_name = model_cfg.get("model") or "gemini-2.5-flash"

            from openai import OpenAI

            client = OpenAI(api_key=api_key, base_url=base_url)
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    max_tokens=150,  # Keep responses short
                    temperature=0.7,
                )
                reply = response.choices[0].message.content or ""
            finally:
                close = getattr(client, "close", None)
                if callable(close):
                    close()

        except Exception as e:
            logger.warning("LLM call failed: %s", e)
            reply = "I couldn't process that. Could you try again?"

        # Strip any markdown that snuck through
        reply = re.sub(r"```[\s\S]*?```", "", reply)
        reply = re.sub(r"\*\*(.+?)\*\*", r"\1", reply)
        reply = re.sub(r"\*(.+?)\*", r"\1", reply)
        reply = re.sub(r"`(.+?)`", r"\1", reply)
        reply = re.sub(r"^#+\s*", "", reply, flags=re.MULTILINE)
        reply = re.sub(r"^\s*[-*]\s+", "", reply, flags=re.MULTILINE)
        reply = reply.strip()

        # Update history
        self._conversation_history.append({"role": "user", "content": user_text})
        self._conversation_history.append({"role": "assistant", "content": reply})

        # Cache the response
        lang = _detect_response_language(reply)
        _response_cache.put(user_text, reply, lang)

        return reply

    def _resolve_provider_creds(self) -> tuple:
        """Resolve API key and base URL for the active provider."""
        from hermes_cli.auth import resolve_provider, read_credential_pool, get_provider_auth_state

        provider = resolve_provider()

        # Try credential pool first
        pool = read_credential_pool(provider)
        if isinstance(pool, list) and pool:
            cred = pool[0]
            api_key = cred.get("access_token") or cred.get("api_key", "")
            base_url = cred.get("base_url", "")
            if api_key and base_url:
                # Append /openai/ for Gemini native base URLs
                if "generativelanguage.googleapis.com" in base_url and not base_url.rstrip("/").endswith("/openai"):
                    base_url = base_url.rstrip("/") + "/openai/"
                return api_key, base_url
            if api_key:
                return api_key, self._default_base_url(provider)

        # Fallback to provider state
        state = get_provider_auth_state(provider)
        if state:
            token = state.get("access_token") or state.get("api_key", "")
            if token:
                return token, self._default_base_url(provider)

        # Env var fallback
        for env_key in ("GOOGLE_API_KEY", "GEMINI_API_KEY", "OPENROUTER_API_KEY",
                        "OPENAI_API_KEY"):
            val = os.environ.get(env_key)
            if val:
                if "GOOGLE" in env_key or "GEMINI" in env_key:
                    return val, "https://generativelanguage.googleapis.com/v1beta/openai/"
                if "OPENROUTER" in env_key:
                    return val, "https://openrouter.ai/api/v1"
                return val, "https://api.openai.com/v1"

        raise RuntimeError("No API credentials found for conversation mode")

    @staticmethod
    def _default_base_url(provider: str) -> str:
        """Return the default base URL for a provider."""
        urls = {
            "gemini": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "openrouter": "https://openrouter.ai/api/v1",
            "anthropic": "https://api.anthropic.com/v1",
            "openai": "https://api.openai.com/v1",
        }
        return urls.get(provider, "https://openrouter.ai/api/v1")

    async def _speak_response(self, text: str, lang: str = "auto"):
        """Convert text to speech and play it using Edge TTS (free, no API key)."""
        try:
            from tools.lazy_deps import ensure
            ensure("tts.edge", prompt=False)
        except Exception:
            pass

        import edge_tts

        # Select voice based on detected language
        voice = LANG_VOICE_MAP.get(lang, LANG_VOICE_MAP["auto"])

        # For Cameroonian languages, apply phonetic preprocessing
        tts_text = text
        if lang in ("ff", "ewo", "dua", "bbj"):
            try:
                from tools.local_languages_helper import convert_to_phonemes
                tts_text = convert_to_phonemes(text, lang)
            except Exception:
                pass

        # Generate audio and play directly
        tmp_path = os.path.join(
            tempfile.gettempdir(), "tchuekam_voice",
            f"response_{int(time.time() * 1000)}.mp3"
        )
        os.makedirs(os.path.dirname(tmp_path), exist_ok=True)

        communicate = edge_tts.Communicate(tts_text, voice=voice, rate="+10%")
        await communicate.save(tmp_path)

        # Play audio
        try:
            from tools.voice_mode import play_audio_file
            play_audio_file(tmp_path)
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    def run(self):
        """Main conversation loop. Blocks until Ctrl+C."""
        self._running = True

        # Print banner
        print("\n" + "=" * 50, file=sys.stderr)
        print("  TCHUEKAM Voice Conversation Mode", file=sys.stderr)
        print("  Speak naturally | Press Ctrl+C to exit", file=sys.stderr)
        print("  Languages: English | French | Fulfulde | Ewondo | Douala", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
        print("  Listening...\n", file=sys.stderr)

        loop = asyncio.new_event_loop()

        try:
            while self._running:
                # 1. Record utterance with VAD
                wav_path = self._record_utterance()
                if not wav_path:
                    continue

                t0 = time.monotonic()

                # 2. Transcribe
                print("  Processing...", end="", file=sys.stderr, flush=True)
                user_text = self._transcribe(wav_path)

                # Clean up recording
                try:
                    os.unlink(wav_path)
                except OSError:
                    pass

                if not user_text:
                    print(" (no speech detected)", file=sys.stderr)
                    continue

                # 3. Detect language
                input_lang = _detect_input_language(user_text)
                print(f"\r  You: {user_text}", file=sys.stderr)

                # 4. Get LLM response
                reply = self._get_llm_response(user_text)
                response_lang = _detect_response_language(reply)

                # Use input language for local languages
                tts_lang = input_lang if input_lang in ("ff", "ewo", "dua", "bbj") else response_lang

                elapsed = (time.monotonic() - t0) * 1000
                print(f"  Tchuekam ({elapsed:.0f}ms): {reply}", file=sys.stderr)

                # 5. Speak response
                loop.run_until_complete(self._speak_response(reply, tts_lang))

                print("  Listening...\n", file=sys.stderr)

        except KeyboardInterrupt:
            pass
        finally:
            self._running = False
            loop.close()
            print("\n  Voice conversation ended.", file=sys.stderr)


# ── Public entry point ───────────────────────────────────────────────────────

def start_conversation_mode():
    """Start the conversation mode. Blocks until interrupted."""
    engine = ConversationEngine()
    engine.run()

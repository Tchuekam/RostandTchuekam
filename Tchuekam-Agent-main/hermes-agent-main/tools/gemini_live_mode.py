"""
Gemini Live Mode -- Real-time multimodal streaming via WebSockets.
"""

import os
import sys
import asyncio
import traceback
import logging

from tools.lazy_deps import ensure

logger = logging.getLogger(__name__)

FORMAT = "int16"
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024

# The Gemini 2.0 Flash Experimental model supports the BidiGenerateContent Live API
MODEL = "gemini-2.0-flash-exp" 

class GeminiLiveAudioLoop:
    def __init__(self):
        ensure("tts.gemini_live", prompt=False)
        self.audio_in_queue = None
        self.out_queue = None
        self.session = None

    async def send_realtime(self):
        while True:
            if self.out_queue is not None:
                msg = await self.out_queue.get()
                if self.session is not None:
                    await self.session.send(input=msg)

    async def listen_audio(self):
        """Read from the microphone and send to the output queue."""
        import sounddevice as sd
        stream = sd.RawInputStream(
            samplerate=SEND_SAMPLE_RATE,
            channels=CHANNELS,
            dtype=FORMAT,
            blocksize=CHUNK_SIZE,
        )
        stream.start()
        try:
            while True:
                data, overflowed = await asyncio.to_thread(stream.read, CHUNK_SIZE)
                if self.out_queue is not None:
                    await self.out_queue.put({"data": bytes(data), "mime_type": "audio/pcm"})
        finally:
            stream.stop()
            stream.close()

    async def receive_audio(self):
        """Background task to read from the websocket and write pcm chunks to the playback queue."""
        while True:
            if self.session is not None:
                turn = self.session.receive()
                async for response in turn:
                    if data := response.data:
                        self.audio_in_queue.put_nowait(data)
                        continue
                    if text := response.text:
                        print(text, end="")
                        sys.stdout.flush()

                # If you interrupt the model, it sends a turn_complete.
                # For interruptions to work, we need to stop playback.
                # So empty out the audio queue because it may have loaded
                # much more audio than has played yet.
                while not self.audio_in_queue.empty():
                    self.audio_in_queue.get_nowait()

    async def play_audio(self):
        """Play audio from the playback queue."""
        import sounddevice as sd
        stream = sd.RawOutputStream(
            samplerate=RECEIVE_SAMPLE_RATE,
            channels=CHANNELS,
            dtype=FORMAT,
        )
        stream.start()
        try:
            while True:
                if self.audio_in_queue is not None:
                    bytestream = await self.audio_in_queue.get()
                    await asyncio.to_thread(stream.write, bytestream)
        finally:
            stream.stop()
            stream.close()

    async def run(self):
        from google import genai
        from google.genai import types
        
        config_kwargs = {"response_modalities": ["AUDIO"]}
        if hasattr(self, "system_instruction") and self.system_instruction:
            config_kwargs["system_instruction"] = {"parts": [{"text": self.system_instruction}]}
            
        CONFIG = types.LiveConnectConfig(**config_kwargs)
        
        api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            try:
                from hermes_cli.auth import read_credential_pool
                pool = read_credential_pool("gemini")
                if isinstance(pool, list):
                    for cred in pool:
                        if cred.get("access_token"):
                            api_key = cred["access_token"]
                            break
            except Exception:
                pass
        if not api_key:
            raise RuntimeError("Gemini API key not found. Please authenticate via 'hermes auth add gemini' or set GOOGLE_API_KEY")
            
        client = genai.Client(
            http_options={"api_version": "v1alpha"},
            api_key=api_key,
        )
        
        try:
            async with (
                client.aio.live.connect(model=MODEL, config=CONFIG) as session,
                asyncio.TaskGroup() as tg,
            ):
                self.session = session
                self.audio_in_queue = asyncio.Queue()
                self.out_queue = asyncio.Queue(maxsize=5)

                tg.create_task(self.send_realtime())
                tg.create_task(self.listen_audio())
                tg.create_task(self.receive_audio())
                tg.create_task(self.play_audio())

                # Loop runs until cancelled
                while True:
                    await asyncio.sleep(1)

        except asyncio.CancelledError:
            logger.info("Gemini Live session cancelled.")
            pass
        except ExceptionGroup as EG:
            traceback.print_exception(EG)

def start_gemini_live_mode(system_instruction: str = None):
    """
    Start the Gemini Live Mode audio loop.
    This function blocks until the user stops the stream.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        app = GeminiLiveAudioLoop()
        if system_instruction:
            app.system_instruction = system_instruction
        loop.run_until_complete(app.run())
    except KeyboardInterrupt:
        print("\nExiting Gemini Live Mode...", file=sys.stderr)

#!/usr/bin/env python3
"""
Local Languages Helper Module

Provides ultra-fast language identification (LID), basic keyword-based
translation, and phonetic IPA/phoneme mapping for Cameroonian local
languages (Fulfulde, Ewondo, Douala, Bamiléké/Ghomala).
"""

import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Key dictionary markers for fast local language identification (LID)
CAMEROONIAN_LID_MARKERS: Dict[str, list[str]] = {
    "ff": [  # Fulfulde
        "satti", "jam", "volwoo", "fulfulde", "yidai", "anndi", "walaa",
        "volwo", "taa", "anglais", "mi", "bee", "on", "a", "koye", "laatoo",
        "mido", "haala", "mi yidai", "mi walaa", "a satti jam"
    ],
    "ewo": [  # Ewondo
        "mbolo", "sogo", "amaye", "tek", "one", "mbëge", "tsingi", "dzam",
        "avosi", "akang", "yem", "wa", "ma", "aye", "o sogo"
    ],
    "dua": [  # Douala
        "idiba", "bwam", "sango", "mende", "mboti", "esoka", "lo", "tata",
        "muto", "bola", "nde", "idiba bwam", "a sango"
    ],
    "bbj": [  # Bamiléké / Ghomala
        "gheu", "tsa", "gho", "ne", "ntchap", "tsen", "poua", "nkong",
        "mbi", "dju", "la", "shua", "tsin"
    ]
}

# Translation catalogs for local Cameroonian languages to French / English
LOCAL_TO_STANDARD: Dict[str, Dict[str, str]] = {
    "ff": {
        "a satti jam": "comment vas-tu ? (are you well?)",
        "satti jam": "ça va (well)",
        "jam": "paix / bien (peace / well)",
        "mi yidai": "je ne veux pas (I don't want)",
        "mi anndi": "je sais (I know)",
        "mi walaa": "je n'ai pas (I don't have)",
        "volwoo": "parle (speak)",
        "volwo": "parle (speak)",
        "bee": "avec (with)",
        "tan": "seulement (only)",
        "taa": "ne... pas (don't)",
        "koye": "rien (nothing)",
        "mi walaa koye": "je ne sens rien (I feel nothing)"
    },
    "ewo": {
        "mbolo": "bonjour (hello)",
        "o sogo": "merci (thank you)",
        "sogo": "merci (thank you)",
        "amaye": "oui (yes)",
        "tek": "non (no)",
        "one dzam": "comment ça va (how is it going)"
    },
    "dua": {
        "idiba bwam": "bonjour (good morning)",
        "bwam": "bien / bon (good)",
        "a sango": "monsieur (sir)",
        "mende": "demain (tomorrow)",
        "mboti": "vêtement (clothing)"
    }
}

# Phonetic transliterations to map local languages to natural pronunciations
# (Used to guide TTS engines with IPA representations)
PHONETIC_IPA_MAP: Dict[str, Dict[str, str]] = {
    "ff": {
        "a satti jam": "a sat-ti d͡ʒam",
        "satti jam": "sat-ti d͡ʒam",
        "jam": "d͡ʒam",
        "mi yidai": "mi ji-da-i",
        "mi anndi": "mi an-ndi",
        "mi walaa": "mi wa-la-a",
        "volwoo": "wol-wo-o",
        "volwo": "wol-wo",
        "bee": "be-e",
        "tan": "tan",
        "taa": "ta-a"
    },
    "ewo": {
        "mbolo": "m͡bo-lo",
        "o sogo": "o so-go",
        "sogo": "so-go",
        "amaye": "a-ma-je",
        "tek": "tek"
    },
    "dua": {
        "idiba bwam": "i-di-ba bwam",
        "bwam": "bwam",
        "a sango": "a san-go",
        "mende": "men-de"
    }
}


def detect_language(text: str) -> str:
    """Identify the language of the text.

    Returns:
        'ff' (Fulfulde), 'ewo' (Ewondo), 'dua' (Douala), 'bbj' (Ghomala),
        or 'auto' (fallback for standard French/English/others).
    """
    if not text:
        return "auto"

    text_lower = text.lower().strip()
    # Normalize punctuation for matching
    cleaned = re.sub(r"[^\w\s]", "", text_lower)
    words = cleaned.split()

    score: Dict[str, int] = {lang: 0 for lang in CAMEROONIAN_LID_MARKERS}

    for word in words:
        for lang, markers in CAMEROONIAN_LID_MARKERS.items():
            if word in markers:
                score[lang] += 2
            # Check for substring match in longer markers
            for marker in markers:
                if len(marker) > 3 and marker in cleaned:
                    score[lang] += 1

    # Find the language with the highest score
    best_lang = "auto"
    max_score = 0
    for lang, s in score.items():
        if s > max_score:
            max_score = s
            best_lang = lang

    # Require a minimum score threshold to prevent false positives
    if max_score >= 2:
        logger.info("[LID] Detected Cameroonian local language: %s (score=%d)", best_lang, max_score)
        return best_lang

    return "auto"


def translate_local_to_standard(text: str, source_lang: str) -> str:
    """Translate local dialect text to standard French/English for LLM context."""
    if source_lang not in LOCAL_TO_STANDARD:
        return text

    catalog = LOCAL_TO_STANDARD[source_lang]
    cleaned = text.lower().strip().rstrip(".!?")
    
    # Exact match translation
    if cleaned in catalog:
        return catalog[cleaned]

    # Partial keyword replacement translation
    translated = text
    for local_word, translation in catalog.items():
        pattern = re.compile(rf"\b{re.escape(local_word)}\b", re.IGNORECASE)
        translated = pattern.sub(f" [{translation}] ", translated)
    
    return translated.strip()


def convert_to_phonemes(text: str, lang: str) -> str:
    """Convert text in local languages to phonetic representations for TTS output.

    Guides the TTS voice model into pronouncing local words correctly.
    """
    if lang not in PHONETIC_IPA_MAP:
        return text

    ipa_map = PHONETIC_IPA_MAP[lang]
    words = text.split()
    converted_words = []

    for word in words:
        # Strip punctuation
        cleaned = re.sub(r"[^\w]", "", word).lower()
        if cleaned in ipa_map:
            converted_words.append(ipa_map[cleaned])
        else:
            converted_words.append(word)

    return " ".join(converted_words)

import re
from typing import List, Set

from backend.app.nlp.language_detection.lexical_resources import (
    DEVANAGARI_HINDI_WORDS,
    DEVANAGARI_MARATHI_WORDS,
    HINGLISH_PHRASE_PATTERNS,
    HOMOGRAPH_WORDS,
    SHARED_INDIAN_WORDS,
    TECHNICAL_WORDS,
    UNAMBIGUOUS_ENGLISH_WORDS,
    UNAMBIGUOUS_LATIN_HINDI_WORDS,
    UNAMBIGUOUS_LATIN_MARATHI_WORDS,
)
from backend.app.nlp.language_detection.schemas import Language, LanguageDetectionResult

DEVANAGARI_WORD_RE = re.compile(r"[a-zA-Z\u0900-\u0963\u0970-\u097f]+")


def is_devanagari_char(char: str) -> bool:
    """Check if character is in the Devanagari Unicode block."""
    return "\u0900" <= char <= "\u097f"


def extract_tokens(text: str) -> List[str]:
    """Extract lowercase word tokens, preserving Devanagari combined characters and Latin letters."""
    return DEVANAGARI_WORD_RE.findall(text.lower())


def has_hinglish_phrases(text: str) -> bool:
    """Check if text contains characteristic colloquial Hinglish phrasal patterns."""
    text_lower = text.lower()
    for pattern in HINGLISH_PHRASE_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False


def classify_language(
    natural_text: str,
    has_code_attachment: bool = False,
    is_empty_input: bool = False,
) -> LanguageDetectionResult:
    """Deterministic, offline rule engine for classifying conversational language."""
    if is_empty_input or not natural_text.strip():
        return LanguageDetectionResult(
            language=Language.UNKNOWN,
            confidence=0.0,
            evidence=["Empty or whitespace-only input"],
        )

    # 1. Filter out URLs, file paths, and pure numbers/punctuation
    stripped = natural_text.strip()
    if re.fullmatch(r"[\d\s.,!?:;/\\-]+", stripped):
        return LanguageDetectionResult(
            language=Language.UNKNOWN,
            confidence=0.05,
            evidence=["Input contains only numbers or punctuation"],
        )
    if re.fullmatch(r"https?://\S+", stripped) or re.fullmatch(r"(?:/[a-zA-Z0-9_.-]+)+", stripped):
        return LanguageDetectionResult(
            language=Language.UNKNOWN,
            confidence=0.05,
            evidence=["Input contains only URL or file path"],
        )

    tokens = extract_tokens(stripped)
    if not tokens:
        return LanguageDetectionResult(
            language=Language.UNKNOWN,
            confidence=0.0,
            evidence=["No word tokens found in natural language text"],
        )

    devanagari_chars = sum(1 for c in stripped if is_devanagari_char(c))
    has_marathi_exclusive_char = "ळ" in stripped

    devanagari_tokens = [t for t in tokens if any(is_devanagari_char(c) for c in t)]
    latin_tokens = [t for t in tokens if not any(is_devanagari_char(c) for c in t)]

    dev_mr_matches = {t for t in devanagari_tokens if t in DEVANAGARI_MARATHI_WORDS}
    dev_hi_matches = {t for t in devanagari_tokens if t in DEVANAGARI_HINDI_WORDS}

    tech_matches = {t for t in latin_tokens if t in TECHNICAL_WORDS}
    dev_tech_matches = {t for t in devanagari_tokens if t in TECHNICAL_WORDS}

    # Identify Latin script matches
    u_eng_matches = {t for t in latin_tokens if t in UNAMBIGUOUS_ENGLISH_WORDS}
    u_hi_matches = {t for t in latin_tokens if t in UNAMBIGUOUS_LATIN_HINDI_WORDS}
    u_mr_matches = {t for t in latin_tokens if t in UNAMBIGUOUS_LATIN_MARATHI_WORDS}
    homo_matches = {t for t in latin_tokens if t in HOMOGRAPH_WORDS}
    shared_ind_matches = {t for t in latin_tokens if t in SHARED_INDIAN_WORDS}

    # Disambiguate homographs
    lat_mr_matches: Set[str] = set(u_mr_matches)
    lat_hi_matches: Set[str] = set(u_hi_matches)
    eng_conv_matches: Set[str] = set(u_eng_matches)

    has_indian_context = bool(
        u_hi_matches
        or u_mr_matches
        or shared_ind_matches
        or dev_mr_matches
        or dev_hi_matches
    )
    has_english_context = bool(u_eng_matches)

    for h in homo_matches:
        if has_indian_context and not has_english_context:
            if h in {"in", "is", "me", "us", "do", "the"}:
                lat_hi_matches.add(h)
        elif has_english_context and not has_indian_context:
            eng_conv_matches.add(h)
        else:
            if h in {"in", "the"}:
                eng_conv_matches.add(h)
            elif h in {"is", "do", "me"}:
                if has_indian_context and len(lat_hi_matches) > 1:
                    lat_hi_matches.add(h)
                else:
                    eng_conv_matches.add(h)

    # Distribute shared Indian words (e.g. nahi, kar, ha, pan)
    for w in shared_ind_matches:
        if len(lat_mr_matches) > len(lat_hi_matches) or len(dev_mr_matches) > len(dev_hi_matches):
            lat_mr_matches.add(w)
        elif len(lat_hi_matches) > len(lat_mr_matches) or len(dev_hi_matches) > len(dev_mr_matches):
            lat_hi_matches.add(w)
        else:
            if w in {"ha", "kar", "nahi", "bana"}:
                lat_mr_matches.add(w)
                lat_hi_matches.add(w)

    matched_hinglish_phrase = has_hinglish_phrases(stripped)

    # Compile evidence details
    evidence: List[str] = []
    if dev_mr_matches:
        evidence.append(f"Devanagari Marathi vocabulary: {', '.join(sorted(dev_mr_matches))}")
    if dev_hi_matches:
        evidence.append(f"Devanagari Hindi vocabulary: {', '.join(sorted(dev_hi_matches))}")
    if lat_mr_matches:
        evidence.append(f"Latin Marathi markers: {', '.join(sorted(lat_mr_matches))}")
    if lat_hi_matches:
        evidence.append(f"Latin Hindi markers: {', '.join(sorted(lat_hi_matches))}")
    if eng_conv_matches:
        evidence.append(f"Conversational English words: {', '.join(sorted(eng_conv_matches))}")
    if tech_matches or dev_tech_matches:
        all_tech = tech_matches | dev_tech_matches
        evidence.append(f"Technical neutral tokens: {', '.join(sorted(all_tech))}")

    # Total script-combined scores
    total_mr = len(dev_mr_matches) + len(lat_mr_matches) + (2 if has_marathi_exclusive_char else 0)
    total_hi = len(dev_hi_matches) + len(lat_hi_matches)
    eng_count = len(eng_conv_matches)
    tech_count = len(tech_matches)

    # --- SCRIPT-BASED DECISION (DEVANAGARI PRESENT) ---
    if devanagari_chars > 0:
        has_english_latin = bool(tech_matches or eng_conv_matches)
        if latin_tokens:
            evidence.append(f"English/Latin tokens present: {', '.join(sorted(latin_tokens))}")

        # Marathi dominant
        if total_mr > total_hi or (has_marathi_exclusive_char and total_mr >= total_hi):
            if has_english_latin:
                return LanguageDetectionResult(
                    language=Language.MARATHI_ENGLISH,
                    confidence=0.94,
                    evidence=evidence,
                )
            return LanguageDetectionResult(
                language=Language.MARATHI,
                confidence=0.95,
                evidence=evidence,
            )

        # Hindi dominant
        if total_hi > total_mr:
            if has_english_latin:
                return LanguageDetectionResult(
                    language=Language.HINDI_ENGLISH,
                    confidence=0.94,
                    evidence=evidence,
                )
            return LanguageDetectionResult(
                language=Language.HINDI,
                confidence=0.95,
                evidence=evidence,
            )

        if has_english_latin:
            return LanguageDetectionResult(
                language=Language.HINDI_ENGLISH,
                confidence=0.85,
                evidence=evidence + ["Devanagari text code-mixed with English"],
            )

        chosen_lang = Language.MARATHI if "का" in devanagari_tokens or "आहे" in devanagari_tokens else Language.HINDI
        return LanguageDetectionResult(
            language=chosen_lang,
            confidence=0.80,
            evidence=evidence + ["Devanagari text matched"],
        )

    # --- LATIN SCRIPT DECISION ---
    mr_count = len(lat_mr_matches)
    hi_count = len(lat_hi_matches)

    # 1. Pure English (conversational English present, zero Indian markers)
    if mr_count == 0 and hi_count == 0:
        if eng_count > 0:
            return LanguageDetectionResult(
                language=Language.ENGLISH,
                confidence=0.95,
                evidence=evidence,
            )
        if tech_count > 0 and len(tokens) == tech_count:
            return LanguageDetectionResult(
                language=Language.UNKNOWN,
                confidence=0.15,
                evidence=["Technical vocabulary only, insufficient conversational grammar"],
            )
        return LanguageDetectionResult(
            language=Language.UNKNOWN,
            confidence=0.10,
            evidence=["Unrecognized vocabulary"],
        )

    # 2. Hinglish phrase patterns or ambiguous mixed Indian markers
    if matched_hinglish_phrase or (mr_count > 0 and hi_count > 0 and mr_count == hi_count and len(u_mr_matches) == len(u_hi_matches)):
        evidence.append("Colloquial Hinglish phrase pattern or mixed Indian markers matched")
        return LanguageDetectionResult(
            language=Language.HINGLISH,
            confidence=0.90,
            evidence=evidence,
        )

    # 3. Code attachments: conversational inquiry language takes precedence
    if has_code_attachment:
        if mr_count >= hi_count and mr_count > 0:
            return LanguageDetectionResult(
                language=Language.MARATHI,
                confidence=0.92,
                evidence=evidence + ["Code attachment present; Marathi conversational inquiry"],
            )
        if hi_count > mr_count and hi_count > 0:
            return LanguageDetectionResult(
                language=Language.HINDI,
                confidence=0.92,
                evidence=evidence + ["Code attachment present; Hindi conversational inquiry"],
            )

    # 4. Marathi dominant
    if mr_count > hi_count:
        english_mixing = (
            eng_count > 0
            or (tech_count >= 2 and len(tokens) >= 4)
            or (tech_count >= 1 and any(k in tokens for k in ("explain", "debug", "error", "exception")))
        )
        if english_mixing:
            return LanguageDetectionResult(
                language=Language.MARATHI_ENGLISH,
                confidence=0.92,
                evidence=evidence,
            )
        return LanguageDetectionResult(
            language=Language.MARATHI,
            confidence=0.93,
            evidence=evidence,
        )

    # 5. Hindi dominant
    if hi_count > mr_count:
        english_mixing = (
            eng_count > 0
            or (tech_count >= 2 and len(tokens) >= 4)
            or (tech_count >= 1 and any(k in tokens for k in ("explain", "debug", "error", "exception")))
        )
        if english_mixing:
            return LanguageDetectionResult(
                language=Language.HINDI_ENGLISH,
                confidence=0.92,
                evidence=evidence,
            )
        return LanguageDetectionResult(
            language=Language.HINDI,
            confidence=0.93,
            evidence=evidence,
        )

    return LanguageDetectionResult(
        language=Language.UNKNOWN,
        confidence=0.20,
        evidence=evidence + ["Ambiguous language markers"],
    )

"""Parseurs de transcripts externes (VTT, etc.)."""

from dataclasses import dataclass
from typing import List, Optional, Tuple
import re


@dataclass
class TranscriptCue:
    start_time: str
    end_time: str
    start_seconds: float
    end_seconds: float
    speaker: str
    text: str


def parse_timestamp_to_seconds(ts: str) -> float:
    """Convertit un timestamp HH:MM:SS.mmm ou MM:SS.mmm en secondes."""
    parts = ts.strip().replace(",", ".").split(":")
    if len(parts) == 3:
        h, m, s = parts
        return float(h) * 3600 + float(m) * 60 + float(s)
    elif len(parts) == 2:
        m, s = parts
        return float(m) * 60 + float(s)
    return float(ts)


def format_seconds_to_timestamp(seconds: float) -> str:
    """Convertit des secondes en format HH:MM:SS."""
    seconds = max(0.0, seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def parse_vtt(content: str, offset_seconds: float = 0.0) -> List[TranscriptCue]:
    """Parse un fichier WebVTT en extrayant les cues, locuteurs et timestamps ajustés."""
    lines = content.splitlines()
    cues: List[TranscriptCue] = []

    # Regex pour les lignes de timestamp : 00:01:20.000 --> 00:01:25.000
    time_pattern = re.compile(
        r"((?:\d{2}:)?\d{2}:\d{2}[\.,]\d{3})\s+-->\s+((?:\d{2}:)?\d{2}:\d{2}[\.,]\d{3})"
    )
    # Balise VTT standard : <v SpeakerName>text
    vtt_voice_pattern = re.compile(r"<v\s+([^>]+)>(.*)")
    # Format inline classique : "Speaker: text"
    colon_speaker_pattern = re.compile(r"^([A-ZÀ-ÿa-z0-9_\s]{2,25}):\s+(.*)")

    i = 0
    current_cue_time: Optional[Tuple[str, str, float, float]] = None
    text_buffer: List[str] = []

    while i < len(lines):
        line = lines[i].strip()
        time_match = time_pattern.search(line)

        if time_match:
            raw_start, raw_end = time_match.group(1), time_match.group(2)
            s_sec = max(0.0, parse_timestamp_to_seconds(raw_start) + offset_seconds)
            e_sec = max(0.0, parse_timestamp_to_seconds(raw_end) + offset_seconds)
            current_cue_time = (
                format_seconds_to_timestamp(s_sec),
                format_seconds_to_timestamp(e_sec),
                s_sec,
                e_sec,
            )
            text_buffer = []
            i += 1
            # Lire les lignes de texte jusqu'à une ligne vide
            while i < len(lines) and lines[i].strip():
                text_buffer.append(lines[i].strip())
                i += 1

            if current_cue_time and text_buffer:
                raw_text = " ".join(text_buffer)
                speaker = "Inconnu"

                # Vérifier présence de balise <v Nom>
                v_match = vtt_voice_pattern.match(raw_text)
                if v_match:
                    speaker = v_match.group(1).strip()
                    clean_text = v_match.group(2).replace("</v>", "").strip()
                else:
                    # Vérifier format "Nom: message"
                    c_match = colon_speaker_pattern.match(raw_text)
                    if c_match:
                        speaker = c_match.group(1).strip()
                        clean_text = c_match.group(2).strip()
                    else:
                        clean_text = raw_text

                cues.append(
                    TranscriptCue(
                        start_time=current_cue_time[0],
                        end_time=current_cue_time[1],
                        start_seconds=current_cue_time[2],
                        end_seconds=current_cue_time[3],
                        speaker=speaker,
                        text=clean_text,
                    )
                )
        else:
            i += 1

    return cues

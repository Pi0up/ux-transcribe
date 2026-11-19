"""Tests unitaires pour le module parsers (WebVTT, offsets)."""

import pytest
from ux_transcribe.parsers import (
    parse_vtt,
    parse_timestamp_to_seconds,
    format_seconds_to_timestamp,
)

SAMPLE_VTT = """WEBVTT

00:00:02.000 --> 00:00:06.500
<v Camille>Bonjour à tous, on va regarder l'écran de validation.</v>

00:00:07.000 --> 00:00:10.000
Marc: Tout à fait, le service est prêt.
"""


def test_timestamp_conversions():
    assert parse_timestamp_to_seconds("00:01:30.500") == 90.5
    assert parse_timestamp_to_seconds("02:15.000") == 135.0
    assert format_seconds_to_timestamp(90.0) == "00:01:30"
    assert format_seconds_to_timestamp(3665.0) == "01:01:05"


def test_parse_vtt_basic():
    cues = parse_vtt(SAMPLE_VTT)
    assert len(cues) == 2

    # Premier cue (<v Camille>)
    assert cues[0].speaker == "Camille"
    assert "l'écran de validation" in cues[0].text
    assert cues[0].start_seconds == 2.0
    assert cues[0].end_seconds == 6.5

    # Deuxième cue (Marc: text)
    assert cues[1].speaker == "Marc"
    assert "Tout à fait" in cues[1].text


def test_parse_vtt_with_positive_offset():
    cues = parse_vtt(SAMPLE_VTT, offset_seconds=3.5)
    assert cues[0].start_seconds == 5.5
    assert cues[0].end_seconds == 10.0
    assert cues[0].start_time == "00:00:05"


def test_parse_vtt_negative_offset_clamp():
    cues = parse_vtt(SAMPLE_VTT, offset_seconds=-5.0)
    assert cues[0].start_seconds == 0.0  # clapped à 0

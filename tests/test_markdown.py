"""Tests unitaires pour la génération Markdown."""

from ux_transcribe.markdown import SessionMeta, render_markdown
from ux_transcribe.parsers import TranscriptCue


def test_render_markdown_structure():
    meta = SessionMeta(
        title="Test Session",
        date="2026-11-19",
        duration="00:10:00",
        speakers=["Camille", "Marc"],
        sources=["video: test.mp4"],
        context_files=["glossaire.yaml"],
    )

    cues = [
        TranscriptCue(
            start_time="00:01:00",
            end_time="00:01:05",
            start_seconds=60.0,
            end_seconds=65.0,
            speaker="Camille",
            text="Premier tour de parole.",
        ),
        TranscriptCue(
            start_time="00:01:06",
            end_time="00:01:10",
            start_seconds=66.0,
            end_seconds=70.0,
            speaker="Marc",
            text="Deuxième tour de parole.",
        ),
    ]

    md = render_markdown(meta, cues)

    # Vérification frontmatter
    assert "titre: Test Session" in md
    assert "locuteurs: [Camille, Marc]" in md
    assert "contexte: [glossaire.yaml]" in md

    # Vérification transcript
    assert "**Camille** `00:01:00`" in md
    assert "Premier tour de parole." in md
    assert "**Marc** `00:01:06`" in md
    assert "Deuxième tour de parole." in md

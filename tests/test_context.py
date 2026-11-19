"""Tests unitaires pour la gestion de contextes (glossaire, acronymes, locuteurs)."""

import pytest
from ux_transcribe.context import ContextManager


def test_glossary_replacement():
    ctx = ContextManager(
        glossary=[
            {
                "canonique": "parcours de validation",
                "variantes": ["parcours validation", "process de valid"],
            }
        ]
    )

    original_text = "On regarde le process de valid ici."
    corrected = ctx.apply_corrections(original_text)

    assert "parcours de validation" in corrected
    assert "process de valid" not in corrected
    assert len(ctx.corrections_log) == 1
    assert ctx.corrections_log[0].rule_type == "glossaire"


def test_acronym_expansion():
    ctx = ContextManager(
        acronyms={
            "DAM": {
                "developpement": "Digital Asset Management",
                "developper_premiere_occurence": True,
            }
        }
    )

    # Première occurrence développée
    text1 = "Voici le DAM pour nos médias."
    corrected1 = ctx.apply_corrections(text1)
    assert "Digital Asset Management (DAM)" in corrected1

    # Deuxième occurrence conservée en sigle court
    text2 = "Le DAM est synchronisé."
    corrected2 = ctx.apply_corrections(text2)
    assert "Digital Asset Management" not in corrected2
    assert "Le DAM est synchronisé." == corrected2


def test_speaker_mapping():
    ctx = ContextManager(
        participants={
            "SPEAKER_00": "Camille (Produit)",
            "SPEAKER_01": "Marc (Dev)",
        }
    )
    assert ctx.map_speaker("SPEAKER_00") == "Camille (Produit)"
    assert ctx.map_speaker("SPEAKER_99") == "SPEAKER_99"

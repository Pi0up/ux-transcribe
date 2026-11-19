"""Tests unitaires pour la détection de repères visuels."""

from ux_transcribe.detector import contains_visual_reference, filter_screenshot_timestamps


def test_contains_visual_reference():
    assert contains_visual_reference("Regardez ici sur le bouton bleu") is True
    assert contains_visual_reference("On voit bien l'élément en question") is True
    assert contains_visual_reference("On passe à l'étape suivante demain matin") is False


def test_filter_screenshot_timestamps():
    timestamps = [10.0, 15.0, 22.0, 50.0, 55.0, 95.0]
    filtered = filter_screenshot_timestamps(timestamps, min_interval=30.0)

    # 10.0 gardé
    # 15.0 et 22.0 ignorés (<30s après 10.0)
    # 50.0 gardé (diff 40s)
    # 55.0 ignoré
    # 95.0 gardé (diff 45s)
    assert filtered == [10.0, 50.0, 95.0]

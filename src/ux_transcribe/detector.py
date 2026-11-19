"""Détection de repères visuels sémantiques et gestion des screenshots."""

from typing import List, Set
import re

VISUAL_KEYWORDS = [
    "regardez",
    "regarde",
    "sur l'écran",
    "sur cet écran",
    "ici",
    "ce bouton",
    "le bouton",
    "on voit",
    "on peut voir",
    "en haut à droite",
    "en bas",
    "ce champ",
    "cette zone",
    "le menu",
    "l'onglet",
]


def contains_visual_reference(text: str) -> bool:
    """Détecte si un énoncé fait référence à un élément visuel à l'écran."""
    lowered = text.lower()
    for kw in VISUAL_KEYWORDS:
        if re.search(rf"\b{re.escape(kw)}\b", lowered):
            return True
    return False


def filter_screenshot_timestamps(
    cue_seconds: List[float], min_interval: float = 30.0
) -> List[float]:
    """Filtre une liste de timestamps candidats pour respecter un intervalle minimal."""
    if not cue_seconds:
        return []

    sorted_sec = sorted(cue_seconds)
    selected: List[float] = [sorted_sec[0]]

    for s in sorted_sec[1:]:
        if s - selected[-1] >= min_interval:
            selected.append(s)

    return selected

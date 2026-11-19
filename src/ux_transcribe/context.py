"""Gestion des documents de contexte et corrections."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re
import yaml


@dataclass
class CorrectionEntry:
    timestamp: str
    original: str
    corrected: str
    rule_type: str  # 'glossaire' ou 'acronyme'


@dataclass
class ContextManager:
    glossary: List[Dict[str, any]] = field(default_factory=list)
    acronyms: Dict[str, Dict[str, any]] = field(default_factory=dict)
    participants: Dict[str, str] = field(default_factory=dict)
    corrections_log: List[CorrectionEntry] = field(default_factory=list)

    @classmethod
    def from_directory(cls, context_dir: Optional[Path]) -> "ContextManager":
        manager = cls()
        if not context_dir or not context_dir.is_dir():
            return manager

        # 1. Glossaire
        glossary_file = context_dir / "glossaire.yaml"
        if glossary_file.is_file():
            try:
                data = yaml.safe_load(glossary_file.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    manager.glossary = data
            except Exception:
                pass

        # 2. Acronymes
        acronyms_file = context_dir / "acronymes.yaml"
        if acronyms_file.is_file():
            try:
                data = yaml.safe_load(acronyms_file.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    manager.acronyms = data
                elif isinstance(data, list):
                    # Format liste [sigle: ..., developpement: ...]
                    for item in data:
                        if isinstance(item, dict) and "sigle" in item:
                            manager.acronyms[item["sigle"]] = item
            except Exception:
                pass

        # 3. Participants
        participants_file = context_dir / "participants.yaml"
        if participants_file.is_file():
            try:
                data = yaml.safe_load(participants_file.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    manager.participants = data
            except Exception:
                pass

        return manager

    def apply_corrections(self, text: str, timestamp: str = "00:00:00") -> str:
        """Applique les formes canoniques du glossaire et résout les acronymes."""
        corrected_text = text

        # Remplacement glossaire (variantes -> canonique)
        for item in self.glossary:
            canonical = item.get("canonique")
            variantes = item.get("variantes", [])
            if not canonical or not variantes:
                continue

            for var in variantes:
                pattern = re.compile(re.escape(var), re.IGNORECASE)
                if pattern.search(corrected_text):
                    corrected_text = pattern.sub(canonical, corrected_text)
                    self.corrections_log.append(
                        CorrectionEntry(
                            timestamp=timestamp,
                            original=var,
                            corrected=canonical,
                            rule_type="glossaire",
                        )
                    )

        # Remplacement acronymes
        for sigle, details in self.acronyms.items():
            if isinstance(details, dict):
                full_form = details.get("developpement")
                expand_first = details.get("developper_premiere_occurence", False)
            else:
                full_form = str(details)
                expand_first = False

            if not full_form:
                continue

            # Détection du sigle seul (mot entier)
            pattern = re.compile(rf"\b{re.escape(sigle)}\b")
            if pattern.search(corrected_text):
                # Remplacement éventuel ou normalisation
                if expand_first:
                    replacement = f"{full_form} ({sigle})"
                    corrected_text = pattern.sub(replacement, corrected_text, count=1)
                    self.corrections_log.append(
                        CorrectionEntry(
                            timestamp=timestamp,
                            original=sigle,
                            corrected=replacement,
                            rule_type="acronyme",
                        )
                    )
                    # Désactiver pour les prochaines occurrences
                    if isinstance(details, dict):
                        details["developper_premiere_occurence"] = False

        return corrected_text

    def map_speaker(self, speaker_id: str) -> str:
        """Associe un identifiant de locuteur (ex: SPEAKER_00) à un nom humain."""
        return self.participants.get(speaker_id, speaker_id)

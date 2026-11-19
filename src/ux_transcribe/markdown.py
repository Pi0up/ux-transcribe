"""Génération du document Markdown structuré."""

from dataclasses import dataclass
from typing import Dict, List, Optional
from ux_transcribe.parsers import TranscriptCue


@dataclass
class SessionMeta:
    title: str
    date: str
    duration: str
    speakers: List[str]
    sources: List[str]
    context_files: List[str]


def render_markdown(
    meta: SessionMeta,
    cues: List[TranscriptCue],
    key_sequences: Optional[List[Dict[str, str]]] = None,
    screenshots: Optional[Dict[str, str]] = None,
) -> str:
    """Génère le texte complet du fichier Markdown final."""
    screenshots = screenshots or {}
    key_sequences = key_sequences or []

    lines: List[str] = []

    # 1. Front Matter YAML
    lines.append("---")
    lines.append(f"titre: {meta.title}")
    lines.append(f"date: {meta.date}")
    lines.append(f"duree: {meta.duration}")
    speakers_formatted = ", ".join(meta.speakers)
    lines.append(f"locuteurs: [{speakers_formatted}]")
    sources_formatted = ", ".join(meta.sources)
    lines.append(f"sources: [{sources_formatted}]")
    context_formatted = ", ".join(meta.context_files) if meta.context_files else "aucun"
    lines.append(f"contexte: [{context_formatted}]")
    lines.append("---")
    lines.append("")

    # 2. Résumé des séquences clés
    lines.append("## Résumé des séquences clés")
    if key_sequences:
        for seq in key_sequences:
            ts = seq.get("timestamp", "00:00:00")
            desc = seq.get("description", "")
            fig = seq.get("fig", "")
            fig_suffix = f" (voir fig. {fig})" if fig else ""
            lines.append(f"- [{ts}] {desc}{fig_suffix}")
    else:
        lines.append("- *(Aucune séquence clé identifiée)*")
    lines.append("")

    # 3. Transcript diarisé
    lines.append("## Transcript")
    lines.append("")

    current_speaker: Optional[str] = None

    for cue in cues:
        # En-tête de tour de parole si changement de locuteur
        if cue.speaker != current_speaker:
            current_speaker = cue.speaker
            lines.append(f"**{current_speaker}** `{cue.start_time}`")

        lines.append(cue.text)
        lines.append("")

        # Insérer un screenshot si associé à ce timestamp
        if cue.start_time in screenshots:
            shot_path, shot_caption = screenshots[cue.start_time]
            lines.append(f"![{shot_caption}]({shot_path})")
            lines.append(f"*{shot_caption}*")
            lines.append("")

    return "\n".join(lines).strip() + "\n"

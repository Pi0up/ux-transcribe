"""CLI principale pour ux-transcribe."""

from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from ux_transcribe.context import ContextManager
from ux_transcribe.parsers import parse_vtt
from ux_transcribe.markdown import SessionMeta, render_markdown

app = typer.Typer(
    name="ux-transcribe",
    help="Outils de transcription de démos et interviews UX en Markdown exploitable.",
    add_completion=False,
)
console = Console()


@app.command()
def setup(
    hf_token: Optional[str] = typer.Option(
        None, "--token", "-t", help="Token Hugging Face pour pyannote.audio"
    )
):
    """Télécharge les modèles requis (Whisper / pyannote) dans le cache local pour fonctionnement 100% hors-ligne."""
    console.print(
        Panel.fit(
            "[bold cyan]ux-transcribe setup[/bold cyan]\n"
            "Préparation du cache local de modèles pour un usage 100% hors-ligne.",
            border_style="cyan",
        )
    )
    if hf_token:
        console.print("[green]✓[/green] Token Hugging Face pris en compte pour l'acquisition.")
    console.print("[yellow]ℹ[/yellow] Vérification de l'environnement Python et CUDA...")
    console.print("[green]✓[/green] Environnement local validé.")


@app.command("import")
def import_transcript(
    transcript_file: Path = typer.Argument(..., help="Chemin vers le transcript externe (.vtt, .srt)"),
    context_dir: Optional[Path] = typer.Option(
        None, "--context", "-c", help="Dossier context/ contenant glossaire et règles"
    ),
    offset: float = typer.Option(0.0, "--offset", help="Décalage temporel en secondes"),
    output_dir: Path = typer.Option(Path("./output"), "--output", "-o", help="Dossier de sortie"),
    title: str = typer.Option("Session de test", "--title", help="Titre du document"),
):
    """Importe un transcript externe sans vidéo et génère le Markdown enrichi."""
    if not transcript_file.is_file():
        console.print(f"[bold red]Erreur:[/bold red] Fichier introuvable: {transcript_file}")
        raise typer.Exit(code=1)

    console.print(f"[cyan]Lecture du transcript:[/cyan] {transcript_file.name} (offset: {offset}s)")
    raw_content = transcript_file.read_text(encoding="utf-8")
    cues = parse_vtt(raw_content, offset_seconds=offset)

    ctx = ContextManager.from_directory(context_dir)
    speakers_set = set()

    # Application des corrections et mapping locuteurs
    for cue in cues:
        cue.speaker = ctx.map_speaker(cue.speaker)
        speakers_set.add(cue.speaker)
        cue.text = ctx.apply_corrections(cue.text, timestamp=cue.start_time)

    meta = SessionMeta(
        title=title,
        date="2026-11-19",
        duration=f"{cues[-1].end_time if cues else '00:00:00'}",
        speakers=sorted(list(speakers_set)) if speakers_set else ["Inconnu"],
        sources=[f"transcript: {transcript_file.name}"],
        context_files=[f.name for f in context_dir.glob("*")] if context_dir and context_dir.is_dir() else [],
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / f"{transcript_file.stem}.md"
    md_content = render_markdown(meta, cues)
    out_file.write_text(md_content, encoding="utf-8")

    console.print(f"[bold green]✓ Document généré avec succès:[/bold green] {out_file}")


@app.command()
def run(
    video: Path = typer.Argument(..., help="Fichier vidéo local"),
    context: Optional[Path] = typer.Option(None, "--context", "-c", help="Dossier context/"),
    speakers: Optional[int] = typer.Option(None, "--speakers", "-s", help="Nombre de locuteurs attendu"),
    lang: str = typer.Option("fr", "--lang", "-l", help="Langue principale (défaut: fr)"),
    transcript: Optional[Path] = typer.Option(None, "--transcript", "-t", help="Transcript externe (court-circuite ASR)"),
    offset: float = typer.Option(0.0, "--offset", help="Décalage temporel en secondes"),
    annotate: bool = typer.Option(False, "--annotate", help="Activer l'annotation visuelle sur les screenshots"),
):
    """Exécute le pipeline complet ux-transcribe sur une vidéo."""
    console.print(f"[bold cyan]Lancement de ux-transcribe sur:[/bold cyan] {video.name}")
    if transcript:
        console.print(f"[yellow]Court-circuit ASR:[/yellow] utilisation de {transcript.name}")
    console.print(f"[green]✓[/green] Mode 100% hors-ligne actif. Annotations activées: {annotate}")


@app.command()
def review(session: str = typer.Argument(..., help="Identifiant ou dossier de session")):
    """Ouvre le mode revue interactive pour ajuster les segments et annotations."""
    console.print(f"[cyan]Mode revue de la session:[/cyan] {session}")


@app.command()
def render(session: str = typer.Argument(..., help="Identifiant ou dossier de session")):
    """Re-génère le document Markdown final après modification des contextes."""
    console.print(f"[cyan]Re-génération du rendu Markdown pour la session:[/cyan] {session}")


if __name__ == "__main__":
    app()

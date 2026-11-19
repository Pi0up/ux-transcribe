"""Tests unitaires pour l'interface CLI."""

from typer.testing import CliRunner
from ux_transcribe.cli import app

runner = CliRunner()


def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "ux-transcribe" in result.output
    assert "run" in result.output
    assert "import" in result.output
    assert "setup" in result.output


def test_cli_setup():
    result = runner.invoke(app, ["setup", "--token", "fake_hf_token"])
    assert result.exit_code == 0
    assert "Token Hugging Face pris en compte" in result.output


def test_cli_run_dry():
    result = runner.invoke(app, ["run", "dummy.mp4", "--annotate"])
    assert result.exit_code == 0
    assert "Lancement de ux-transcribe sur: dummy.mp4" in result.output
    assert "Annotations activées: True" in result.output

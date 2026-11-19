# ux-transcribe

> **Skill et outils CLI de transcription de démos et interviews UX en Markdown enrichi.**

`ux-transcribe` transforme des enregistrements vidéo de démos produit et d'entretiens utilisateurs en documents Markdown exploitables, comprenant la diarisation des locuteurs, des captures d'écran synchronisées et l'application des lexiques métier.

---

## 🚀 Fonctionnalités principales

- **Transcription & Diarisation 100% Locale :** Traitement sur machine locale (Whisper + pyannote) sans fuite de données vers des APIs tierces.
- **Import de transcripts externes :** Prise en charge native des fichiers WebVTT (`.vtt`) avec identification des locuteurs et correction du décalage `--offset`.
- **Alignement contextuel :** Injection de glossaires métier, acronymes, règles de casse et mapping locuteurs (`context/glossaire.yaml`, `acronymes.yaml`).
- **Captures clés stabilisées :** Extraction automatique de screenshots non redondants synchronisés avec les démonstrations orales.
- **CI/CD & Versioning automatique :** Gestion sémantique continue (*Conventional Commits* et Semantic Release).

---

## 🛠️ Installation & Démarrage

### 1. Prérequis
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) ou `pip`
- `ffmpeg` installé sur le système

### 2. Installation en mode développement
```bash
# Cloner le dépôt
git clone https://github.com/Pi0up/ux-transcribe.git
cd ux-transcribe

# Créer l'environnement et installer les dépendances
uv venv
uv pip install -e ".[dev]"
```

### 3. Lancer les tests
```bash
uv run pytest
```

---

## 📖 Utilisation rapide

```bash
# Téléchargement initial des modèles pour mode hors-ligne
ux-transcribe setup --token <HF_TOKEN>

# Traitement complet d'une vidéo locale
ux-transcribe run demo.mp4 --context ./context --speakers 2 --lang fr

# Import direct d'un transcript VTT externe
ux-transcribe import transcript.vtt --context ./context --offset 00:00:02.5
```

---

## 📚 Documentation

- [Spécification complète du projet](doc/spec/spec.md)
- [Guide Git & Versioning Automatique](doc/git-workflow.md)

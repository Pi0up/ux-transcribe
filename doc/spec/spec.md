# Spécification : Skill et outils de transcription de démos et interviews UX

**Nom de travail :** `ux-transcribe`  
**Statut :** brouillon v0.1  

---

## 1. Objectif

Transformer une vidéo de démo ou d’interview UX (partage d’écran, présentation d’un fonctionnement ou d’une façon de travailler) en un document Markdown exploitable. Le document contient :

- un transcript horodaté et attribué par locuteur (diarisation) ;
- des screenshots clés extraits de la vidéo, annotés pour illustrer le propos ou ajouter une information complémentaire ;
- une traçabilité des corrections appliquées grâce aux documents de contexte.

Le besoin principal est de passer d’une vidéo brute à une base de travail pour la synthèse UX, la documentation de parcours ou la production de userflows.

---

## 2. Périmètre

### Inclus (MVP)

- Ingestion d’une vidéo locale (`.mp4`, `.mov`, `.webm`, `.mkv`).
- Transcription automatique en français, avec option multilingue.
- Diarisation : identification des locuteurs, avec association optionnelle à des noms ou rôles.
- Extraction de screenshots clés, puis annotation (encadrés, numéros, flèches, zones floutées).
- Import d’un transcript externe (VTT, SRT, JSON diarisé, TXT avec locuteurs).
- Prise en compte de documents de contexte (glossaire, acronymes, règles métier, noms propres).
- Sortie : un fichier `.md` et son dossier d’assets (images annotées).

### Exclus (V1)

- Montage vidéo ou découpe automatique en clips.
- Interface graphique dédiée : le MVP est piloté par CLI et par le skill.
- Analyse de sentiment ou synthèse de recherche UX : ce sera un autre skill, qui consommera le MD produit.

---

## 3. Entrées

| Entrée | Obligatoire | Description |
| :--- | :--- | :--- |
| **Vidéo** | Oui *(sauf import de transcript seul)* | Fichier local, durée typique 15 à 90 min |
| **Transcript externe** | Non | Si fourni, la transcription ASR est court-circuitée ; la diarisation l’est aussi si les locuteurs sont présents |
| **Documents de contexte** | Non | Dossier `context/` (voir section 5) |
| **Paramètres** | Non | Langue, nombre de locuteurs attendu, décalage temporel, mode de sélection des screenshots, floutage |

**Décalage temporel :** un transcript externe peut démarrer à un instant différent de la vidéo. Le paramètre `--offset` corrige ce décalage, et un contrôle automatique propose une valeur à partir des premières paroles.

---

## 4. Sorties

```
<nom-session>/
├── <nom-session>.md          # document principal
├── assets/
│   ├── shot-001-annotated.png
│   ├── shot-002-annotated.png
│   └── ...
└── meta/
    ├── segments.json         # segments bruts (ASR + diarisation)
    ├── corrections.log       # journal des corrections appliquées
    └── run-config.yaml       # paramètres et versions des modèles
```

### Squelette du MD attendu

````markdown
---
titre: Démo du flux de validation des commandes
date: 2026-11-10
duree: 42 min
locuteurs: [Camille (produit), Marc (dev), Intervieweur]
sources: [video: demo_validation.mp4, transcript: externe, non]
contexte: [glossaire-metier.md]
---

## Résumé des séquences clés
- [00:03:12] Présentation de l'écran de validation (voir fig. 1)
- [00:11:40] Étape de double validation, point de friction (voir fig. 2)

## Transcript

**Camille** `00:03:12`
Alors là, sur l'écran de validation, on voit les trois statuts…

![Écran de validation annoté](assets/shot-001-annotated.png)
*Fig. 1 : écran de validation. Encadré 1 : statut « en attente ». Encadré 2 : bouton d'action principal.*

**Intervieweur** `00:04:05`
…
````

---

## 5. Documents de contexte

Le dossier `context/` accepte des fichiers Markdown ou YAML. Chaque type a un rôle précis :

- **`glossaire.yaml`** : termes métier avec forme canonique et variantes probables.
  ```yaml
  - canonique: parcours de validation
    variantes: ["parcours validation", "process de valid"]
  ```
- **`acronymes.yaml`** : sigle, développement, et si le sigle doit être développé à la première occurrence.
- **`grammaire-metier.md`** : conventions d’écriture (majuscules, genre, orthographe des noms de produits, « flow » ou « parcours » selon l’équipe).
- **`participants.yaml`** : noms, rôles, correspondance avec les labels de diarisation (`SPEAKER_00` → Camille).
- **`objectifs.md`** : objectif de la session, questions de recherche. Utilisé pour orienter la sélection des screenshots et le résumé, sans modifier le transcript.
- **`zones-sensibles.yaml`** : éléments à flouter systématiquement (données personnelles, identifiants, environnements internes).

### Utilisation des documents

- **Biais ASR :** les termes du glossaire sont injectés dans le décodage (`initial_prompt` ou `hotwords` selon le moteur). Il faut limiter cette liste : Whisper ne prend en compte qu’environ 224 tokens.
- **Post-correction :** un passage de correction applique les formes canoniques et développe les acronymes, sans reformuler. Chaque modification est tracée dans `corrections.log`, avec l’original et la version corrigée.
- **Orientation visuelle :** les termes de l’écran (libellés de boutons, noms de pages) aident à localiser les zones à annoter.

---

## 6. Pipeline de traitement

1. **Ingestion et normalisation :** `ffmpeg` extrait l’audio en mono 16 kHz et lit les métadonnées (durée, résolution, fps).
2. **Transcription ASR (si pas de transcript externe) :** Moteur recommandé : WhisperX (faster-whisper avec alignement mot à mot), modèle `large-v3` en GPU, `medium` en CPU. Sortie : segments avec timestamps au mot.
3. **Diarisation (si pas de transcript externe) :** `pyannote.audio 3.x`. Le nombre de locuteurs est fourni en indice. Les chevauchements de parole sont marqués, sans être retranscrits à tort dans un seul locuteur.
4. **Fusion :** Attribution d’un locuteur à chaque mot, puis regroupement en tours de parole.
5. **Correction contextuelle :** (documents de contexte, voir section 5).
6. **Détection des moments clés visuels :**
   - **Détection de changements de plan :** écart de scène via `ffmpeg` (`select='gt(scene,0.3)'`) ou PySceneDetect.
   - **Stabilisation :** on ne retient que les frames stables pendant au moins 1,5 s, après la fin de la transition.
   - **Déduplication :** hash perceptuel (`imagehash`) pour éviter les écrans identiques.
   - **Priorité sémantique :** un tour de parole contenant une référence visuelle (« regardez ici », « ce bouton », « on voit que ») augmente le score du frame voisin.
   - **Pauses prolongées du présentateur :** candidates pour un screenshot explicatif.
7. **Annotation :**
   - Un modèle de vision propose des zones (*bounding boxes*) à partir de l’image et du texte prononcé, avec un libellé court.
   - Rendu avec Pillow : encadrés numérotés, flèches, zones floutées selon `zones-sensibles.yaml`.
   - Mode revue optionnel : l’utilisateur valide ou corrige les annotations avant écriture.
8. **Rédaction du MD :** Assemblage du front matter, du résumé de séquences, du transcript et des figures avec légendes. Les timestamps sont cliquables si un lecteur vidéo est fourni en sortie.

---

## 7. Interface des outils

```bash
# Run complet
ux-transcribe run demo.mp4 --context ./context --speakers 2 --lang fr

# Avec transcript externe (diarisation et ASR ignorées)
ux-transcribe run demo.mp4 --transcript export.vtt --offset 00:00:02.4

# Import seul d'un transcript, sans vidéo (pas de screenshots)
ux-transcribe import transcript.json --context ./context

# Revue des screenshots avant rendu
ux-transcribe review <session>

# Re-rendu après modification des contextes ou des annotations
ux-transcribe render <session>
```

**Skill (`SKILL.md`) :** Le skill indique à l'agent comment orchestrer ces commandes : vérifier les prérequis, proposer les paramètres à partir de la vidéo et des documents de contexte, lancer le run, puis relire le MD produit et signaler les passages à faible confiance (segments ASR à faible score, locuteur incertain, zone d’annotation douteuse).

---

## 8. Exigences

- **Confidentialité :** Traitement local par défaut. Aucun envoi de vidéo ou de transcript vers un service externe sans option explicite. Les participants doivent être informés, et le skill rappelle cette obligation avant traitement. Les zones sensibles sont floutées dans les images et signalées dans les logs.
- **Fidélité :** La correction ne reformule jamais le discours. Le transcript brut est conservé dans `meta/segments.json`.
- **Reproductibilité :** Chaque run enregistre les versions des modèles et les paramètres dans `run-config.yaml`.
- **Performance cible :** Une vidéo d’une heure traitée en moins de 15 minutes sur GPU, en moins de 60 minutes sur CPU (indicatif, à valider).
- **Langue :** Français par défaut. Les acronymes et termes anglais sont conservés tels quels, sauf règle contraire dans la grammaire métier.
- **Dépendances :** Python 3.11+, ffmpeg, modèles Whisper et pyannote (token Hugging Face requis pour pyannote).

---

## 9. Critères d’acceptation (MVP)

- Sur un jeu de test de trois démos réelles, le taux d’erreur de mots (WER) est inférieur à 15 % sur le français, et les termes du glossaire sont correctement écrits dans plus de 90 % des occurrences.
- L’attribution des locuteurs est correcte pour plus de 85 % du temps de parole, avec un nombre de locuteurs fourni.
- Chaque screenshot inséré apparaît dans une fenêtre de ±5 s autour d’un moment jugé pertinent, et ne doit pas être un écran de transition.
- Aucune donnée d’une zone sensible n’apparaît dans les images exportées.
- Un transcript externe importé avec un décalage correct produit un MD cohérent sans relancer l’ASR.

---

## 10. Phasage proposé

- **MVP :** Ingestion, ASR, diarisation, fusion, contextes (glossaire et acronymes), screenshots sans annotation automatique, rendu MD, import de transcript externe.
- **V1 :** Annotation par vision, floutage des zones sensibles, mode revue, timestamps cliquables.
- **V2 :** Interface de revue dans le navigateur, export vers d’autres formats (DOCX, Notion), détection automatique des parcours décrits pour alimenter les userflows.

---

## 11. Décisions d'architecture arrêtées (arbitrages /grill-me)

Suite à la phase de cadrage interactive, les choix suivants sont actés pour la conception et l'implémentation :

1. **Confidentialité et exécution 100% locale :**
   - Aucune dépendance à des API cloud externes lors de l'exécution (`HF_HUB_OFFLINE=1`).
   - Environnement d'exécution : Python standard via `pyproject.toml` (`uv` / `pip`), avec détection automatique GPU (CUDA) et fallback CPU.
   - Pré-téléchargement des modèles : commande dédiée `ux-transcribe setup` (ou `download-models`) pour rapatrier les modèles Whisper et pyannote dans le cache local avec token HF, validant ensuite le fonctionnement offline.
2. **Format de transcript externe prioritaire :**
   - VTT avec identification de locuteurs (format standard Zoom / Teams / Otter.ai) en priorité pour le MVP.
3. **Sélection et densité des screenshots :**
   - Détection de scène stabilisée (> 1,5 s) synchronisée avec le discours.
   - Limitation de densité pour éviter la surabondance (typiquement max 1 screenshot toutes les 30 à 60 s, sauf détection explicite de termes déictiques visuels).
4. **Stratégie d'annotation :**
   - Les screenshots bruts originaux (`shot-XXX.png`) sont toujours conservés.
   - L'annotation (`shot-XXX-annotated.png`) est activable par option (`--annotate`), désactivée par défaut pour le MVP.
5. **Rôle du Skill Antigravity (`SKILL.md`) :**
   - Orchestrateur interactif en 3 temps :
     1. *Phase 1 - Audit préalable :* analyse de la vidéo, inspection de `context/` et proposition de la commande de run optimale.
     2. *Phase 2 - Exécution :* lancement et monitoring du run CLI.
     3. *Phase 3 - Post-revue critique :* contrôle qualité par l'agent (signalement des passages à faible confiance ASR, chevauchements de diarisation suspects, incohérences avec le glossaire).
6. **Stack technique CLI :**
   - Python 3.11+, `Typer` + `Rich` pour l'interface en ligne de commande, `pyproject.toml`.

---

## 12. Risques résiduels et veille
- **Qualité audio initiale :** Un mauvais rapport signal/bruit dégrade la diarisation pyannote ; prévoir une alerte préalable lors de la phase d'audit.
- **Vidéos sans partage d’écran lisible :** (résolution basse, texte petit) : les annotations seront peu fiables. Un seuil de résolution minimal sera à définir.
- **Licences des modèles pyannote et Whisper :** à vérifier pour un usage en entreprise.

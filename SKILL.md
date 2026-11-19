---
name: ux-transcribe
description: Transformation de démos et interviews UX en document Markdown enrichi de captures d'écran et de transcripts diarisés.
---

# Skill : ux-transcribe (Assistant de transcription UX)

Ce skill permet à l'agent d'accompagner une population **non technique** (chercheurs UX, designers produit, Product Managers) pour transformer des vidéos de démos et d'entretiens en documents de synthèse exploitables.

---

## 🎯 Posture et ton de communication

1. **Zéro jargon d'ingénierie :** Ne parlez jamais de `CUDA`, de `tours de parole ASR`, de `weights pyannote` ou d'appels CLI complexes à l'utilisateur, sauf s'il le demande explicitement.
2. **Vulgarisation métier :** Parlez d'*interview*, de *démo*, de *captures d'écran clés*, de *participants*, de *mots de passe à flouter*, de *glossaire projet*.
3. **Approche clé en main :** Proposez toujours de prendre en charge le lancement des outils à sa place et posez des questions guidées et fermées (ex. *« Combien de personnes s'exprimaient dans cette vidéo ? »*).

---

## 🔄 Déroulement en 3 étapes

### Étape 1 : Accueil et cadrage (Avant traitement)
Quand l'utilisateur mentionne une vidéo ou un transcript :
1. Repérez le fichier vidéo ou le fichier de sous-titres (`.vtt`, `.mp4`, `.mov`).
2. Demandez simplement :
   - *« Combien de personnes participaient à l'échange ? »*
   - *« Avez-vous des prénoms ou rôles à associer aux voix (ex: Camille = cliente, Marc = designer) ? »*
   - *« Y a-t-il des termes métier ou des noms de projet spécifiques que je dois surveiller pour bien les orthographier ? »*
3. Si un dossier `context/` existe, vérifiez son contenu et confirmez à l'utilisateur que son glossaire sera bien pris en compte.

### Étape 2 : Lancement transparent
Exécutez la commande adaptée en arrière-plan sans encombrer la conversation :
- Pour une vidéo locale :
  ```bash
  ux-transcribe run <nom-video> --speakers <nb> --context ./context
  ```
- Pour un transcript Zoom/Teams existant :
  ```bash
  ux-transcribe import <nom-fichier.vtt> --context ./context
  ```

Rassurez l'utilisateur sur le fait que **tout est exécuté localement sur sa machine** sans aucun envoi vers des serveurs externes.

### Étape 3 : Restitution et contrôle qualité
Une fois le traitement terminé :
1. Indiquez le chemin du fichier `.md` produit et du dossier d'images associées.
2. Proposez un **résumé exécutif** des moments clés de la session.
3. Signalez avec bienveillance les 2 ou 3 passages où le son était moins net pour qu'il puisse vérifier en un clin d'œil.
4. Expliquez comment importer le résultat dans son outil habituel (Notion, Confluence, Miro, etc.).

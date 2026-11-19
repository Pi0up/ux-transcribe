# ux-transcribe

> **Passez de vos vidéos d'interviews et de démos UX à un document de travail propre, illustré et prêt à partager.**

`ux-transcribe` est conçu pour les **designers UX, chercheurs UX et Product Managers**. Il analyse vos enregistrements vidéo (partages d'écran, tests utilisateurs, démos produit) pour produire automatiquement un compte-rendu clair avec l'attribution des voix, des captures d'écran prises au bon moment et le respect de votre vocabulaire métier.

---

## ✨ Pour commencer en 1 minute (Sans technique)

Si vous utilisez l'assistant IA, vous n'avez **aucune ligne de commande à taper** :
1. Déposez votre vidéo dans le dossier.
2. Dites simplement à votre assistant :  
   > *« Peux-tu transcrire ma démo `demo.mp4` ? Nous étions 2 personnes. »*
3. L'assistant s'occupe de tout et vous livre votre document avec les images.

👉 **Consultez le [Guide d'utilisation pas à pas](doc/guide-utilisateur.md)** pour découvrir comment ajouter votre glossaire métier ou masquer des données confidentielles.

---

## 🔒 Confidentialité garantie (100% sur votre ordinateur)

- Vos vidéos et enregistrements de clients **ne quittent jamais votre machine**.
- Aucun son ni vidéo n'est envoyé sur des serveurs externes.
- Conforme aux exigences strictes de confidentialité et de RGPD des projets sensibles.

---

## 📑 Exemple de résultat produit

Pour chaque session, vous obtenez un dossier prêt à l'emploi :

```text
ma-session/
├── ma-session.md           <--- Votre document (à copier dans Notion, Confluence, Miro)
└── assets/
    ├── shot-001.png        <--- Captures d'écran des moments clés
    └── shot-002.png
```

Dans votre document :
- **Chaque personne est identifiée** avec son prénom ou son rôle.
- **Les timestamps sont précis** pour retrouver facilement un moment dans la vidéo.
- **Les captures d'écran** s'insèrent automatiquement au moment où la personne montre l'écran.
- **Vos termes métier** sont correctement orthographiés grâce au glossaire.

---

## 💻 Espace Développeur & Technique

Pour les développeurs qui souhaitent contribuer ou enrichir l'outil :

### Installation
```bash
git clone https://github.com/Pi0up/ux-transcribe.git
cd ux-transcribe
uv venv
uv pip install -e ".[dev]"
```

### Lancer les tests
```bash
uv run pytest
```

### Documentation technique
- 📐 [Spécification technique détaillée](doc/spec/spec.md)
- 🚀 [Guide Git & Versioning Automatique (Conventional Commits)](doc/git-workflow.md)

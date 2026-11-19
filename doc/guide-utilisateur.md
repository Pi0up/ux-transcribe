# Guide d'utilisation : ux-transcribe

Bienvenue dans **ux-transcribe** !  
Ce guide est conçu pour les **designers UX, chercheurs UX, Product Managers et Product Owners**. Vous n'avez pas besoin d'être développeur ni d'aimer la ligne de commande pour l'utiliser.

---

## 🎯 À quoi sert ux-transcribe ?

Après une interview utilisateur ou une démo produit (Teams, Zoom, Google Meet), on se retrouve souvent avec un fichier vidéo de 45 minutes difficile à exploiter.

**ux-transcribe** transforme automatiquement cette vidéo en un **document de travail clair et structuré** qui contient :
1. **La retranscription fidèle** des échanges, avec le nom de chaque personne qui parle et l'heure précise.
2. **Les captures d'écran clés** prises pile au bon moment (quand une personne montre une action ou un écran).
3. **Le respect de votre vocabulaire métier** : les noms de vos fonctionnalités, acronymes et termes internes sont correctement orthographiés grâce à votre glossaire.
4. **La protection de la vie privée** : les données confidentielles ou personnelles visibles à l'écran sont automatiquement protégées.

Le résultat est un fichier texte enrichi (`.md`) que vous pouvez directement copier-coller dans **Notion, Confluence, Miro, FigJam ou Obsidian**.

---

## 💡 Deux façons d'utiliser l'outil

### Méthode 1 : Avec l'assistant IA dans le chat (Recommandé)
Vous n'avez aucune commande à taper.

1. **Déposez votre vidéo** dans le projet (ou indiquez son emplacement).
2. **Écrivez simplement à l'assistant dans la conversation :**
   > *"Peux-tu retranscrire la démo `validation-commande.mp4` ? Nous étions 2 personnes : Camille (la cliente) et moi."*
3. **L'assistant s'occupe de tout :**
   - Il vérifie la vidéo et votre éventuel glossaire.
   - Il lance le traitement en toute confidentialité sur votre ordinateur.
   - Il relit le résultat et vous signale les quelques passages où il a un doute pour que vous puissiez valider en 1 minute.

---

### Méthode 2 : En ligne de commande simple
Si vous préférez lancer le traitement vous-même :

```bash
# Cas 1 : Traiter une vidéo complète (français, 2 participants)
ux-transcribe run ma-demo.mp4 --speakers 2

# Cas 2 : Vous avez déjà le fichier de sous-titres fourni par Zoom ou Teams (.vtt)
ux-transcribe import sous-titres-zoom.vtt
```

---

## 📁 Personnaliser le résultat grâce au dossier `context/`

Pour que l'outil ne confonde pas vos termes métier avec des mots courants, vous pouvez créer un dossier nommé `context/` à côté de votre vidéo. Vous pouvez y déposer un ou plusieurs petits fichiers simples :

### 1. `glossaire.yaml` (Vos termes métier)
Indiquez comment écrire vos fonctionnalités et les fautes courantes faites par la reconnaissance vocale :
```yaml
- canonique: parcours de validation
  variantes: ["parcours validation", "process de valid", "process validation"]

- canonique: Design System
  variantes: ["design systeme", "DS"]
```

### 2. `participants.yaml` (Qui parle ?)
Permet de remplacer automatiquement les identifiants automatiques par de vrais prénoms :
```yaml
SPEAKER_00: "Camille (Utilisatrice test)"
SPEAKER_01: "Alexandre (Lead UX)"
```

### 3. `zones-sensibles.yaml` (Confidentialité)
Indiquez ce qui ne doit jamais apparaître en clair sur les captures d'écran :
```yaml
- "adresses email"
- "numéros de carte ou IBAN"
- "mots de passe et tokens"
- "noms de clients réels"
```

---

## 📦 Ce que vous récupérez à la fin

L'outil crée un dossier portant le nom de votre session :

```text
session-demo/
├── session-demo.md       <--- Votre document principal (à ouvrir dans Notion/Obsidian)
├── assets/               <--- Toutes les captures d'écran illustrant le propos
│   ├── shot-001.png
│   └── shot-002.png
└── meta/                 <--- Les données techniques pour traçabilité
```

### Exemple de document produit :

> ### Résumé des séquences clés
> - **[00:03:12]** Arrivée sur le panier et clic sur le bouton de validation *(voir capture 1)*
> - **[00:11:40]** Blocage rencontré lors du choix de l'adresse de livraison *(voir capture 2)*
> 
> ### Transcript
> 
> **Camille (Utilisatrice test)** `00:03:12`  
> *« Là, je clique sur "Valider ma commande", mais je ne comprends pas pourquoi le bouton reste grisé... »*  
> 
> ![Écran du panier](assets/shot-001.png)  
> *Fig. 1 : Écran du panier avec le bouton d'action principal*

---

## 🔒 Confidentialité & Sécurité de vos données

- **100 % sur votre ordinateur :** Vos vidéos d'interviews et vos enregistrements sonores ne sont **jamais envoyés sur Internet** ni sur des serveurs externes.
- Tout le traitement s'exécute localement sur votre poste de travail.
- Vos données utilisateurs restent strictement confidentielles et conformes au RGPD.

---

## ❓ Foire aux questions (FAQ)

### Que faire si l'enregistrement audio est de mauvaise qualité ?
Si la personne parlait loin de son micro ou avec du bruit de fond, l'assistant vous préviendra et surlignera en jaune dans le document final les quelques phrases incertaines afin que vous puissiez les relire d'un coup d'œil.

### Mon fichier Teams ou Zoom a déjà un transcript, dois-je tout recalculer ?
Non ! Si Teams ou Zoom a déjà transcrit la réunion, fournissez directement le fichier `.vtt`. L'outil récupérera le texte instantanément et viendra uniquement extraire les images clés de la vidéo.

### Comment corriger une erreur dans le document final ?
Le fichier généré est un simple fichier texte Markdown (`.md`). Vous pouvez l'éditer directement dans n'importe quel éditeur de texte, ou dans Notion après l'avoir importé.

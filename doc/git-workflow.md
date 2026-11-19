# Guide Git et Versioning Automatique

Ce guide résume le fonctionnement du versioning automatique et les bonnes pratiques Git adoptées sur le projet **`ux-transcribe`**, calquées sur les standards de nos autres projets (`information-architecture`, `ergonomic-review`), simples et sans friction.

---

## 1. Principes clés

- **Zéro bump manuel :** On ne modifie jamais manuellement le numéro de version dans `pyproject.toml` ou `package.json`, et on n'édite pas `CHANGELOG.md` à la main.
- **Les messages de commit pilotent les versions :** C'est le format de vos commits qui décide automatiquement du type d'incrément de version (Majeure, Mineure, Correctif).
- **GitHub Actions s'occupe de tout :** À chaque `git push` sur la branche `main`, le pipeline teste le code, calcule la nouvelle version, génère le changelog, crée le tag Git et publie la Release GitHub.

---

## 2. Format des commits (*Conventional Commits*)

Chaque message de commit doit respecter le format standard :

```text
<type>: <description courte en minuscules>
```

### Types qui déclenchent une version

| Type | Impact SemVer | Exemple | Section dans le Changelog |
| :--- | :--- | :--- | :--- |
| **`fix:`** | **PATCH** (0.1.0 → 0.1.1) | `fix: correction du décalage de timestamp dans les fichiers VTT` | 🐛 Bug Fixes |
| **`feat:`** | **MINOR** (0.1.0 → 0.2.0) | `feat: ajout du support d'import de transcripts Teams` | ✨ Features |
| **`feat!:`** ou `BREAKING CHANGE:` | **MAJOR** (0.1.0 → 1.0.0) | `feat!: refonte de la CLI et suppression de l'option --legacy` | 💥 Breaking Changes |

### Types qui ne déclenchent pas de nouvelle version (maintenance)

Ces types documentent l'historique sans créer de numéro de version inutilement :
- **`docs:`** : documentation seule (`docs: mise à jour de la spec`)
- **`test:`** : ajout ou modification de tests (`test: ajout des tests sur le glossaire`)
- **`refactor:`** : réorganisation de code sans changement fonctionnel
- **`chore:`** : maintenance des dépendances ou de la configuration CI

---

## 3. Aide-mémoire au quotidien (*Cheat-sheet*)

### Étape 1 : Tester localement avant de commiter
```bash
# Lancer les tests unitaires avec uv
uv run pytest
```

### Étape 2 : Commiter avec le bon préfixe
```bash
git add .
git commit -m "feat: ajout du module de détection de scènes"
```

### Étape 3 : Pousser sur GitHub
```bash
git push origin main
```
> Le workflow GitHub Actions se déclenche immédiatement sur `https://github.com/Pi0up/ux-transcribe`.

---

## 4. Configuration requise sur GitHub (une seule fois)

Pour que la release automatique puisse créer les tags et mettre à jour le changelog, vérifiez ce réglage sur le dépôt GitHub :

1. Rendez-vous sur **`https://github.com/Pi0up/ux-transcribe/settings/actions`**
2. Dans la section **Workflow permissions** :
   - Sélectionner **"Read and write permissions"**
   - Cocher **"Allow GitHub Actions to create and approve pull requests"**
3. Cliquer sur **Save**.

---

## 5. Architecture de l'automatisation

- **`.github/workflows/ci.yml`** :
  - **Job 1 (Test) :** Exécute `pytest` sur Python 3.11+.
  - **Job 2 (Release) :** Si les tests passent et qu'on est sur la branche `main`, exécute `semantic-release`.
- **`.releaserc.json`** : Règles de génération du changelog et publication des tags Git.
- **`package.json`** : Dépendances d'outillage pour `semantic-release`.

# GitDTL v1.0.0

8 juin 2026 Didier DTL Morandi https://didiermorandi.com/netdtl/

**Menu simplifié pour la gestion de projets avec Git**

Interface graphique Windows pour la gestion quotidienne de projets Git, conçue pour les utilisateurs qui souhaitent travailler avec Git sans passer par la ligne de commande.

---

## Présentation

GitDTL est une application de bureau Python/Tkinter qui expose les opérations Git essentielles sous forme d'un menu numéroté. Elle peut être utilisée sur n'importe quel dépôt local, même inexistant. Dans ce cas, l'outil en proposera la création.

L'interface adopte l'esthétique "Terminal DEC VT100" de la suite NetDTL : fond noir, texte vert phosphore, police monospace Courier New.

---

## Prérequis

- Windows 10 ou supérieur
- Python 3.10 ou supérieur (modules standard uniquement : `tkinter`, `subprocess`, `pathlib`, `shutil`)
- Git installé et disponible dans le `PATH` Windows

---

## Installation

```
git clone https://github.com/DidierMorandi/gitdtl.git
cd gitdtl
python GitDTL.py
```

Aucune dépendance externe à installer.

---

## Lancement

```
python GitDTL.py
```

GitDTL s'ouvre sur le dossier courant. Le dossier de projet peut être changé à tout moment via le bouton **Changer de projet**.

---

## Fonctionnalités

| N° | Action | Commande Git équivalente |
|----|--------|--------------------------|
| 1 | État du projet | `git status` |
| 2 | Voir les modifications | `git diff` |
| 3 | Ajouter un fichier au projet | `git add` |
| 4 | Enregistrer un fichier modifié | `git add` |
| 5 | Supprimer un fichier du projet | `git rm` |
| 6 | Valider les changements | `git commit` |
| 7 | Publier le projet sur GitHub | `git push` |
| 8 | Créer une version | `git tag` + `git push` |
| 9 | Historique des versions | `git log` |
| 10 | Synchroniser depuis GitHub | `git pull` |
| 11 | Diagnostic GitDTL | `git status` + branche + remote + dernier commit |
| 12 | Lire le journal | Affichage du fichier `logs/gitdtl.log` |

### Comportements notables

**Initialisation automatique du dépôt.** Si le dossier courant ne contient pas encore de dépôt Git, GitDTL propose de l'initialiser (`git init`) avant d'exécuter toute opération.

**Configuration du remote.** Si aucun remote `origin` n'est configuré au moment de publier, GitDTL demande l'URL du dépôt GitHub et l'enregistre automatiquement.

**Gestion de l'upstream.** Lors du premier `git push` sur une nouvelle branche, GitDTL détecte l'absence d'upstream et exécute automatiquement `git push --set-upstream origin <branche>`.

**Suppression de fichier.** Deux options sont proposées : supprimer le fichier du disque et du suivi Git, ou le retirer uniquement du suivi Git en l'ajoutant dans `.gitignore`.

**Avertissement avant publication.** Si des fichiers modifiés ne sont pas encore inclus dans un commit, GitDTL les liste et demande confirmation avant d'exécuter `git push`.

**Création de version.** La fonction "Créer une version" enchaîne automatiquement : commit de version, création d'un tag annoté (`vX.Y.Z`), push du commit, push du tag.

**Journal applicatif.** Chaque action Git et chaque erreur sont enregistrées dans `logs/gitdtl.log` avec horodatage. Le journal peut être consulté, effacé ou exporté depuis l'interface.

**Aide contextuelle.** Chaque boîte de dialogue expose un bouton **? pour Aide** qui affiche une explication de l'opération en cours. Les textes d'aide peuvent être personnalisés via un fichier `aide.md` placé dans le même dossier que le script.

---

## Personnalisation de l'aide

Créer ou modifier un fichier `aide.md` dans le répertoire de GitDTL avec des sections nommées par clé :

```markdown
## commit_message

Décrivez brièvement la modification apportée.
Exemple : Correction du calcul de l'en-tête HTML.

## release_version

Indiquez le numéro de version au format X.Y.Z.
Le préfixe v sera ajouté automatiquement.
```

Les clés disponibles sont : `create_git_repository`, `remove_file_action`, `commit_message`, `release_version`, `release_confirmation`, `clear_log`, `publish_with_uncommitted_changes`, `github_remote_url`.

Si le fichier est absent ou si une clé n'est pas définie, le texte d'aide par défaut intégré au script est utilisé.

---

## Structure du projet

```
gitdtl/
├── GitDTL.py       Script principal
├── aide.md         Textes d'aide personnalisés (optionnel)
└── logs/
    └── gitdtl.log  Journal applicatif (créé automatiquement)
```

---

## Licence

MIT — voir le fichier `LICENSE`.

---

*In Memoriam Jean-Claude BELLAMY (1937-2015)*

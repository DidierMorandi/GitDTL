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
| 1 | État du projet : que faire maintenant ? | `git status` |
| 2 | Voir les modifications | `git diff` |
| 3 | Ajouter un fichier au projet | `git add` |
| 4 | Enregistrer un fichier modifié | `git add` |
| 5 | Supprimer un fichier ou un dossier | `git rm` |
| 6 | Valider les changements | `git commit` |
| 7 | Publier le projet sur GitHub | `git push` |
| 8 | Créer une version | `git tag` + `git push` |
| 9 | Historique des versions | `git log` |
| 10 | Synchroniser depuis GitHub | `git pull` |
| 11 | Diagnostic technique du dépôt | `git status` + branche + remote + dernier commit |
| 12 | Lire le journal | Affichage du fichier `logs/gitdtl.log` |
| 13 | Voir le projet dans GitHub | Ouvre la page GitHub configurée |
| 14 | Documentation | Affiche ce README en Markdown |
| 15 | Commande magique : GitScan | Scanne un dossier choisi et affiche le bilan des dépôts Git détectés |
| 16 | Cloner un dépôt GitHub | `git clone` |

### Comportements notables

**Initialisation automatique du dépôt.** Si le dossier courant ne contient pas encore de dépôt Git, GitDTL propose de l'initialiser (`git init`) avant d'exécuter toute opération.

**Configuration du remote.** Si aucun remote `origin` n'est configuré au moment de publier, GitDTL demande l'URL du dépôt GitHub et l'enregistre automatiquement.

**Gestion de l'upstream.** Lors du premier `git push` sur une nouvelle branche, GitDTL détecte l'absence d'upstream et exécute automatiquement `git push --set-upstream origin <branche>`.

**Suppression de fichier.** Deux options sont proposées : supprimer le fichier du disque et du suivi Git, ou le retirer uniquement du suivi Git en l'ajoutant dans `.gitignore`.

**Avertissement avant publication.** Si des fichiers modifiés ne sont pas encore inclus dans un commit, GitDTL les liste et demande confirmation avant d'exécuter `git push`.

**Guidage visuel.** Après une première activation, GitDTL met l'option 1 en surbrillance au lancement afin d'encourager le réflexe `git status`. Lorsque l'état du projet signale des éléments non validés, l'étape suivante est également suggérée : option 4 pour enregistrer les fichiers, ou option 6 si les changements sont déjà prêts à être validés. Après une publication réussie, GitDTL met l'option 13 en surbrillance pour ouvrir le projet dans GitHub.

**Commande envoyée.** Une ligne discrète en bas de l'écran affiche la dernière commande Git réellement lancée par GitDTL. Le libellé reste en police normale, tandis que la commande est affichée en monospace vert DTL. Cette ligne est masquée tant qu'aucune commande Git n'a été envoyée, et elle est effacée lorsqu'une option sans commande Git est sélectionnée.

**Exécution silencieuse sous Windows.** Les commandes Git sont lancées sans ouvrir de fenêtre console parasite, y compris lors d'un `git push`.

**Git du matin.** Un script compagnon peut afficher à l'ouverture de session Windows un petit bilan des dépôts Git détectés : modifications à enregistrer, changements à valider, commits à publier et temps estimé. Il s'appuie sur `DTLGitMorning.ps1`, lancé discrètement par `DTLGitMorning.vbs` via un raccourci placé dans le dossier de démarrage Windows. Le scan est en lecture seule : il utilise l'état Git local et ne modifie aucun dépôt. Pour tester sans redémarrer, lancez `DTLGitMorning.vbs`. Pour désactiver ce rappel, supprimez simplement le raccourci `DTL Git du matin.lnk` dans le dossier de démarrage Windows.

**Création de version.** La fonction "Créer une version" enchaîne automatiquement : commit de version, création d'un tag annoté (`vX.Y.Z`), push du commit, push du tag.

**Journal applicatif.** Chaque action Git et chaque erreur sont enregistrées dans `logs/gitdtl.log` avec horodatage. Le journal peut être consulté, effacé ou exporté depuis l'interface.

**Aide contextuelle.** Chaque boîte de dialogue expose un bouton **? pour Aide** qui affiche une explication de l'opération en cours. Les textes d'aide peuvent être personnalisés via un fichier `aide.md` placé dans le même dossier que le script.

**Système expert.** Les messages Git non prévus par l'interface peuvent être enrichis par des conseils issus de règles placées dans `expert_git.md`.

**Bienvenue première utilisation.** Au premier lancement, GitDTL affiche un écran de bienvenue dont le texte vient de la section `welcome` de `aide.md`. Un cookie local `.gitdtl_welcome_seen` évite de réafficher cet écran ensuite.

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

Les clés disponibles sont : `create_git_repository`, `remove_file_action`, `commit_message`, `release_version`, `release_confirmation`, `clear_log`, `publish_with_uncommitted_changes`, `github_remote_url`, `clone_repository_url`.

Si le fichier est absent ou si une clé n'est pas définie, le texte d'aide par défaut intégré au script est utilisé.

## Personnalisation du système expert

Créer ou modifier un fichier `expert_git.md` dans le répertoire de GitDTL.
Chaque règle contient des fragments de messages Git à reconnaître et un conseil à afficher :

```markdown
## Branche sans upstream

Patterns:
- has no upstream branch
- --set-upstream

Advice:
La branche locale n'est pas encore reliée à sa branche GitHub.
GitDTL peut corriger ce cas avec git push --set-upstream origin <branche>.
```

---

## Structure du projet

```
gitdtl/
├── GitDTL.py       Script principal
├── aide.md         Textes d'aide personnalisés (optionnel)
├── expert_git.md   Règles du système expert (optionnel)
└── logs/
    └── gitdtl.log  Journal applicatif (créé automatiquement)
```

---

## Licence

MIT — voir le fichier `LICENSE`.

---

*In Memoriam Jean-Claude BELLAMY (1937-2015)*

# GitDTL v1.0.0

8 juin 2026 - Didier DTL Morandi - https://didiermorandi.com/netdtl/

**Menu simplifié pour la gestion de projets avec Git**

GitDTL est une interface graphique Windows pour la gestion quotidienne de projets Git, conçue pour les utilisateurs qui souhaitent travailler avec Git sans passer par la ligne de commande.

---

## Présentation

GitDTL est une application de bureau Python/Tkinter qui expose les opérations Git essentielles sous forme d'un menu numéroté. Elle peut être utilisée sur n'importe quel dépôt local, même s'il n'existe pas encore. Dans ce cas, l'outil propose de le créer.

L'interface adopte l'esthétique « terminal DEC VT100 » de la suite NetDTL : fond noir, texte vert phosphore et police monospace Courier New.

---

## Prérequis

- Windows 10 ou supérieur
- Python 3.10 ou supérieur
- Git installé et disponible dans le `PATH` Windows

GitDTL utilise uniquement des modules standards de Python : `tkinter`, `subprocess`, `pathlib` et `shutil`.

---

## Installation

```powershell
git clone https://github.com/DidierMorandi/gitdtl.git
cd gitdtl
python GitDTL.py
```

Aucune dépendance externe n'est nécessaire.

---

## Lancement

```powershell
python GitDTL.py
```

GitDTL s'ouvre sur le dossier courant. Le dossier de projet peut être changé à tout moment avec le bouton **Changer de projet**.

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
| 12 | Lire le journal | Affichage de `logs/gitdtl.log` |
| 13 | Voir le projet dans GitHub | Ouvre la page GitHub configurée |
| 14 | Documentation | Affiche ce README en Markdown |
| 15 | Commande magique : GitScan | Scanne un dossier et affiche le bilan des dépôts détectés |
| 16 | Cloner un dépôt GitHub | `git clone` |
| 17 | Publier une Release GitHub sans kit | tag local + publication GitHub sans kit d'installation |
| 18 | Créer un kit et publier une Release GitHub | PyInstaller si besoin + ZIP + manuels + publication GitHub |

### Comportements notables

**Initialisation automatique.** Si le dossier courant ne contient pas encore de dépôt Git, GitDTL propose `git init`.

**Configuration du remote.** Si aucun remote `origin` n'est configuré au moment de publier, GitDTL demande l'URL du dépôt GitHub et l'enregistre.

**Gestion de l'upstream.** Lors du premier push sur une nouvelle branche, GitDTL détecte l'absence d'upstream et lance `git push --set-upstream origin <branche>`.

**Suppression de fichier.** Deux options sont proposées : supprimer le fichier du disque et du suivi Git, ou le retirer uniquement du suivi Git en l'ajoutant à `.gitignore`.

**Avertissement avant publication.** Si des fichiers modifiés ne sont pas encore inclus dans un commit, GitDTL les liste et demande confirmation avant le push.

**Assistant de validation.** Avant de créer un commit, GitDTL analyse les changements indexés, affiche un résumé des éléments détectés et propose un message au format Conventional Commits. L'utilisateur peut accepter ce message, le modifier avec le texte proposé prérempli, ou saisir un tout autre message.

**Guidage visuel.** GitDTL met en évidence les prochaines actions utiles après lecture de l'état Git.

**Commande envoyée.** Une ligne discrète affiche la dernière commande Git réellement exécutée.

**Exécution silencieuse.** Les commandes Git sont lancées sans fenêtre console parasite sous Windows.

**Git du matin.** Un script compagnon peut afficher à l'ouverture de session Windows un résumé des dépôts Git détectés : modifications à enregistrer, changements à valider, commits à publier et temps estimé.

**Création de version.** La fonction enchaîne commit de version, tag annoté `vX.Y.Z`, push du commit et push du tag.

**Publication d'une Release GitHub sans kit.** L'option 17 part d'un tag local existant. Elle ne crée pas de tag et ne prépare pas de kit d'installation. GitDTL vérifie que le dépôt est propre, que `origin` pointe vers GitHub, que le tag existe localement et qu'aucune Release GitHub ne porte déjà ce tag. GitDTL pousse le tag si nécessaire, puis crée la Release avec GitHub CLI `gh`.

**Création d'un kit et publication d'une Release GitHub.** L'option 18 exécute la chaîne complète : compilation avec PyInstaller lorsqu'un fichier `.spec` existe, création du ZIP, ajout du Manuel de référence et du Guide utilisateur dans le dossier `documentation\` du ZIP, puis publication GitHub. Elle utilise un tag local existant et refuse de publier si le dépôt n'est pas propre ou si une Release GitHub existe déjà pour ce tag.

**Journal applicatif.** Chaque action Git et chaque erreur sont enregistrées dans `logs/gitdtl.log`. Le journal peut être consulté, effacé ou exporté depuis l'interface.

**Aide contextuelle.** Chaque boîte de dialogue expose un bouton d'aide. Les textes peuvent être personnalisés dans `aide.md`.

**Système expert.** Les messages Git inattendus peuvent être enrichis par des conseils issus de règles dans `expert_git.md`.

**Bienvenue première utilisation.** Au premier lancement, GitDTL affiche un écran de bienvenue. Un fichier `.gitdtl_welcome_seen` évite de le réafficher ensuite.

---

## Personnalisation de l'aide

Créer ou modifier `aide.md` dans le dossier GitDTL avec des sections nommées :

```markdown
## commit_message

Décrivez brièvement la modification apportée.
Exemple : Correction du calcul de l'en-tête HTML.

## release_version

Indiquez le numéro de version au format X.Y.Z.
Le préfixe v sera ajouté automatiquement.
```

Clés disponibles : `create_git_repository`, `remove_file_action`, `commit_message`, `release_version`, `release_confirmation`, `clear_log`, `publish_with_uncommitted_changes`, `github_remote_url`, `clone_repository_url`.

Si le fichier ou une clé manque, le texte d'aide intégré est utilisé.

## Personnalisation du système expert

Créer ou modifier `expert_git.md` dans le dossier GitDTL. Chaque règle contient des fragments de messages Git à reconnaître et un conseil à afficher :

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

```text
gitdtl/
├── GitDTL.py       Script principal
├── aide.md         Textes d'aide personnalisés
├── expert_git.md   Règles du système expert
└── logs/
    └── gitdtl.log  Journal applicatif
```

---

## Licence

MIT - voir le fichier `LICENSE`.

---

*In Memoriam Jean-Claude BELLAMY (1937-2015)*

## Mise à jour - 14 juin 2026

Le code courant annonce `APP_VERSION = "v1.0-15"` dans `GitDTL.py`.

Nouveautés confirmées :

- Fenêtre d'accueil au premier lancement, mémorisée par un petit fichier local.
- Détection plus intelligente du dossier projet initial.
- Conseils experts chargés depuis les règles locales quand elles sont disponibles.
- Mise en évidence des prochaines actions utiles après lecture de l'état Git.
- Proposition d'ajouter les dossiers Python courants à `.gitignore` lorsqu'ils apparaissent non suivis.
- `GitScan` découvre les dépôts Git sous un dossier racine et affiche un résumé synthétique.
- L'option de clonage GitHub détecte le dossier cloné et propose de le gérer immédiatement.
- Journal local consultable, effaçable ou exportable depuis l'interface.
- Documentation HTML `GitDTL_Manuel_Utilisateur.html` présente dans le dépôt.

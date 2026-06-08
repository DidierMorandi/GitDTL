# Système expert GitDTL

Chaque règle commence par un titre `##`.
Ne changez librement que les motifs et les conseils si vous voulez ajuster les réponses.

Format attendu :

```text
## Nom de la règle

Patterns:
- fragment de message git
- autre fragment possible

Advice:
Texte affiché à l'utilisateur.
```

Les règles ci-dessous sont inspirées des chapitres de Pro Git sur le cycle `working tree -> staging area -> commit`, les remotes, les branches de suivi et `.gitignore`.

## Aucun dépôt distant configuré

Patterns:
- no configured push destination
- git remote add

Advice:
Git ne connaît pas encore l'adresse GitHub du projet.

Dans GitDTL, utilisez l'option 7 : l'outil demandera l'adresse du dépôt GitHub et configurera automatiquement le remote `origin`.

Règle déduite de Pro Git : un projet local doit connaître un dépôt distant avant de pouvoir pousser ses commits.

## Branche sans upstream

Patterns:
- has no upstream branch
- --set-upstream

Advice:
La branche locale n'est pas encore reliée à sa branche GitHub.

GitDTL sait corriger ce cas automatiquement avec :

`git push --set-upstream origin <branche>`

Règle déduite de Pro Git : une branche locale peut suivre une branche distante ; cette relation est l'upstream.

## Rien à valider

Patterns:
- nothing to commit
- working tree clean

Advice:
Il n'y a plus de changement local à valider.

L'étape suivante logique est de publier avec l'option 7, ou simplement de revenir au menu.

Règle déduite de Pro Git : `git commit` ne crée un commit que si des changements sont présents dans la staging area.

## Push refusé par avance distante

Patterns:
- failed to push some refs
- fetch first
- non-fast-forward

Advice:
Le dépôt GitHub contient probablement des changements absents du dossier local.

Commencez par l'option 10 pour synchroniser depuis GitHub, puis relancez la publication.

Règle déduite de Pro Git : avant de pousser, la branche locale doit pouvoir avancer proprement la branche distante.

## Authentification GitHub refusée

Patterns:
- authentication failed
- permission denied
- could not read from remote repository

Advice:
GitHub refuse l'accès au dépôt distant.

Vérifiez l'adresse du remote, le compte GitHub utilisé, et l'authentification HTTPS ou SSH.

Règle déduite de Pro Git : les remotes peuvent être accessibles en HTTPS ou SSH, mais les droits d'accès restent nécessaires.

## Fichier introuvable pour Git

Patterns:
- pathspec
- did not match any file

Advice:
Git ne trouve pas le fichier demandé.

Vérifiez que le fichier existe encore dans le dossier du projet, puis relancez l'action.

Règle déduite de Pro Git : les commandes Git agissent sur des chemins connus du working tree ou de l'index.

## Dépôt Git absent

Patterns:
- not a git repository
- any of the parent directories

Advice:
Le dossier courant n'est pas encore un dépôt Git.

Dans GitDTL, choisissez l'option 1 : l'outil proposera de créer le dépôt avec `git init`.

Règle déduite de Pro Git : un dossier devient un dépôt Git seulement après `git init` ou `git clone`.

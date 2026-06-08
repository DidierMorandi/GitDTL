# Aide GitDTL

Modifiez librement les textes sous chaque titre `##`.
Ne changez pas les titres `## create_git_repository`, `## remove_file_action`, etc. : GitDTL les utilise pour retrouver le bon texte d'aide.

## create_git_repository

Un projet Git permet de suivre un historique de la gestion de ses fichiers. L'utilitaire Git permet aussi de déposer un projet sur le site GitHub.

Choisissez 'Créer le projet Git' pour lancer une commande 'git init' dans le dossier courant.
Choisissez 'Annuler' pour revenir au menu sans créer de dépôt.

## remove_file_action

Le premier choix supprime le fichier du disque et de l'environnement Git.

Le deuxième choix conserve le fichier dans le dossier, le retire seulement du suivi Git et l'ajoute dans un fichier spécial .gitignore pour qu'il ne soit plus pris en compte par Git.

Annuler ne modifie rien.

## commit_message

Cette description est un message inclus dans le processus de validation (commit).

Elle doit expliquer brièvement ce qui vient de changer, par exemple :
- Ajout d'un logo
- Correction de la procédure de suppression des fichiers
- Mise à jour de l'interface principale

## release_version

Indiquez le numéro de version à publier.

Exemples : 1.0.0, 1.1.0, 2.0.0.
GitDTL ajoutera automatiquement le préfixe v pour créer un tag Git.

## release_confirmation

Une version crée un point de repère officiel dans l'historique Git.

GitDTL va créer un commit, poser un tag de version, puis publier le tout sur le site de GitHub (https://github.com/)
Utilisez cette action uniquement quand la version est prête à être conservée.

## clear_log

Le journal contient les actions et erreurs enregistrées par GitDTL.

Effacer le journal vide le fichier de log courant, mais ne modifie pas le projet Git.

## publish_with_uncommitted_changes

Publier envoie le projet vers un dépôt GitHub préalablement configuré sur le site github.com.

Si des fichiers ne sont pas validés dans un commit, ils ne feront pas partie de la version publiée. Il est souvent préférable d'ajouter les fichiers puis de valider les changements avant de publier.

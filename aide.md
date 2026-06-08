# Aide GitDTL

Modifiez librement les textes sous chaque titre `##`.
Ne changez pas les titres `## create_git_repository`, `## remove_file_action`, etc. : GitDTL les utilise pour retrouver le bon texte d'aide.

## welcome

# Bienvenue dans GitDTL

GitDTL vous accompagne dans les opérations Git courantes sans passer par la ligne de commande.

Pour démarrer :
- choisissez ou vérifiez le dossier du projet courant ;
- utilisez l'option 1 pour connaître l'état du projet ;
- suivez les options mises en surbrillance ambre pour avancer dans le bon ordre.

Cet écran de bienvenue ne s'affiche qu'à la première utilisation.

## create_git_repository

Un projet Git permet de suivre un historique de la gestion de ses fichiers. L'utilitaire Git permet aussi de déposer un projet sur le site GitHub.

Choisissez 'Créer le projet Git' pour lancer une commande 'git init' dans le dossier courant.
Choisissez 'Annuler' pour revenir au menu sans créer de dépôt.

## remove_file_action

Le premier choix supprime l'élément du disque et de l'environnement Git.

Le deuxième choix conserve l'élément dans le dossier, le retire seulement du suivi Git et l'ajoute dans un fichier spécial .gitignore pour qu'il ne soit plus pris en compte par Git.

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

Les fichiers affichés dans cette alerte existent dans le dossier, mais ne sont pas encore inclus dans une validation Git.

Si vous publiez maintenant, les changements déjà validés seront envoyés sur GitHub, mais ces fichiers resteront uniquement sur votre ordinateur.

Il est souvent préférable d'ajouter les fichiers puis de valider les changements avant de publier.

## github_remote_url

Git a besoin de connaître l'adresse du dépôt GitHub où publier le projet.

Créez d'abord un dépôt vide sur GitHub, puis copiez son URL.

Exemples :
- https://github.com/compte/projet.git
- git@github.com:compte/projet.git

## common_python_ignores

Ces dossiers sont produits automatiquement par Python ou par GitDTL.

Les ajouter à .gitignore évite qu'ils apparaissent dans les fichiers non suivis.

## stage_modified_files

Cette action lance git add sur les fichiers modifiés déjà connus de Git et sur les nouveaux fichiers non suivis.

Elle prépare ces changements pour la prochaine validation.

# GitDTL v1.0.0

GitDTL est un utilitaire Windows qui rend Git plus accessible aux administrateurs système débutants.

Sa devise :

> Git pour l'administrateur système débutant.

## Objectif

GitDTL masque les commandes Git courantes derriere des actions simples :

- ajouter un fichier
- modifier un fichier
- supprimer un fichier
- publier
- créer une version
- consulter l'historique
- diagnostiquer le dépôt
- lire le journal des operations

## Plateforme

- Windows 10
- Windows 11
- Python 3.10 ou version supérieure
- Git installé et disponible dans le PATH Windows

## Lancement

Depuis le dossier du projet :

```powershell
python GitDTL.py
```

Au démarrage, GitDTL utilise le dossier courant comme projet Git. Le bouton **Changer de projet** permet de choisir un autre dossier.

## Journal

GitDTL cree automatiquement :

```text
logs\gitdtl.log
```

Le journal conserve les opérations réalisées et les commandes Git exécutées, avec date et heure.

## Securite

- Une confirmation est demandée avant la suppression d'un fichier.
- Une confirmation est demandée avant la création d'une version.
- Avant chaque publication, GitDTL vérifie l'état du dépôt avec Git et avertit si des fichiers ne sont pas encore validés.

## Livrables

- `GitDTL.py`
- `README.md`
- `Manuel_utilisateur.html`
- `LICENSE`

## Licence

MIT.

# Timeline Relationmap Manager

Timeline Relationmap Manager

Ce projet est un gestionnaire de timeline en relationmap. Il permet de créer, gérer et organiser des projets en enregistrant leurs répertoires dans un fichier JSON. L'application offre une interface graphique intuitive pour ajouter, visualiser, modifier et supprimer des projets.

## Fonctionnalités principales

Ajout de projets : Permet d'ajouter un nouveau projet en spécifiant son nom et son répertoire.
Visualisation des projets : Affiche la liste des projets enregistrés avec leurs détails (nom, répertoire, date d'ajout).
Actions sur les projets :
Voir les détails : Affiche les informations détaillées d'un projet.
Modifier : Permet de modifier les informations d'un projet (à implémenter).
Supprimer : Supprime un projet après confirmation.
Gestion des répertoires : Crée automatiquement les répertoires et fichiers nécessaires pour stocker les données des projets.

## Fonctionnement actuel

L'application crée automatiquement un fichier JSON (project_directories.json) pour enregistrer les projets.
Les projets sont affichés dans une liste avec des boutons d'action pour interagir avec eux.
L'interface est responsive et stylisée pour une expérience utilisateur agréable.


## Utilisation

Installation :
Assurez-vous d'avoir Python 3 installé sur votre système.
Clonez ce dépôt ou téléchargez les fichiers.
Exécution :
Exécutez le script main.py avec la commande suivante :
python3 main.py en terminal dans le repertoire de son emplacement.
Interface :
Utilisez l'interface graphique pour ajouter, visualiser, modifier ou supprimer des projets.
Fichiers

## file: project_directories.json

-main.py : Script principal pour lancer l'interface de gestionnaire.
-project_directories.json : Fichier JSON pour enregistrer les répertoires de projet.
-setup.py : Script pour initialiser les répertoires et fichiers nécessaires.
Contributeurs

Eric Murray Lavoie
Licence

Ce projet est open source et distribué gratuitement à la communauté sous licence MIT. Vous êtes libre de l'utiliser, de le modifier et de le partager selon les termes de la licence.

Comment contribuer

Forkez ce dépôt.
Créez une branche pour vos modifications (git checkout -b feature/nouvelle-fonctionnalité).
Committez vos changements (git commit -m 'Ajouter une nouvelle fonctionnalité').
Poussez vos modifications (git push origin feature/nouvelle-fonctionnalité).
Ouvrez une Pull Request.
Remarques

Ce projet est en cours de développement. Les fonctionnalités peuvent évoluer rapidement.
N'hésitez pas à ouvrir des issues ou à proposer des améliorations via des Pull Requests.
# Timeline-Relationmap-Manager

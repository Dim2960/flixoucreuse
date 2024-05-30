# Système de recommandation de film
![Flixoucreuse](https://github.com/Dim2960/img/flixoucreuse.png)

## Description
Bienvenue sur le dépôt GitHub de notre projet de groupe réalisé pendant notre formation en Data Analyse avec la World code School. Ce projet a été mené par Aikel, Victoria et moi dans le cadre de notre cursus, et il porte sur la création d'un système de recommandation de films.

Le projet s'est déroulé en plusieurs étapes :

* Analyse des Données : Explorer les données pour identifier les tendances et les caractéristiques des films (acteurs les plus présents, période de sortie, durée des films, âge des acteurs, etc.).
* Jointures et Nettoyage : Effectuer des jointures entre les datasets, nettoyer les données et rechercher des corrélations.
* Système de Recommandation : Utiliser des algorithmes de machine learning pour recommander des films en fonction de ceux appréciés par le spectateur.
* Affichage et Interface : Afficher les recommandations et les KPI sur une interface utilisateur, ainsi que des images de films récupérées depuis une base complémentaire de TMDB.

## Table des matières
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Membres du projet](#membres)
- [Remerciements](#remerciements)

## Installation

1. Clonez le dépôt:
    ```sh
    git clone https://github.com/Dim2960/flixoucreuse.git
    ```
2. Allez dans le répertoire du projet:
    ```sh
    cd flixoucreuse
    ```
3. Installez les dépendances:
    ```sh
    pip install -r requirements.txt
    ```
4. Ajouter la clé API tmdb pour utilisation en local:  
  
   Copier votre clé API tmdb dans le fichier api.txt

5. Lancer l'application en local:
    ```sh
    streamlit run index.py
    ```
    

## Observation

* Pour voir le nettoyage, l'exploration, visualisation des données , ouvrez les notebooks correspondants dans Jupyter ou Google Colab : [Notebook](https://github.com/Dim2960/flixoucreuse/exploration_visualisation).
* Pour un exemple de l'application ouvrez à partir de l'url suivante : [appli-streamlit](https://flixoucreuse.streamlit.app/)

## Membres du projet

[victoria-1989](https://github.com/victoria-1989)  
[charaabi01](https://github.com/charaabi01)  
[Dim2960](https://github.com/Dim2960)

## Remerciements

- Merci à [Romain Lejeune](https://github.com/Vaelastraszz) pour l'aide apportée durant ce projet.

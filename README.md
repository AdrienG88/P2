# P2 Webscraping Project for OpenClassrooms


## Contenu du projet:

1 fichier requirements.txt

2 scripts Python indépendants


## Mode d'emploi:

1.  Pour créer l'environnement virtuel nécessaire au fonctionnement des scripts:

      a.Entrez la commande suivante dans la console pour créer un environnement virtuel à partir du module venv:
      
        python -m venv <nom-souhaité-de-l-environnement>
      
      
      b.Grâce à la commande suivante, activez l'environnement virtuel (sous Windows):
      
        <nom-souhaité-de-l-environnement>\Scripts\activate.bat
        
        
      c.Entrez la commande suivante dans la console pour installer les modules et paquets nécessaires dans l'environnement virtuel actif:
      
        pip install -r P2_00_requirements.txt


2.  Exécutez le script P2_01_scrape_cat_urls.py

Ce script va automatiquement prélever toutes les url des différentes catégories de livres du site bookstoscrape.com, et les enregistrer dans un fichier nommé all_categories_urls.csv


3.  Exécutez le script P2_02_scrape_all_book_info.py \n

    Saisissez l'url d'une catégorie issue du fichier all_categories_urls.csv comme demandé dans le script.

A partir de cette url, le script va automatiquement récupérer toutes les informations sur l'ensemble des livres de la catégorie choisie du site bookstoscrape.com, et les consigner dans un fichier <nom-de-la-catégorie>.csv

# P2 Webscraping Project for OpenClassrooms


## Contenu du projet:

1 fichier requirements.txt

1 fichier Python contenant le code-source du programme

1 fichier README.me contenant la marche à suivre pour faire fonctionner le programme.


## Mode d'emploi:

1.  Pour créer l'environnement virtuel nécessaire au fonctionnement des scripts:

      a.Entrez la commande suivante dans la console pour créer un environnement virtuel à partir du module venv:
      
        python -m venv <nom-souhaité-de-l-environnement>
      
      
      b.Grâce à la commande suivante, activez l'environnement virtuel (sous Windows):
      
        <nom-souhaité-de-l-environnement>\Scripts\activate.bat
        
        
      c.Entrez la commande suivante dans la console pour installer les modules et paquets nécessaires dans l'environnement virtuel actif:
      
        pip install -r requirements.txt



2.  Exécutez le script P2_01_scrape_bookstoscrape_website.py avec Python

Dans la console, entrez la commande suivante pour exécuter le programme :

      python P2_01_scrape_bookstoscrape_website.py


Ce script va automatiquement prélever toutes les url des différentes catégories de livres du site bookstoscrape.com, et les enregistrer dans un fichier nommé all_categories_urls.csv

Pour chaque url de catégorie, le script va automatiquement récupérer toutes les informations sur l'ensemble des livres de la catégorie choisie du site bookstoscrape.com, les consigner dans un fichier <nom-de-la-catégorie>.csv, et télécharger toutes les couvertures de livres dans un dossier <nom-de-la-catégorie>.

L'ensemble des données est consigné dans un dossier BooksToScrape_Data situé dans le même dossier que le script exécuté.



# projet_IA Client 3
Projet IA A3

# Notebook
Le modele sauvegarder en .pkl est le model du "model_client_3_bestmodel.ipynb"

Les autres modele utilisé sont dans le "client_3_autre_model.ipynb"

La version du modele avec un apprentissage sur des données reduite (essouche / non essouche) dans le "model_client_3_base_reduite.ipynb"





# Scirpt
##  Faire attention d'etre dans le dossier du client 3 pour lancer le script et qu'il puisse lire les fichiers

## Lancement script python pour la carte:
Avoir les librairies : pandas, folium, pickle, branca, requests, datetime, sys


## Commandes :

python map_client3.py (date format : year-day-month) (fichier pickle) (fihcier json)
exemple :

python map_client3.py 2010-02-28 dic_client_3.pkl data.json
return : map.html contenant la carte pour le client 3


## Les tests on était réaliset avec python 3.12:

python3.12 map_client3.py 2010-02-28 dic_client_3.pkl data.json 
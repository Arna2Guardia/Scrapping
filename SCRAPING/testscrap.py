import json
import requests

headers = {
    'Apollographql-Client-Name': 'Iron',
    'App-Version': '2023.01.29.00',
    'App-Platform': 'Iron',
    'Accept-Language': 'fr-FR',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36',
    'X-Stockx-Device-Id': 'jsui_1_bot_mdr'
}

id_chaussure = 'nike-dunk-low-grey-fog'
#On charge notre data depuis notre json (les données dans la requête post)
with open("data.json", "r") as file:
    data = json.load(file)

#Notre paramètre pour le modele de chaussure
data['variables']['id'] = id_chaussure

# On fait notre requete post
response = requests.post("https://stockx.com/api/p/e", json=data, headers=headers)

#On deffini notre objet json

datajson = response.json()

#On prends uniquement les données de la réponse qui nous intéressent
liste_taille = datajson['data']['product']['variants']

#On se retrouve donc avec un liste python, facilement traitable
print(liste_taille[1])

for i in range(len(liste_taille)):
    element = liste_taille[i]
    interesting = element['market']['bidAskData']
    prix_bas = interesting['highestBid']
    taille = interesting['highestBidSize']
    # prix_haut = interesting['']
    if interesting['lowestAsk'] == 'None':
        prix_haut = prix_bas
    else:
        prix_haut = interesting['lowestAsk']
    nb_demande = interesting['numberOfAsks']
    print('Pour la taille ' + str(taille) + ' US.')
    print('Le prix max est de ' + str(prix_haut) + "$.")
    print('Et le prix le plus bas de ' + str(prix_bas) + "$.")
    print('Il y a actuellement ' + str(nb_demande) + ' demandes pour cette taille et ce modèle.\n')

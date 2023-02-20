import requests
import bs4
import time
import csv
import json


baseUrl = 'https://stockx.com'
uri = '/fr-fr/sneakers?page='

headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
  "Accept-Language": "en-US,en;q=0.8",
  "Referer": "https://stockx.com/",
  "Origin": "https://stockx.com",
  "Connection": "keep-alive",
  "Cache-Control": "no-cache"
}

response = requests.get(baseUrl + uri, headers=headers)

def endpointsCollector():
  webpoints = []

  for i in range(1,25):
    webpoints.append(baseUrl + uri + str(i))
  endpoints = []
  idChaussures = []
  for webpoint in webpoints:
    response = requests.get(webpoint, headers=headers)
    if response.ok:
      swoup = bs4.BeautifulSoup(response.text,'html.parser')
      id = swoup.find('div', {"id": "browse-grid"})
      divs = swoup.findAll('div', {"class": "css-1ibvugw-GridProductTileContainer"})
      for div in divs:
          a = div.find('a')
          endpoints.append(baseUrl + a['href'])
          id = a['href']
          id = id.replace('/fr-fr/','')
          idChaussures.append(id)
  return endpoints, idChaussures



print(response) 

headers3 = {
    'Apollographql-Client-Name': 'Iron',
    'App-Version': '2023.01.29.00',
    'App-Platform': 'Iron',
    'Accept-Language': 'fr-FR',
    'User-Agent': 'myUserAgent2/0',
    'X-Stockx-Device-Id': 'jsui_1_bot_mdr'
}

_, idChaussures = endpointsCollector()
#print(idChaussures)

with open("data.json", "r") as file:
    data = json.load(file)

for idChaussure in idChaussures:
  data['variables']['id'] = idChaussure

  response2 = requests.post("https://stockx.com/api/p/e", json=data, headers=headers3)
  if response2.status_code != 200:
    print('Request failed with status code:', response2.status_code)
  else:
    datajson = response2.json()
    print(datajson)
    try:
      listeTaille = datajson['data']['product']['variants']
    except TypeError:
      print(f"Error processing idChaussure: {idChaussure}")
      pass

    for i in range(len(listeTaille)):
      element = listeTaille[i]
      interesting = element['market']['bidAskData']
      prixBas = interesting['highestBid']
      taille = interesting['highestBidSize']
      if interesting['lowestAsk'] == 'None':
          prixHaut = prixBas
      else:
          prixHaut = interesting['lowestAsk']
      nbDemande = interesting['numberOfAsks']
      print('Pour la taille ' + str(taille) + ' US.')
      print('Le prix max est de ' + str(prixHaut) + "$.")
      print('Et le prix le plus bas de ' + str(prixBas) + "$.")
      print('Il y a actuellement ' + str(nbDemande) + ' demandes pour cette taille et ce modèle.\n')
      time.sleep(1)
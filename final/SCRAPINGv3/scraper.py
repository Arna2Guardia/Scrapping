import requests
import bs4
import time
import csv
import json


baseUrl = 'https://stockx.com'
uri = '/fr-fr/sneakers?page='

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.8",
    "Accept": "text/html",
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
  nameChaussures = []
  for webpoint in webpoints:
    response = requests.get(webpoint, headers=headers)
    if response.ok:
      swoup = bs4.BeautifulSoup(response.text,'html.parser')
      id = swoup.find('div', {"id": "browse-grid"})
      divs = swoup.findAll('div', {"class": "css-1ibvugw-GridProductTileContainer"})
      for div in divs:
          a = div.find('a')
          name = div.find('p', {"class": "css-3lpefb"})
          name = name.contents[0]
          #print(name)
          endpoints.append(baseUrl + a['href'])
          id = a['href']
          id = id.replace('/fr-fr/','')
          idChaussures.append(id)
          nameChaussures.append(name)
  return endpoints, idChaussures, nameChaussures


print(response) 


#             try:
#               price = price.contents[0]
#               intPrice = int(price.replace('\xa0€',''))
#               print("Link:", baseUrl + a['href'])
#               print("Price:", price)
#               endpoints.append([baseUrl + a['href'], price.replace(u'\xa0', ' ')])
#               new = requests.get(baseUrl + a['href'], headers=headers)

#               if new.ok:
#                 swoup2 = bs4.BeautifulSoup(new.text,'html.parser')
#                 lastSellAll = swoup2.find('p', {'class': 'css-xfmxd4'})
#                 lastSellAll = lastSellAll.contents[0]
#                 intLastSellAll = int(lastSellAll.replace('\xa0€',''))                
#                 res = intPrice - intLastSellAll

#                 try:
#                   difference = swoup2.findAll('p', {'class': 'css-eqh2n0'})
#                   print('Last sell:', lastSellAll, '\n')
#                   cpt = 0
#                   for dif in difference:
#                     if cpt == 0:
#                       print('Difference between 2 last sales:', dif.contents[0], '\n')
#                     else:
#                       print(dif.contents[0], '\n')
#                     cpt +=1
#                 except:
#                   print("Class css-eqh2n0 not found")
#                   pass

#                 try:
#                   difference = swoup2.findAll('p', {'class': 'css-as46lx'})
#                   #print('Last sell:', lastSellAll, '\n')
#                   cpt = 0
#                   for dif in difference:
#                     if cpt == 0:
#                       print('Difference between 2 last sales:', dif.contents[0], '\n')
#                     else:
#                       print(dif.contents[0], '\n')
#                     cpt +=1
#                 except:
#                   print('Class css-as46lx not found')
#                   pass
              
#                 try:
#                   difference = swoup2.findAll('p', {'class': 'css-1qumzfe'})
#                   #print('Last sell:', lastSellAll, '\n')
#                   cpt = 0
#                   for dif in difference:
#                     if cpt == 0:
#                       print('Difference between 2 last sales:', dif.contents[0], '\n')
#                     else:
#                       print('+',dif.contents[0], '\n')
#                     cpt +=1
#                 except:
#                   print('Class css-1qumzfe not found')
#                   pass
              



#             except:
#               pass

#             time.sleep(1)
#     #print('\nL id est:', id)
    

headers3 = {
    'Apollographql-Client-Name': 'Iron',
    'App-Version': '2023.01.29.00',
    'App-Platform': 'Iron',
    'Accept-Language': 'fr-FR',
    'User-Agent': 'myUserAgent2/0',
    'X-Stockx-Device-Id': 'jsui_1_bot_mdr'
}

_, idChaussures, _ = endpointsCollector()
#print(idChaussures)

with open("data.json", "r") as file:
  data = json.load(file)


allInfo = []
cpt = 0

# boucle sur chaque chaussure
for idChaussure in idChaussures:

  data['variables']['id'] = idChaussure

  response2 = requests.post("https://stockx.com/api/p/e", json=data, headers=headers3)
  if response2.status_code != 200:
    print('Request failed with status code:', response2.status_code)
  else:
    datajson = response2.json()
    #print(datajson)
    try:
      listeTaille = datajson['data']['product']['variants']
    except TypeError:
      print(f"Error processing idChaussure: {idChaussure}")
      pass

    # boucle sur chaque pointure
    obj = {}
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
      obj[str(taille)] = [prixBas, prixHaut, nbDemande]

      # print('Pour la taille ' + str(taille) + ' US.')
      # print('Le prix max est de ' + str(prixHaut) + "$.")
      # print('Et le prix le plus bas de ' + str(prixBas) + "$.")
      # print('Il y a actuellement ' + str(nbDemande) + ' demandes pour cette taille et ce modèle.\n')
      time.sleep(0.8)
      print("Tout va bien")
    allInfo.append(obj)
    cpt+=1
    print(cpt)
    if cpt == 20:
      break
    print("petite pause")
    time.sleep(20)
  

rows = []
end, _, name = endpointsCollector()
for i in range(len(allInfo)):
  rowsBuilder = {}
  rowsBuilder["id"] = i
  rowsBuilder["name"] = name[i]
  rowsBuilder["link"] = end[i]
  for key, value in allInfo[i].items():
    rowsBuilder[key] = value

  rows.append(rowsBuilder)

headers2 = ["id","name","link","1","1.5","2","2.5","3","3.5","4","4.5","5","5.5","6",
            "6.5","7","7.5","8","8.5","9","9.5","10","10.5",
            "11","11.5","12","12.5","13","13.5","14","14.5",
            "15","15.5","16","16.5","17","17.5","18",'13W / 11.5M',
            '5W / 3.5M', '7W / 5.5M', '6W / 4.5M', '8.5W / 7M', '10W / 8.5M', '5.5W / 4M', '8W / 6.5M',
            '11W / 9.5M', '10.5W / 9M', '6.5W / 5M', '9.5W / 8M',
            '14W / 12.5M', '16.5W / 15M', '15.5W / 14M', '12W / 10.5M',
            '13.5W / 12M', '7.5W / 6M', '12.5W / 11M', '11.5W / 10M', '14.5W / 13M', '9W / 7.5M',
            "3.5 2E wide", "4 2E wide", "4.5 2E wide", "5 2E wide", "5.5 2E wide", "6 2E wide", "6.5 2E wide",
            "7 2E wide", "7.5 2E wide", "8 2E wide", "8.5 2E wide", "9 2E wide", "9.5 2E wide", "10 2E wide",
            "10.5 2E wide", "11 2E wide", "11.5 2E wide", "12 2E wide", "12.5 2E wide","13 2E wide", "13.5 2E wide",
            "14 2E wide", "14.5 2E wide", "15 2E wide", "15.5 2E wide", "16 2E wide", "16.5 2E wide", "17 2E wide", "17.5 2E wide", "18 2E wide","None",
            "1 2E", "1.5 2E", "2 2E", "2.5 2E", "3.5 2E", "4 2E", "4.5 2E", "5 2E", "5.5 2E", "6 2E", "6.5 2E",
            "7 2E", "7.5 2E", "8 2E", "8.5 2E", "9 2E", "9.5 2E", "10 2E",
            "10.5 2E", "11 2E", "11.5 2E", "12 2E", "12.5 2E","13 2E", "13.5 2E",
            "14 2E", "14.5 2E", "15 2E", "15.5 2E", "16 2E", "16.5 2E", "17 2E", "17.5 2E", "18 2E"]


with open("all_data.csv", 'w', newline="") as file:
    writer = csv.DictWriter(file, fieldnames=headers2)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

print('Done')
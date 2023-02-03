import requests
import bs4
import time
import csv

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


print(response) 

if response.ok:
    webpoints = []

    for i in range(1,25):
        webpoints.append(baseUrl + uri + str(i))
    #print(webpoints)  

    endpoints = []
    for webpoint in webpoints:
        response = requests.get(webpoint, headers=headers)
        if response.ok:
          swoup = bs4.BeautifulSoup(response.text,'html.parser')
          #print(swoup.prettify())
          id = swoup.find('div', {"id": "browse-grid"})
          divs = swoup.findAll('div', {"class": "css-1ibvugw-GridProductTileContainer"})
          for div in divs:
            a = div.find('a')
            price = div.find('p',{"class": "css-9ryi0c"})
            #print(a)
            #price = price.contents[0]
            # int_price = int(price.replace('\xa0€',''))
            # print("LE PRIX EST: \n", int_price)

            try:
              price = price.contents[0]
              intPrice = int(price.replace('\xa0€',''))
              print("Link:", baseUrl + a['href'])
              print("Price:", price)
              endpoints.append([baseUrl + a['href'], price.replace(u'\xa0', ' ')])
              #print(endpoints)
              new = requests.get(baseUrl + a['href'], headers=headers)
              #print(new)

              if new.ok:
                swoup2 = bs4.BeautifulSoup(new.text,'html.parser')
                lastSellAll = swoup2.find('p', {'class': 'css-xfmxd4'})
                lastSellAll = lastSellAll.contents[0]
                intLastSellAll = int(lastSellAll.replace('\xa0€',''))                
                #print('INTLASTSELLALL IS \n:', intLastSellAll)
                res = intPrice - intLastSellAll
                #print(res)

                try:
                  difference = swoup2.findAll('p', {'class': 'css-eqh2n0'})
                  print('Last sell:', lastSellAll, '\n')
                  cpt = 0
                  for dif in difference:
                    if cpt == 0:
                      print('Difference between 2 last sales:', dif.contents[0], '\n')
                    else:
                      print(dif.contents[0], '\n')
                    cpt +=1
                except:
                  print("Class css-eqh2n0 not found")
                  pass

                try:
                  difference = swoup2.findAll('p', {'class': 'css-as46lx'})
                  #print('Last sell:', lastSellAll, '\n')
                  cpt = 0
                  for dif in difference:
                    if cpt == 0:
                      print('Difference between 2 last sales:', dif.contents[0], '\n')
                    else:
                      print(dif.contents[0], '\n')
                    cpt +=1
                except:
                  print('Class css-as46lx not found')
                  pass
              
                try:
                  difference = swoup2.findAll('p', {'class': 'css-1qumzfe'})
                  #print('Last sell:', lastSellAll, '\n')
                  cpt = 0
                  for dif in difference:
                    if cpt == 0:
                      print('Difference between 2 last sales:', dif.contents[0], '\n')
                    else:
                      print('+',dif.contents[0], '\n')
                    cpt +=1
                except:
                  print('Class css-1qumzfe not found')
                  pass
              



            except:
              pass

            time.sleep(2)
    #print('\nL id est:', id)
    
rows = []
for i in range(len(endpoints)):
  rows.append({
    "id": i,
    "category": "None",
    "link": endpoints[i]
  })

headers = ["id","category","link"]

with open('endpointsList.csv', 'w', newline="") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

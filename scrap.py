import requests
import bs4
import time

baseUrl = 'https://stockx.com'
uri = '/fr-fr/sneakers'


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
    swoup = bs4.BeautifulSoup(response.text,'html.parser')
    #print(swoup.prettify())
    id = swoup.find('div', {"id": "browse-grid"})
    divs = swoup.findAll('div', {"class": "css-1ibvugw-GridProductTileContainer"})
    for div in divs:
      a = div.find('a')
      price = div.find('p',{"class": "css-9ryi0c"})
      #print(a)

      try:
        print("Link:", baseUrl + a['href'])
        print("Price:", price.contents[0])
        new = requests.get(baseUrl + a['href'], headers=headers)
        #print(new)

        if new.ok:
          swoup2 = bs4.BeautifulSoup(new.text,'html.parser')
          #print(swoup2.prettify())
          bdm = swoup2.find('button', attrs= {"id": 'menu-button-pdp-size-selector'})
          bdm['aria-expanded'] = "true"
          print(bdm)
          ddm = swoup2.find('div', attrs= {"class": 'css-r6z5ec'})
          ddm['style'] = "visibility: visible; min-width: max-content; --popper-transform-origin: top left; position: absolute; inset: 0px auto auto 0px; margin: 0px; transform: translate(1048px, 284px); width: 428px;"
          print(ddm)
          grid_price = swoup2.find('div', attrs= {"id": 'menu-list-pdp-size-selector'})
          grid_price['style'] = "transform-origin: var(--popper-transform-origin); opacity: 1; visibility: visible; transform: none;"
          print(grid_price)
          prices_size = swoup2.findAll('button', {"class": "css-10ur78r"})
          print(prices_size)

          for but in prices_size:
            div_price = but.find('div', {"class": "css-1pulpde"})
            pointure = but.find('div', {"class": "css-nszg6y"})

            try:
              print('Price for:',pointure,' is:',div_price)

            except:
              print('ça marche pas fdp')
              pass

      except:
        pass

      time.sleep(5)
    #print('\nL id est:', id)

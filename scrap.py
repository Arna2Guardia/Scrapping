import requests
import bs4

baseUrl = 'https://stockx.com'
uri = 'nike'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}


response = requests.get(baseUrl + uri, headers=headers)

print(response)

if response.ok:
    swoup = bs4.BeautifulSoup(response.text,'html.parser')
    ol = swoup.find('ol', {"class": "trackingContainer"})
    lis = swoup.findAll('li')
    #for li in lis:
        #a = li.find('a')
        #print(a)
        #try:
        #   print(baseUrl + a['href'])
        #except:
        #    pass

    print(ol)


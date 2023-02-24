import requests
import bs4
import random
import csv
import math


baseUrl = "https://www.leagueofgraphs.com"
uri = "/rankings/summoners/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.leagueofgraphs.com',
    'Origin': 'https://www.leagueofgraphs.com'
}

response = requests.get(baseUrl + uri,headers=headers)
print(response)
soup = bs4.BeautifulSoup(response.text,'html.parser')



def getPages(url, nbPages):
    linkPages = []
    for i in range(1,nbPages):
        linkPages.append(url + "page-" + str(i))
    return linkPages

# print(getPages(baseUrl + uri,51))

def getPageEndpoints(soup,url):
    table = soup.find("table", {"class":"summonerRankingsTable"})
    trs = table.findAll("tr")
    endpoints = []
    for tr in trs:
        a = tr.find('a')
        if a is not None and str(url + a['href']) != "https://www.leagueofgraphs.com/rankings/summoners":
            try:
                endpoints.append(url + a['href'])
            except:
                pass

    return endpoints

def allEndPoints(url,pages):
    endPoints = []
    for page in pages:
        response = requests.get(page, headers=headers)  
        soup = bs4.BeautifulSoup(response.text,'html.parser')  
        endPoints += getPageEndpoints(soup,url)  
    return endPoints


pages = getPages(baseUrl + uri, 51)
response = requests.get(baseUrl + uri, headers=headers)
soup = bs4.BeautifulSoup(response.text, 'html.parser')
endPoints = allEndPoints(baseUrl, pages)
#print(endPoints)


def swoup(url, headers, process):

    response = requests.get(url, headers=headers)
    if response.ok:

        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        try:
            return process(soup)
        except Exception:
            print("ERROR: Impossible to process ! On :" + str(url))
            return False
    else:
        print("ERROR: Failed Connect on :" + str(url))
        return False 



def fileWriter(file, fieldnames, data):
    with open(file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        cpt = 1  

        for endpoint in data:
            endpoint['ID'] = cpt  
            writer.writerow(endpoint)
            cpt += 1 

fieldnames = ["ID", "Links"]  
data_links = [{"Links": links} for links in allEndPoints(baseUrl,getPages(baseUrl + uri, 51))] 
fileWriter("links.csv", fieldnames, data_links)


def getInfoByPage(soup):
    name = soup.find("title").contents[0].replace(" - LeagueOfGraphs",'')
    print(name)
    sumRanking = soup.find("div",{"class":"summoner-rankings"})
    if sumRanking is not None:
        soloq = sumRanking.find("div",{"class":"best-league"})
        flexq = sumRanking.find("div",{"class":"other-league"})
        if soloq is not None:
            soloqRank = soloq.find("div",{"class":"leagueTier"}).contents[0].strip()
            nbLps = soloq.find("span",{"class":"leaguePoints"}).contents[0].strip()
            worldRank = soloq.find("span", {"class":"highlight"}).contents[0].strip()
            regionalRank = soloq.find("a", {"class":"regionalRank"}).contents[0].strip()
            nbWins = soloq.find("span", {"class":"winsNumber"}).contents[0].strip()
            nbLoses = soloq.find("span", {"class":"lossesNumber"}).contents[0].strip()
            # print(soloqRank)
            # print(nbLps)
            # print(worldRank)
            # print(regionalRank)
            # print("Wins:", nbWins + ' | ' + "Losses:",nbLoses)

        if flexq is not None:
            flexqRank = flexq.find("div",{"class":"leagueTier"}).contents[0].strip()
            # print(flexqRank)

    champsGrid = soup.find("table",{"class":"sortable_table"})
    champs = champsGrid.findAll("tr")
    champInfos = []
    for champ in champs:
        champColumn = champ.find("td",{"class":"champColumn"})

        if champColumn is not None:
            champName = champColumn.find("div",{"class":"name"}).contents[0].strip()
            champGlobalRank = champColumn.find("span",{"class":"top-rank"})
            games = champColumn.find_next_sibling("td")
            if champGlobalRank is not None:
                champGlobalRank = champGlobalRank.contents[0].strip()
            champRegionalRank = champColumn.find("span",{"class":"regionalRank"})
            if champRegionalRank is not None:
                champRegionalRank = champRegionalRank.contents[0].strip()
            kda = [champColumn.find("span",{"class":"kills"}).contents[0].strip(),champColumn.find("span",{"class":"deaths"}).contents[0].strip(),champColumn.find("span",{"class":"assists"}).contents[0].strip()]
            # print(champName)
            # print("World Rank:",champGlobalRank,"Regional Rank:",champRegionalRank)
            # print("K/D/A:",kda)

            if games is not None:
                gamesP = games.find("progressbar")
                if gamesP is not None:
                    gamesPlayed = gamesP["data-value"]

            relative = champ.find("td",{"class":"relative"})
            if relative is not None:
                champWr = relative.find("progressbar")
                if champWr is not None:
                    winrateOnChamp = champWr["data-value"]
                    if len(winrateOnChamp) > 4:
                        winrateOnChamp = winrateOnChamp[0:4]
                    # print("Winrate on " + champName + ": " + winrateOnChamp  + " for : " + gamesPlayed + " game(s) played")
                else:
                     print("Winrate on " + champName + " not found.")
            champInfos.append([champName,champGlobalRank,champRegionalRank,kda,gamesPlayed,winrateOnChamp])

    rolesGrid = soup.find("div",{"id":"profileRoles"})
    roles = rolesGrid.findAll("tr")
    rolesInfo = []
    cpt = 0
    for role in roles:
        if cpt <= math.ceil(len(roles)/4):
            try:
                playerRole = role.find("td").find("div", {"class": "txt name"}).text.strip()
                gamesPlayedRole = role.findAll("td")[1]['data-sort-value']
                winrateRole = role.findAll("td")[2]['data-sort-value']
                if len(winrateRole) > 4:
                    winrateRole = winrateRole[0:4]
                # print(playerRole + ":", gamesPlayedRole + "game(s) played, ", winrateRole)
                cpt = cpt + 1
                rolesInfo.append([playerRole,gamesPlayedRole,winrateRole])
            except:
                cpt = cpt + 1
                pass
                
        else:
            break

    player = {
        "Name": name,
        "Rank SoloQ": soloqRank,
        "LP SoloQ": nbLps,
        "World Ranking": worldRank,
        "Regional Ranking": regionalRank,
        "Wins": nbWins,
        "Losses": nbLoses,
        "Rank FlexQ": flexqRank,
        "Champions Info": champInfos,
        "Roles Info": rolesInfo,
    }
    return player


def fileWriter(file, fieldnames, data):
    with open(file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        cpt = 1  

        for endpoint in data:
            endpoint['ID'] = cpt  
            writer.writerow(endpoint)
            cpt += 1 

allData = []
j = 0
for i in endPoints:
    #  if j > 10:
    #      break
    #  else:
        try:
            response2 = requests.get(i,headers=headers)
            soup2 = bs4.BeautifulSoup(response2.text,'html.parser')
            allData.append(getInfoByPage(soup2))
            j = j + 1
        except:
            print("Error on:", i)
            
print("Done")
print(allData)

fieldnames2 = ["ID","Name", "Rank SoloQ", "LP SoloQ", "World Ranking", "Regional Ranking", "Wins", "Losses", "Rank FlexQ", "Champions Info", "Roles Info"]
fileWriter("INFO_PLAYER.csv", fieldnames2, allData)
    


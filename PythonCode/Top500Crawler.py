from urllib.request import urlopen
from bs4 import BeautifulSoup
import googlemaps

def getLocInfo(url):
    soup = BeautifulSoup(urlopen(url))
    tableRows = soup.find('table', class_='table table-condensed').findAll("tr")[2:]
    city = str(tableRows[0].findAll('td')[0].text).strip()
    country = str(tableRows[1].findAll('td')[0].text).strip()
    if country == "Korea, South": country = "South Korea"
    return (city,country)

def getCoordinates(city,country):
    gmaps = googlemaps.Client(key='AIzaSyAoihuxdW93Jm1eRtqMJK_VhQrSma2RrzM')
    geocode_result = gmaps.geocode(city+", "+country)
    lat = str(geocode_result[0]['geometry']['location']['lat']).strip()
    lng = str(geocode_result[0]['geometry']['location']['lng']).strip()
    return (lat,lng)

def getSpecsInfo(url):
    soup = BeautifulSoup(urlopen(url))
    tableRows = soup.find('table', class_='table table-responsive').findAll("tr")
    manufacturer = str(tableRows[1].findAll('td')[3].text).strip().replace(",","-")
    coresCount = str(tableRows[1].findAll('td')[4].text).strip().replace(",","")
    rMax = str(tableRows[1].findAll('td')[5].text).strip().replace(",","")
    rPeak= str(tableRows[1].findAll('td')[6].text).strip().replace(",","")
    power= str(tableRows[1].findAll('td')[7].text).strip().replace(",","")
    if power == "":
        power = "N/A"
    return (manufacturer,coresCount,rMax,rPeak,power)

outputFile = open('top500.csv', 'a')
#Writing Header Row
outputFile.write("Rank,Name,City,Country,Lat,Lng,Manufacturer,Cores,Rmax,Rpeak,Power")
url = 'https://www.top500.org/list/2017/11/?page=1'


page = urlopen(url)
#print(page)
soup = BeautifulSoup(page)
table = soup.find('table', class_='table table-condensed table-striped')

for (rank, row) in enumerate(table.findAll("tr")[1:], start=1):
    print("Rank: ", rank)
    #First, getting the city and country
    cells = row.findAll('td')
    url_1 = "https://www.top500.org" + str(cells[1].findAll("a")[0]["href"])
    name = str(cells[1].findAll("a")[0].text).replace(",","-")
    (city, country) = getLocInfo(url_1)
    (lat,lng) = getCoordinates(city, country)
    #Second, getting specs
    url_2="https://www.top500.org" + str(cells[2].findAll("a")[0]["href"])
    (manufacturer, coresCount, rMax, rPeak, power) = getSpecsInfo(url_2)
    #print(manufacturer, coresCount, rMax, rPeak, power)
    outputFile.write("\n" + str(rank) + "," + name
                     + "," + city + "," +country
                     + "," + lat + "," + lng
                     + "," + manufacturer + "," + coresCount
                     + "," + rMax + "," + rPeak + "," + power)
outputFile.close()
print("End of Crawling!")

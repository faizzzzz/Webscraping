from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup


def findCars():
    minPrice = str(2500)
    maxPrice = str(4000)
    maxMiles = str(175000)

    # secondPage = "s=120%"
    numCarsPerPage = 120
    pages = 5

    filename = "car_info.csv"

    delPrev = open(filename, 'w')
    delPrev.truncate(0)
    delPrev.close()

    for page in range(1,(pages + 1)):
        myURL = 'https://dallas.craigslist.org/search/cto?' + 's=' + str(page*numCarsPerPage) + '&min_price=' + minPrice + '&max_price=' + maxPrice + '&max_auto_miles=' + maxMiles
        req = Request(myURL, headers={'User-Agent':'Mozilla/5.0'})
        uClient = uReq(myURL)
        pageHTML = uClient.read()
        uClient.close()     ### IMPORTANT ###

        page_soup = soup(pageHTML, 'html.parser')

        vehicle_list = page_soup.findAll('li', {'class':'result-row'})

        cars = 0
        # Creating a .csv file
        file = open(filename, 'a')

        headers = "Name, price, location, time, link\n"
        file.write("Page: " + str(page) + "\n")
        file.write("Search Criteria:\n" + "MinPrice: " + minPrice + "\nMaxPrice: " + maxPrice + "\nMaxMiles: " + maxMiles + "\n\n")
        file.write(headers)
        file.close()

        for vehicle in vehicle_list:
            car_info = open(filename, 'a')
            # name
            name = vehicle.p.a.text

            # price
            vehiclePrice = vehicle.p.findAll('span', {'class':'result-price'})[0].text
            # location, some vehicles don't have a location
            try:
                vehicleLocation = vehicle.p.findAll('span', {'class':'result-hood'})
                vehicleLocation = vehicleLocation[0].text

            except:
                vehicleLocation = 'location not given'

            # time
            timePosted = vehicle.p.time['datetime']

            # link
            siteName = 'https://dallas.craigslist.org/'
            link = vehicle.a['href']
            completeLink = siteName + link
            cars += 1
            try:    # This replace the comma from the names. If this is not removed it messes up the excel sheet
                car_info.write(name.replace(',','|') + "," + vehiclePrice + "," + vehicleLocation.replace(',','|') + "," + timePosted + "," + completeLink + "\n")
                car_info.close()
            except: # Some car names don't have commas
                car_info.write("No name" + "," + vehiclePrice + "," + vehicleLocation.replace(',','|') + "," + timePosted + "," + completeLink + "\n")
                car_info.close()

        print("page: " + str(page))

findCars()



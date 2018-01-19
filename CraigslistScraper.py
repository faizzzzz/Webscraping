from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup


def findCars(lprice, mprice, miles, pages):
    minPrice = str(lprice)
    maxPrice = str(mprice)
    maxMiles = str(miles)

    # secondPage = "s=120%"
    numCarsPerPage = 120

    filename = "car_info.csv"
    
    # deleting on the previous file
    delPrev = open(filename, 'w')
    delPrev.truncate(0)
    delPrev.close()

    # writing on the file
    file = open(filename, 'a')
    headers = "Name, price, location, time, link\n"
    # file.write("Search Criteria:\n" + "MinPrice: " + minPrice + "\nMaxPrice: " + maxPrice + "\nMaxMiles: " + maxMiles + "\n\n")
    file.write(headers)
    file.close()
    

    for page in range(1,(pages + 1)):
        myURL = 'https://dallas.craigslist.org/search/cto?' + 's=' + str(page*numCarsPerPage) + '&min_price=' + minPrice + '&max_price=' + maxPrice + '&max_auto_miles=' + maxMiles
        req = Request(myURL, headers={'User-Agent':'Mozilla/5.0'})
        uClient = uReq(myURL)
        pageHTML = uClient.read()
        uClient.close()     ### IMPORTANT ###

        page_soup = soup(pageHTML, 'html.parser')

        vehicle_list = page_soup.findAll('li', {'class':'result-row'})

        cars = 0
        
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
            completeLink = link
            cars += 1
            try:    # This replace the comma from the names. If this is not removed it messes up the excel sheet
                car_info.write(name.replace(',','|') + "," + vehiclePrice + "," + vehicleLocation.replace(',','|') + "," + timePosted + "," + completeLink + "\n")
                car_info.close()
            except: # Some car names don't have commas
                car_info.write("No name" + "," + vehiclePrice + "," + vehicleLocation.replace(',','|') + "," + timePosted + "," + completeLink + "\n")
                car_info.close()
        # car_info.close()
        print("page: " + str(page))

if __name__ == "__main__":
    findCars(2500, 4000, 175000, 5)     # findCars(minPrice, maxPrice, maxMiles, numPages)
    # one page on craigslist list 120 cars, so 5 pages will list 5*120 = 600 cars.



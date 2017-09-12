import xml.etree.cElementTree as ET
import csv 
import requests
import pandas as pd

URL = "http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml"

response = requests.get(URL)
with open('feed.xml', 'wb') as file:
    file.write(response.content)

tree = ET.ElementTree(file='feed.xml')
root = tree.getroot()


Listing_data = open('ListingData.csv', 'w')


csvwriter = csv.writer(Listing_data)
listing_head = []
count = 0

for member in root.findall('Listing'):
    listing = []
    appliance_list = []
    rooms_list = []
    #Set Headers for Columns
    if count == 0:
        mlsID = member[1].find('MlsId').tag
        listing_head.append(mlsID)
        mlsName = member[1].find("MlsName").tag
        listing_head.append(mlsName)
        dateListed = member[1].find("DateListed").tag
        listing_head.append(dateListed)
        streetAddress = member[0][0].tag
        listing_head.append(streetAddress)
        price = member[1][1].tag
        listing_head.append(price)
        bedrooms = member[3][3].tag
        listing_head.append(bedrooms)
        bathrooms = member[3][4].tag
        listing_head.append(bathrooms)
        appliances = member[10][1].tag
        listing_head.append(appliances)
        listing_head.append("Rooms")
        listing_head.append("Description")
        csvwriter.writerow(listing_head)
        count = count + 1
    dateListed = member[1][6].text
    dateListed = dateListed[0:4]
    desc = member[3][2].text
    desc = desc[0:200]
    #check for listing to be made in 2016 as 
    #well as having 'and' within the description
    #If conditions are met than write the specified columns to csv
    if dateListed == '2016' and desc.find("and") != -1:    
        mlsID = member[1][3].text
        listing.append(mlsID)
        mlsName = member[1][4].text
        listing.append(mlsName)
        dateListed = member[1][6].text
        dateListed = dateListed[0:10]
        listing.append(dateListed)
        streetAddress = member[0][0].text
        listing.append(streetAddress)
        price = member[1][1].text
        listing.append(price)
        bedrooms = member[3][3].text
        listing.append(bedrooms)
        bathrooms = member[3][4].text
        listing.append(bathrooms)
        #list appliances
        for i in range(len(member[10][1])):
            appliance = member[10][1][i].text
            appliance_list.append(appliance)
        listing.append(appliance_list)
        #list rooms
        for i in range(len(member[10][39])):
            rooms = member[10][39][i].text
            rooms_list.append(rooms)
        listing.append(rooms_list)
        desc = member[3][2].text
        #limit description to 200 characters
        desc = desc[0:200]
        listing.append(desc)
        csvwriter.writerow(listing)
Listing_data.close()

#sort by date using pandas then rewrite csv 
data = pd.read_csv('ListingData.csv')
data['DateListed'] = pd.to_datetime(data['DateListed'], format = "%Y/%m/%d %H:%M")
data = data.sort_values(by='DateListed', ascending = False)
data = data.to_csv('ListingData.csv', index = False)

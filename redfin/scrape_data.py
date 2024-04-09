# scrape some data why dont we

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import pandas as pd
import time
import json

import pdb

aggregate = pd.read_csv('Apartment_List_Rent_Estimates_2024_03.csv')
cities = aggregate[aggregate['location_type'] == 'City']['location_name'].unique().tolist()
metros = aggregate[aggregate['location_type'] == 'Metro']['location_name'].unique().tolist()

driver = webdriver.Chrome()

action = webdriver.ActionChains(driver)

driver.implicitly_wait(2)

housing = pd.DataFrame(columns=['price', 'rooms', 'baths', 'square_feet', 'address'])

for city in cities:
    print(city)
    availability = pd.DataFrame(columns=housing.columns)
    # go to the home page
    driver.get('https://www.redfin.com/')
    time.sleep(5)

    #driver.get('https://apartments.com')
    #search_bar = driver.find_element(By.ID, 'quickSearchLookup')

    # search up a city
    search_bar = driver.find_element(By.ID, 'search-box-input')
    search_bar.send_keys(f'{city}')
    time.sleep(5)
    search_bar.send_keys(Keys.DOWN)
    time.sleep(5)
    search_bar.send_keys(Keys.ENTER)

    # scrape the list
    prices = driver.find_elements(By.CLASS_NAME, 'bp-Homecard__Price--value')
    rooms = driver.find_elements(By.CLASS_NAME, 'bp-Homecard__Stats--beds')
    baths = driver.find_elements(By.CLASS_NAME, 'bp-Homecard__Stats--beds')
    square_footage = driver.find_elements(By.CLASS_NAME, 'bp-Homecard__LockedStat--value')
    addresses = driver.find_elements(By.CLASS_NAME, 'bp-Homecard__Address')

    # # parse the object
    for (price, room, baths, square_feet, address) in zip(prices, rooms, baths, square_footage, addresses):
        row = [[price.text, room.text, baths.text, square_feet.text, address.text]]
        print(row)
        availability = pd.concat([availability, pd.DataFrame(row, columns=availability.columns)])

    
    totalPages = driver.find_element(By.CLASS_NAME, 'pageText').text[-1]
    print(totalPages)

    for i in range(0, 10):
        try:
            # get the next page
            next_btn = driver.find_element(By.CLASS_NAME, 'PageArrow__direction--next')
            next_btn.click()

        except:
            # no next button
            break

        try:
            # and save the results
            prices = driver.find_elements(By.CLASS_NAME, 'bp-Homecard__Price--value')
            rooms = driver.find_elements(By.CLASS_NAME, 'bp-Homecard__Stats--beds')
            baths = driver.find_elements(By.CLASS_NAME, 'bp-Homecard__Stats--beds')
            square_footage = driver.find_elements(By.CLASS_NAME, 'bp-Homecard__LockedStat--value')
            addresses = driver.find_elements(By.CLASS_NAME, 'bp-Homecard__Address')

            # if any of them have no elements, raise an exception
            if len(prices) == 0 or len(rooms) == 0 or len(addresses) == 0 or len(square_footage) == 0 or len(baths) == 0:
                raise Exception(f'Nontraditional listings found in {city}')
    
            # parse the object
            for (price, room, baths, square_feet, address) in zip(prices, rooms, baths, square_footage, addresses):
                row = [[price.text, room.text, baths.text, square_feet.text, address.text]]
                print(row)
                availability = pd.concat([availability, pd.DataFrame(row, columns=availability.columns)])


        except:
            continue



    # save the list of houses
    availability.to_csv(f'by_city/available_housing_{city.split(",")[0]}.csv', index=False)


    housing = pd.concat([housing, availability])
    
housing.to_csv('available_housing_expanded.csv', index=False)

driver.quit()
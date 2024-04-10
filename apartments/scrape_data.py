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

housing = pd.DataFrame(columns=['price', 'rooms', 'address'])

for city in cities:
    availability = pd.DataFrame(columns=housing.columns)
    # go to the home page
    driver.get('https://apartments.com')

    # search up a city
    search_bar = driver.find_element(By.ID, 'quickSearchLookup')
    search_bar.send_keys(f'{city}')
    time.sleep(1)
    search_bar.send_keys(Keys.DOWN)
    time.sleep(1)
    search_bar.send_keys(Keys.ENTER)

    # scrape the list
    prices = driver.find_elements(By.CLASS_NAME, 'property-pricing')
    rooms = driver.find_elements(By.CLASS_NAME, 'property-beds')
    addresses = driver.find_elements(By.CLASS_NAME, 'property-address')
    time.sleep(1)

    # parse the object
    for (price, room, address) in zip(prices, rooms, addresses):
        row = [[price.text, room.text, address.text]]
        availability = pd.concat([availability, pd.DataFrame(row, columns=availability.columns)])

    while True:
        try:
            # get the next page
            next_btn = driver.find_element(By.CLASS_NAME, 'next')
            next_btn.click()

        except:
            # no next button
            break

        try:
            # and save the results
            prices = driver.find_elements(By.CLASS_NAME, 'property-pricing')
            rooms = driver.find_elements(By.CLASS_NAME, 'property-beds')
            addresses = driver.find_elements(By.CLASS_NAME, 'property-address')

            # if any of them have no elements, raise an exception
            if len(prices) == 0 or len(rooms) == 0 or len(addresses) == 0:
                raise Exception(f'Nontraditional listings found in {city}')
    
            # parse the object
            for (price, room, address) in zip(prices, rooms, addresses):
                row = [[price.text, room.text, address.text]]
                availability = pd.concat([availability, pd.DataFrame(row, columns=availability.columns)])


        except:
            try:
                # this page actually has houses instead of apartments
                prices = driver.find_elements(By.CLASS_NAME, 'price-range')
                rooms = driver.find_elements(By.CLASS_NAME, 'bed-range')
                addresses = driver.find_elements(By.CLASS_NAME, 'property-address')
        
                # parse the object
                for (price, room, address) in zip(prices, rooms, addresses):
                    row = [[price.text, room.text, address.get_attribute('title')]]
                    availability = pd.concat([availability, pd.DataFrame(row, columns=availability.columns)])

                
            except:
                # ok now its actually broken
                continue



    # save the list of houses
    availability.to_csv(f'apartments/by_city/available_housing_{city.split(",")[0]}.csv', index=False)
    housing = pd.concat([housing, availability])
    
housing.to_csv('apartments/available_housing_expanded.csv', index=False)

driver.quit()
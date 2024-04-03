from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

#There are 3 sections: 
#1- Loading the given website and scraping store data 
#2- Clicking on 'cafe details' link to navigate to store address and scraping the address information
#3- Wrangling the data saved from the first 2 steps into a single, cleaned dataframe that can then be used to incorporate the review data and perform analytics



#STEP 1

#configuring webdriver
service = Service('/Users/austin/Downloads/chromedriver-mac-x64/chromedriver')
driver = webdriver.Chrome(service=service)

#go to lamadeleline webpage
driver.get(f'https://lamadeleine.com/locations')

#I use this time to manually zoom out on the map in browser (click the zoom out button on bottom right of page 8 times). This is needed to scrape ALL locations, not just the ones that show up as default
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.locationlist__wrapper')))

time.sleep(4)

#saving handle of original window, for use later
original_window = driver.current_window_handle

#navigating to elements I want to scrape
elements = driver.find_elements(By.CSS_SELECTOR, ".location__name, .location__phone")

#creating list to store scraped data 
elements_texts = []

#iterating through each element I want and printing
for element in elements:
    #print(element.text)
    elements_texts.append(element.text)

#iterating through text in my list and counting how many restaurants were scraped
print("Contents of elements_text", elements_texts)






# STEP 2


#initiate counter and list (counter will just help with debugging)
i = 1
locations = []
all_addresses = []
num_lines_per_address = 3
num_of_directions = len(driver.find_elements(By.CSS_SELECTOR, ".location__link"))

all_addresses = []
for index in range(num_of_directions):
    
    #re-find the "cafe details" links each iteration
    directions_links = driver.find_elements(By.CSS_SELECTOR, ".location__link")
    link = directions_links[index]

    #clicking on link to cafe details, wait for the new page to load, and then scrape the address information
    link.click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.address__information')))

    #resetting address list and locating elements
    addresses = []
    address_lines = driver.find_elements(By.CSS_SELECTOR, '.address__line__1, .address__line__2, .address__line__3')
    
    #appending findings to list
    for address_line in address_lines:
        address_text = address_line.text
        addresses.append(address_text)

    #if does not contain 3 items then pad the list to contain 3 items
    while len(addresses) < 3:
        addresses.append("")
    print(addresses)

    #adding address to the all_addresses list
    all_addresses.append(addresses)

    #navigating back to list of locations
    driver.back()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.location__link')))

#creating df from address scraping
address_df = pd.DataFrame(all_addresses, columns=['streetAddress1', 'streetAddress2', 'cityStateZip'])
print(address_df)

#create store_details list
store_details = [text.replace('\n', ', ') for text in elements_texts]
driver.quit()



# STEP 3
#I will use pandas to manipulate the data

chunks = []

#iterate over store details to group pairs (step of 2)
for i in range(0, len(store_details), 2):
    #ensuring there is a pair available
    if i + 1 < len(store_details):
        #appending to chunks
        chunks.append((store_details[i], store_details[i+1]))

#converting tuples into a pandas df
store_details_df = pd.DataFrame(chunks, columns=['locationName', 'phoneNumber'])

#fixing issues with blank columns in address_df
for index, row in address_df.iterrows():
    #check if cityStateZip column is empty for row
    if row['cityStateZip'].strip() == '':
        #adjust streetAddress1 to streetAddress2, and streetAddress2 to cityStateZip
        address_df.at[index, 'cityStateZip'] = row['streetAddress2']
        address_df.at[index, 'streetAddress2'] = row['streetAddress1']
        address_df.at[index, 'streetAddress1'] = ''  # Clearing the original streetAddress1

#splitting address_df into desired components
pattern = r'(?P<City>.*?),\s*(?P<State>[A-Z]{2})\s*(?P<PostalCode>\d{5})'

#extracting components
city_state_zip = address_df['cityStateZip'].str.extract(pattern)

#rename column
address_df.rename(columns={'streetAddress1': 'StreetAddress'}, inplace=True)

#concatenate new columns to original df
address_df = pd.concat([address_df.drop(columns=['cityStateZip']), city_state_zip], axis=1)

#combine streetAddress with streetAddress2 and drop residual column
address_df['StreetAddress'] = address_df.apply(lambda row: row['StreetAddress'] + (' ' + row['streetAddress2'] if row['streetAddress2'] else ''), axis=1)
address_df.drop('streetAddress2', axis=1, inplace=True)

#combine both dfs into 1
scraping_df = pd.concat([store_details_df, address_df], axis=1)

#uncomment below code to export as a csv
# file_path = '/Users/austin/Documents/BainCSV/scraped.csv'
# scraping_df.to_csv(file_path, index=False)
# file_path
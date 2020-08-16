from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml
import numpy as np
import time


# Webpage we're scraping
#base_url = "https://honolulu.craigslist.org/search/oah/sss?query=cars&sort=rel"
pages = np.arange(1, 360, 120)

# Dictionary to hold data
data = {
    'Title': [],
    'Price': []
}

for page in pages:
    # Send get http request
    page = requests.get("https://honolulu.craigslist.org/search/oah/sss?query=cars&s="+str(page)+"&sort=rel")
    # Verify successful get request
    if page.status_code == requests.codes.ok:
        # Get the whole page
        bs = BeautifulSoup(page.text, 'lxml')
    # Get all listings on this page
    containing_div = bs.find('div', class_='content')
    list_of_listings = containing_div.find('ul', class_='rows')
    all_postings = list_of_listings.find_all('li', class_='result-row')
    time.sleep(5)

    # loop through all postings to find data
    for posting in all_postings:
        # Get the title of the FIRST posting and add to dictionary
        title = posting.find('a', class_='result-title hdrlnk').text

        if title:
            data['Title'].append(title)
        else:
            data['Title'].append('N/A')

        # Get the price of the FIRST posting and add to dictionay
        price = posting.find('span', class_='result-price').text

        if price:
            data['Price'].append(price)
        else:
            data['Price'].append('N/A')


    # Store data to csv with pandas
    df = pd.DataFrame(data, columns=[
        'Title',
        'Price'])

    # Increase count column by 1 (rather than start at 0)
    df.index = df.index + 1
    #print(df)

# one liner for writing a csv file
df.to_csv('craigslist_postings_file.csv', sep=',', index=False, encoding='utf-8')


print("Code Completed")
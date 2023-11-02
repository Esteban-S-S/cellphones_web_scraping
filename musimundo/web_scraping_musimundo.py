import requests
from bs4 import BeautifulSoup as bs
import random
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc



browser = webdriver.Chrome() 

page_number = 0
ids_cell_phones = []


'''I execute the infinite while loop that will stop when it no longer detects any more pages 
with products within the loop, mainly the identifier of each cell phone will be obtained and 
it will be stored in ids_cell_phones.'''

while True:

    url = f'https://www.musimundo.com/telefonia/telefonos-celulares/c/82?q=%3Arelevance&page={page_number}'

    browser.get(url)

    time.sleep(random.randint(8,10))

    try:
        browser.find_element('xpath', '//*[@id="didomi-notice-agree-button"]').click()
    except:
        pass
        
    html = browser.page_source

    soup = bs(html , 'lxml')

    page_number += 1


    try:
        articles = soup.find('div', {'class':'productGrid clearfix'}).find_all('div',{'class': 'mus-pro-thumb'})
    except:
        break

    for article in articles:
        cell_phone_id = article.find('a').get('href')

        ids_cell_phones.append(cell_phone_id)

      
        print(article.find('a').get('href'))

ids_cell_phones = [phone for phone in ids_cell_phones if phone is not None]


musimundo_cell_phones = pd.Series()
critical_errors = 0

'''I define the function parce_cell_phones that takes a cell phone identifier 
as an argument and extracts detailed information about that phone from its individual page.'''

def parse_cell_phones(cell_phone_id):
    
    global critical_errors ## I indicate that 'serious_errors' is a global variable
    
    url = f'https://www.musimundo.com{cell_phone_id}'
    
    browser.get(url)

    time.sleep(random.randint(4,10))

    html = browser.page_source

    try:
        soup = bs(html, 'lxml')

        model = soup.find('div',{'class': 'productDetailsPanel mus-product-box'})\
                    .find('p',{'class':'mus-pro-name strong'})\
                    .text\
                    .replace('\n','')\
                    .replace('\t','')

        price = float(soup.find('span', {'class': 'mus-pro-price-number'})
                      .text
                      .replace('\n','')
                      .replace('$','')
                      .replace('.','')
                      .replace(',','.'))
        
        especifications = soup.find('div',{'id':'fichaTecnica'}).find_all('tr')
    
    except:
        critical_errors += 1
        return None
    
    '''I assign None to the variables because there are cases in which this data is not presented'''

    ram = None
    camera = None
    processor = None
    storege = None
    screen = None

    for div in especifications:
        momentary_text = div.text.lower()

        if 'ram' in momentary_text:
            try:
                ram = div.find('td', {'class':''}).text.replace('\n','').replace('\t','')
            except:
                pass

        elif 'camara principal' in momentary_text:
            try:
                camera = ' | Trasera: ' + div.find('td', {'class':''}).text.replace('\n','').replace('\t','')
            except:
                pass

        elif 'camara frontal' in momentary_text:
            try:
                camera = 'Frontal: ' + div.find('td', {'class':''}).text.replace('\n','').replace('\t','') + camera
            except:
                pass

        elif 'procesador' in momentary_text:
            try:
                processor = div.find('td', {'class':''}).text.replace('\n','').replace('\t','')
            except:
                pass

        elif 'almacenamiento' in momentary_text:
            try:
                storege = div.find('td', {'class':''}).text.replace('\n','').replace('\t','')
            except:
                pass
        
        elif 'tamaño de pantalla' in momentary_text:
            try:
                screen = div.find('td', {'class':''}).text.replace('\n','').replace('\t','')
            except:
                pass
        



    musimundo_cell_phones['model'] = model
    
    musimundo_cell_phones['price'] = price

    musimundo_cell_phones['ram'] = ram
    
    musimundo_cell_phones['processor'] = processor
    
    musimundo_cell_phones['storege'] = storege
    
    musimundo_cell_phones['camera'] = camera
    
    musimundo_cell_phones['screen'] = screen

    df_musimundo_cell_phones = pd.DataFrame(musimundo_cell_phones)

    return (df_musimundo_cell_phones.T)


'''I create a for loop to iterate through the cell phone identifiers, call the pare_cell_phones function with 
each identifier, and add the results to the df_musimundo_cell_phones DataFrame.'''

df_musimundo_cell_phones = pd.DataFrame()

for i in range(len(ids_cell_phones)):
    try:
        df_musimundo_cell_phones = pd.concat([df_musimundo_cell_phones, parse_cell_phones(ids_cell_phones[i])])
    except:
        pass
    
    if critical_errors > 10:
        print('It has more than 10 serious errors, if you want to stop the process press Ctrl + C')

    print(f'Progress {i+1} of {len(ids_cell_phones)}')

    time.sleep(random.randint(4,10))

browser.quit()

df_musimundo_cell_phones.to_csv('celulares_musimundo.csv', index = False)

print('Number of records obtained: ', len(df_musimundo_cell_phones))

print('Number of serious errors found: ', critical_errors)

print('Number of null data found: ',df_musimundo_cell_phones.isnull().sum().sum())

print('extraction completed')
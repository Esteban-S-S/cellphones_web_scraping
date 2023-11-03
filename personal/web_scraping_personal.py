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

page_number = 1
ids_cell_phones = []

'''I execute the infinite while loop that will stop when it no longer detects any more pages 
with products within the loop, mainly the identifier of each cell phone will be obtained and 
it will be stored in ids_cell_phones.'''

while True:
    url = f'https://tienda.personal.com.ar/celulares?page={page_number}'

    browser.get(url)

    time.sleep(random.randint(10,12))

    try:
        browser.find_element('xpath', '//*[@id="didomi-notice-agree-button"]').click()
    except:
        pass
    
    html = browser.page_source

    soup = bs(html , 'lxml')
    try:
        current_page = int(soup.find('div',{'class':'emsye86z'}).find('a',{'class':'emsye870 emsye871 emsye872'}).text)
    except:
        pass

    if page_number == current_page:
        articles = soup.find('div',{'class': 'emsye86a'})
    else:
        break

    page_number += 1

    for article in articles:
        cell_phone_id = article.get('href')

        ids_cell_phones.append(cell_phone_id)

        time.sleep(random.randint(1,3))

        print(cell_phone_id)


    ids_cell_phones = [phone for phone in ids_cell_phones if phone is not None]





personal_cell_phones = pd.Series()
critical_errors = 0

'''I define the function parce_cell_phones that takes a cell phone identifier 
as an argument and extracts detailed information about that phone from its individual page.'''

def parse_cell_phones(cell_phone_id):

    global critical_errors ## I indicate that 'critical_errors' is a global variable
    
    url = f'https://tienda.personal.com.ar{cell_phone_id}'
    #print('Dirección: ', url)

    browser.get(url)

    time.sleep(random.randint(4,10))

    html = browser.page_source

    soup = bs(html, 'lxml')

    try:
        model = soup.find('h1').text

        price = int(soup.find('div',{'class':'_1qzmwzw89 _1qzmwzw8c _1qzmwzw66 _1qzmwzw6g'})
                    .find('div',{'class':'emsye831'})
                    .text
                    .replace('$','')
                    .replace('.',''))
        
        '''As there are cases in which I do not obtain information about the ram from what was obtained in "highlighted_especifications"
        I create the variable more_specifications from which I do obtain that information.'''
                
        highlighted_especifications = soup.find('div',{'class': '_1qzmwzw8b _1qzmwzw1k _1qzmwzw6j _1qzmwzw89'}).find_all('div',{'class':'_1qzmwzw89 _1qzmwzw8b _1qzmwzw8c'})

        more_especifications = soup.find('div', {'class': 'emsye84e'}).find_all('div', {'class': '_1qzmwzw89 emsye84j'})
        
    except:
        critical_errors += 1        
        return None
    
    '''I assign None to the variables because there are cases in which this data is not presented'''
 
    ram = None
    camera = None
    processor = None
    storege = None
    screen = None
        
    for div in highlighted_especifications:
        momentary_text = div.find('div',{'class':'emsye846'}).text.lower()
        #print(momentary_text)
        
        if 'procesador' in momentary_text:
            try:
                processor = div.find('div', {'class': 'emsye847'}).text
            except:
                pass

        
        elif 'almacenamiento' in momentary_text:
            try:
                storege = div.find('div', {'class': 'emsye847'}).text.replace('\n',' ')
            except:
                pass


        elif 'cámara' in momentary_text:
            try:
                
                camera = div.find('div', {'class': 'emsye847'}).text
            except:
                pass
        

        elif 'pantalla' in momentary_text:
            try:
                screen = div.find('div', {'class': 'emsye847'}).text
            except:
                pass

        
    for div in more_especifications:
        momentary_text = div.find('div',{'class':'_1qzmwzw89 emsye84k'}).text.lower()
        #print(momentary_text)

        if 'ram' in momentary_text:
            try:
                ram = div.find('span').text
            except:
                pass
    
    personal_cell_phones['company'] = 'Personal'
    
    personal_cell_phones['model'] = model
    
    personal_cell_phones['price'] = price

    personal_cell_phones['ram'] = ram
    
    personal_cell_phones['processor'] = processor
    
    personal_cell_phones['storege'] = storege
    
    personal_cell_phones['camera'] = camera
    
    personal_cell_phones['screen'] = screen

    df_personal_cell_phones = pd.DataFrame(personal_cell_phones)

    return (df_personal_cell_phones.T)


'''I create a for loop to iterate through the cell phone identifiers, call the pare_cell_phones function with 
each identifier, and add the results to the df_personal_cell_phones DataFrame.'''

df_personal_cell_phones = pd.DataFrame()

for i in range(len(ids_cell_phones)):
    try:
        df_personal_cell_phones = pd.concat([df_personal_cell_phones, parse_cell_phones(ids_cell_phones[i])])
    except:
        pass

    if critical_errors > 10:
            print('It has more than 10 serious errors, if you want to stop the process press Ctrl + C')
            
    print(f'Progress {i+1} of {len(ids_cell_phones)}')

    time.sleep(random.randint(4,8))

browser.quit()

df_personal_cell_phones.to_csv('celulares_personal.csv', index = False)

print('Number of records obtained: ', len(df_personal_cell_phones))

print('Number of critical errors found: ', critical_errors)

print('Number of null data found: ',df_personal_cell_phones.iloc[:,:7].isnull().sum().sum())

print('extraction completed')
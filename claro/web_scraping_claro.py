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
number_iteration=1
ids_cell_phones = []


'''I execute the infinite while loop that will stop when it no longer detects any more pages 
with products within the loop, mainly the identifier of each cell phone will be obtained and 
it will be stored in ids_cell_phones.'''

while True:

    url = f'https://tienda.claro.com.ar/plp/equipos?pageNumber={page_number}'

    browser.get(url)

    time.sleep(random.randint(8,10))

    '''I try to click on a cookie acceptance element if it is present.'''
    try:
        browser.find_element('xpath', '//*[@id="didomi-notice-agree-button"]').click()
    except:
        pass
        
    html = browser.page_source

    soup = bs(html , 'lxml')

    final_page = int(soup.find('div',{'class':'Pagination_cont__28-ql'}).find_all('div',{'class': 'Pagination_number__3cAx4'})[-1].text)
    

    if page_number > final_page:        
        break

    page_number += 1



    articles = soup.find('div', {'class': 'Catalog_cont-fil-items__31RhA Catalog_filters-on__2NU5y'}).find('div', {'class': 'Catalog_items__3tiDK Catalog_grillax3__1AkL4'}).find_all('div', {'class': 'CardProducto_cont-sin-comparar__P90uJ'})

    for article in articles:
        cell_phone_id = article.find('a').get('href')

        ids_cell_phones.append(cell_phone_id)

      
        #print(article.find('a').get('href'))

ids_cell_phones = [phone for phone in ids_cell_phones if phone is not None]



claro_cell_phones = pd.Series()
critical_errors = 0

'''I define the function parce_cell_phones that takes a cell phone identifier 
as an argument and extracts detailed information about that phone from its individual page.'''

def parse_cell_phones(cell_phone_id):
    
    global critical_errors ## I indicate that 'critical_errors' is a global variable
    
    url = f'https://tienda.claro.com.ar{cell_phone_id}'
    
    try:
        browser.get(url)

        time.sleep(random.randint(5,12))

        html = browser.page_source

        soup = bs(html, 'lxml')

    
        model = soup.find('h1',{'data-test':'product_title'}).text

        price = int(soup.find('div', {'data-test': 'product_information'}).find('div',{'data-test':'product_prices'}).text.replace('$','').replace('.',''))


        especifications_1 = soup.find('div', {'class': 'Pdp_divFlexEspecificaciones__1ote3'}).find_all('div', {'class': 'Pdp_divIconFlex__3Hi6N'})
        especifications_2 = soup.find('div', {'class': 'Pdp_divTableEspecificaciones__3-bXX'}).find_all('div', {'class':'Pdp_divFlex__1AwU4'})

    except:
        critical_errors += 1
        return None
    
    '''I assign None to the variables because there are cases in which this data is not presented'''
    
    ram = None
    camera = None
    processor = None
    storege = None
    screen = None

    for div in especifications_1:
        
            momentary_text = div.text.lower()

            if 'cámara' in momentary_text:
                try:
                    camera = ' / Trasera '+ div.find('div', {'class':'Pdp_descriptionImg__2wfms'}).text
                except:
                    pass
                    
            elif 'display' in momentary_text:
                try:
                    screen = div.find('div', {'class':'Pdp_descriptionImg__2wfms'}).text
                except:
                      pass
            
            elif 'procesador' in momentary_text:
                    try:
                        processor = div.find('div', {'class':'Pdp_descriptionImg__2wfms'}).text
                    except:
                        pass



    

    for div in especifications_2:
            momentary_text = div.text.lower()

            if 'cámara' in   momentary_text:
                try:
                    camera = 'Frontal ' + div.find('div',{'class':'Pdp_divDescripcion__36s2x'}).text + camera
                except:
                    pass

            elif 'ram' in momentary_text:
                try:
                    ram =  div.find('div',{'class':'Pdp_divDescripcion__36s2x'}).text
                except:
                    pass

            elif 'memoria interna' in momentary_text:
                try:
                    storege =  div.find('div',{'class':'Pdp_divDescripcion__36s2x'}).text
                except:
                    pass


    claro_cell_phones['company'] = 'Claro'

    claro_cell_phones['model'] = model
    
    claro_cell_phones['price'] = price

    claro_cell_phones['ram'] = ram
    
    claro_cell_phones['processor'] = processor
    
    claro_cell_phones['storege'] = storege
    
    claro_cell_phones['camera'] = camera
    
    claro_cell_phones['screen'] = screen

    df_claro_cell_phones = pd.DataFrame(claro_cell_phones)

    return (df_claro_cell_phones.T)


'''I create a for loop to iterate through the cell phone identifiers, call the pare_cell_phones function with 
each identifier, and add the results to the df_claro_cell_phones DataFrame.'''

df_claro_cell_phones = parse_cell_phones(ids_cell_phones[0])

print('cantidad de filas', len(df_claro_cell_phones), ' de ', len(ids_cell_phones))

for i in range(1, len(ids_cell_phones)):
    try:
        df_claro_cell_phones = pd.concat([df_claro_cell_phones, parse_cell_phones(ids_cell_phones[i])])
    except:
        pass
    
    if critical_errors > 10:
        print('It has more than 10 serious errors, if you want to stop the process press Ctrl + C')

    print('cantidad de filas', len(df_claro_cell_phones), ' de ', len(ids_cell_phones))

    time.sleep(random.randint(4,10))

browser.quit()

df_claro_cell_phones.to_csv('celulares_claro.csv', index = False)

print('Number of records obtained: ', len(df_claro_cell_phones))

print('Number of critical errors found: ', critical_errors)

print('Number of null data found: ',df_claro_cell_phones.iloc[:,:7].isnull().sum().sum())

print('extraction completed')

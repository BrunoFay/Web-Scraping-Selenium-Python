from cmath import log
from timeit import repeat
from xml.dom.minidom import Attr
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from collections import Counter
from mongoConnection import db
import os


#setar um tamanho de tela
options= Options()
options.add_argument('window-size=1300,800')


#roda o script sem o navegador
""" options.headless= True """
main_url = os.getenv('SCRAPPING_URL')
browser= webdriver.Chrome(options=options)
browser_action=ActionChains(browser)
browser.get(main_url)


# fazer um pausa  para depois pegar o conteudo da pagina
sleep(1.5)

def hover_category(selector_name):
  browser_action.move_to_element(selector_name).perform()

# rolar até o final da page
def handle_scroll_page():
    first_scroll_height = browser.execute_script("return document.body.scrollHeight")
    positions=[]
    while True:
        sleep(0.3)
        repeat_positions= Counter(positions)
        first_scroll_height = browser.execute_script("return document.body.scrollHeight")
        html = browser.find_element(By.TAG_NAME,'html')
        html.send_keys(Keys.PAGE_DOWN)
        current_scroll_height = browser.execute_script("return document.body.scrollHeight")
        positions.append(current_scroll_height)
        if (repeat_positions[current_scroll_height] >= 10):
         break
    return 'finished'

def Select_cards():
    send_to_top=browser.find_element(By.CSS_SELECTOR,'#goToTop')
    send_to_top.click()
    page_content=browser.page_source
    site = BeautifulSoup(page_content,'html.parser')
    in_stock = site.find_all('div',attrs={
        'class':'ui card produto product-in-card in-stock',
      })
    out_of_stock = site.find_all('div',attrs={
        'class':'ui card produto product-in-card out-of-stock',
      })
    return in_stock + out_of_stock

def create_product_dict(list):
    product_cards=Select_cards()
    for product_card in product_cards:
        product_dict={}

        product_primary_card_img_element= product_card.find('img', attrs={'class':'visible content'})
        product_primary_card_img = product_primary_card_img_element['src']

        product_secondary_card_img_element= product_card.find('img', attrs={'class':'hidden content'})
        product_title= product_card.find('span', attrs={'itemprop':'name'})
        product_price= product_card.find('meta', attrs={'itemprop':'price'})

        if(product_secondary_card_img_element):
          product_secondary_card_img= product_secondary_card_img_element['src']
          product_dict['secondary_card_image'] = f'https:{product_secondary_card_img}'

        product_dict['primary_card_image'] = f'https:{product_primary_card_img}'
        product_dict['title'] = product_title.text
        product_dict['price'] = product_price['content']

        main_product_link = product_card.find('a', attrs={'itemprop':'url'})['href']
        browser.get(f'{main_url}{main_product_link}')

        page_content=browser.page_source
        site = BeautifulSoup(page_content,'html.parser')

        main_product_image_src_element = site.find('img',attrs={
            'id':'imagem-padrao',
          })
        main_product_image = main_product_image_src_element['src']
        secondary_images = site.find_all('img',attrs={
            'class':'ui image small centered',
          })
        """ setar array de images """
        secondaries_images_srcs=[]

        for img in secondary_images:
          imgSrc = img['src']
          secondaries_images_srcs.append(f'https:{imgSrc}')

        product_dict['main_image'] = f'https:{main_product_image}'
        product_dict['secondaries_images'] = secondaries_images_srcs

        list.append(product_dict)
        browser.back()



sneakers_list=[]
nike_list=[]
adidas_list=[]
vans_list=[]
puma_list=[]

def set_lists(category_list,category_order):
    count = 0
    while True:
        category_selector=browser.find_element(By.XPATH,f'/html/body/div[2]/div[3]/div[2]/div/nav/ul/li[{category_order}]/a')
        hover_category(category_selector)
        category_selector.click()
        check_looping=handle_scroll_page()
        create_product_dict(category_list)
        sleep(0.5)
        if(check_looping == 'finished'):
          break
        count += 1
set_lists(sneakers_list,1)
set_lists(nike_list,4)
set_lists(adidas_list,5)
set_lists(vans_list,6)
set_lists(puma_list,7)

browser.close()

def set_lists_on_db():
    sneakers_collection = db['Sneakers']
    nike_collection = db['Nike']
    adidas_collection = db['Adidas']
    vans_collection = db['Vans']
    puma_collection = db['Puma']

    sneakers_collection.insert_many(sneakers_list)
    nike_collection.insert_many(nike_list)
    adidas_collection.insert_many(adidas_list)
    vans_collection.insert_many(vans_list)
    puma_collection.insert_many(puma_list)

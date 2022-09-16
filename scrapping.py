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

#setar um tamanho de tela
options= Options()
options.add_argument('window-size=1300,800')
#roda o script sem o navegador
""" options.headless= True """
browser= webdriver.Chrome(options=options)
browser_action=ActionChains(browser)
browser.get('https://www.maze.com.br/')


# fazer um pausa de 2 segundos para depois pegar o conteudo da pagina
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
  tenis_cards=Select_cards()
  for tenis_card in tenis_cards:
    tenis={}

    tenis_primary_img= tenis_card.find('img', attrs={'class':'visible content'})
    tenis_secundary_img= tenis_card.find('img', attrs={'class':'hidden content'})
    tenis_title= tenis_card.find('span', attrs={'itemprop':'name'})
    tenis_price= tenis_card.find('meta', attrs={'itemprop':'price'})
    tenis_id= tenis_card.find('meta', attrs={'itemprop':'productID'})['content']
    if(tenis_secundary_img):
      tenis['secondary_card_image'] = tenis_secundary_img['src']
    tenis['primary_card_image'] = tenis_primary_img['data-src']
    tenis['title'] = tenis_title.text
    tenis['price'] = tenis_price['content']
    print(tenis_card)
    element_link_xpath = f'//*[@id="Product_{tenis_id}"]/div/a'
    browser.find_element(By.XPATH,element_link_xpath).click()
    break
    """ list.append(tenis) """


""" list=[]
nike_lists=[list for i in range(13)] """
sneakers_list=[]

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
set_lists(sneakers_list,7)
print(len(sneakers_list))


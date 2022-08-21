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
nike_airforce_list=[]
nike_airmax90_list=[]
nike_airmax97_list=[]


# fazer um pausa de 2 segundos para depois pegar o conteudo da pagina
sleep(1.5)
nike_selector=browser.find_element(By.XPATH,'/html/body/div[2]/div[3]/div[2]/div/nav/ul/li[4]/a')
def hover_category(selector_name):
  browser_action.move_to_element(selector_name).perform()
hover_category(nike_selector)
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
def Select_cards():
    send_to_top=browser.find_element(By.CSS_SELECTOR,'#goToTop')
    send_to_top.click()
    page_content=browser.page_source
    site = BeautifulSoup(page_content,'html.parser')
    return site.find_all('div',attrs={
        'class':'ui card produto product-in-card in-stock',
        'class':'ui card produto product-in-card out-of-stock'
      })

def create_product_dict(list):
  tenis_cards=Select_cards()
  for tenis_card in tenis_cards:
    tenis={}

    tenis_primary_img= tenis_card.find('img', attrs={'class':'visible content'})
    tenis_secundary_img= tenis_card.find('img', attrs={'class':'hidden content'})
    tenis_title= tenis_card.find('span', attrs={'itemprop':'name'})
    tenis_price= tenis_card.find('meta', attrs={'itemprop':'price'})

    if(tenis_secundary_img):
      tenis['secondary_card_image'] = tenis_secundary_img['src']
    tenis['primary_card_image'] = tenis_primary_img['data-src']
    tenis['title'] = tenis_title.text
    tenis['price'] = tenis_price['content']
    list.append(tenis)
count=1
list=[]
nike_lists=[list for i in range(13)]
while count <= 12:
    if count !=1:
      nike_selector=browser.find_element(By.XPATH,'/html/body/div[2]/div[3]/div[2]/div/nav/ul/li[4]/a')
      hover_category(nike_selector)
    selector=browser.find_element(By.XPATH,f'/html/body/div[2]/div[3]/div[2]/div/nav/ul/li[4]/div/div/div/div/div/div[{count}]/div/a')
    selector.click()
    handle_scroll_page()
    create_product_dict(nike_lists[count])
    count +=1
    sleep(1)


""" airmax90_selector=browser.find_element(By.XPATH,'/html/body/div[2]/div[3]/div[2]/div/nav/ul/li[4]/div/div/div/div/div/div[5]/div/a')
airmax90_selector.click()
handle_scroll_page()
create_product_dict(nike_airmax90_list)

sleep(1)
nike_selector=browser.find_element(By.XPATH,'/html/body/div[2]/div[3]/div[2]/div/nav/ul/li[4]/a')
browser_action.move_to_element(nike_selector).perform()
airmax97_selector=browser.find_element(By.XPATH,'/html/body/div[2]/div[3]/div[2]/div/nav/ul/li[4]/div/div/div/div/div/div[7]/div/a')
airmax97_selector.click()
handle_scroll_page()
create_product_dict(nike_airmax97_list) """
print(nike_lists)

""" search_input= brower.find_element(By.CSS_SELECTOR, 'body > div.pusher > div.ui.container.fluid.maze_header > div > div > div > div.ui.mobile.hide.eight.wide.tablet.ten.wide.computer.column.searchBar > div > div.ui.input.fluid.blocoBuscaContainer > input')
search_input.send_keys('puma')
sleep(0.4)

first_option= brower.find_element(By.CSS_SELECTOR,'body > div.pusher > div.ui.container.fluid.maze_header > div > div > div > div.ui.mobile.hide.eight.wide.tablet.ten.wide.computer.column.searchBar > div > div.results.hidden.results-clone > a:nth-child(1) > div')
first_option.click()

sleep(3) """
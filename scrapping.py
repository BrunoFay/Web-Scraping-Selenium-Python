from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

#setar um tamanho de tela
options= Options()
options.add_argument('window-size=1300,800')
navegador= webdriver.Chrome(options=options)

navegador.get('https://www.maze.com.br/')

# fazer um pausa de 2 segundos para depois pegar o conteudo da pagina
sleep(1)

search_input= navegador.find_element(By.CSS_SELECTOR, 'body > div.pusher > div.ui.container.fluid.maze_header > div > div > div > div.ui.mobile.hide.eight.wide.tablet.ten.wide.computer.column.searchBar > div > div.ui.input.fluid.blocoBuscaContainer > input')
search_input.send_keys('puma')
sleep(0.4)

first_option= navegador.find_element(By.CSS_SELECTOR,'body > div.pusher > div.ui.container.fluid.maze_header > div > div > div > div.ui.mobile.hide.eight.wide.tablet.ten.wide.computer.column.searchBar > div > div.results.hidden.results-clone > a:nth-child(1) > div')
first_option.click()

sleep(3)

page_content=navegador.page_source
site = BeautifulSoup(page_content,'html.parser')
print(site)

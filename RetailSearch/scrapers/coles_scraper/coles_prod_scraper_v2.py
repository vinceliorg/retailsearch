from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import os
import codecs

driver_path = '/usr/local/bin/chromedriver'

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--no-sandbox")

driver = Chrome(executable_path=driver_path,chrome_options=chrome_options)
i = 0 

filename = 'coles_prod_urls_v2.txt'
with open(filename) as file:
    urls = [line.rstrip() for line in file]



def parse(url):
    try: 
        global i
        if i!=0 & i % 100 == 0:
            time.sleep(300)
        print(f'extracting {i}th url: {url}')
        driver.get(url)
        n=os.path.join("products",url.split('/')[-1]+'.html')
        #open file in write mode with encoding
        #obtain page source
        #write page source content to file
        with open(n, "w", encoding='utf-8') as f:
            f.write(driver.page_source)
        time.sleep(1)
        i = i+1
    except:
        print('error, sleep and then going to retry')
        time.sleep(300)
        parse(url)

for url in urls:
    if 'product/' in url:
        parse(url)
    
driver.quit()
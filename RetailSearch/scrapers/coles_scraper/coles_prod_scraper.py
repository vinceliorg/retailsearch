from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time

driver_path = '/usr/local/bin/chromedriver'

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--no-sandbox")

driver = Chrome(executable_path=driver_path,chrome_options=chrome_options)
i = 0 

filename = 'coles_prod_urls.txt'
with open(filename) as file:
    urls = [line.rstrip() for line in file]

f = open("coles_products.csv", "a")

def parse(url):
    try: 
        global i
        i = i+1
        print(f'extracting {i}th url: {url}')
        driver.get(url)
        record={}
        xpath = '//span[@class="product-brand"]'
        brand = driver.find_elements(By.XPATH,xpath)[0].text
        # record['brand'] = brand.text
        xpath = '//span[@class="product-name"]'
        product_name = driver.find_elements(By.XPATH,xpath)[0].text
        # record['product_name'] = product_name.text
        xpath = '//span[@class="price-container"]'
        price = driver.find_elements(By.XPATH,xpath)[0].text
        xpath = '//span[@class="package-size"]'
        package_size = driver.find_elements(By.XPATH,xpath)[0].text
        # record['package_size'] = package_size.text
        xpath = '//span[@class="package-price"]'
        package_price = driver.find_elements(By.XPATH,xpath)[0].text
        # record['package_price'] = package_price.text
        xpath = '//div[@class="product-body"]'
        product_body = driver.find_elements(By.XPATH,xpath)[0].text
        # record['product_body'] = product_body.text
        xpath = '//img[@class="product-thumb-image"]'
        img_els = driver.find_elements(By.XPATH,xpath)
        imgs = []
        for img_el in img_els:
            href = img_el.get_attribute('data-ng-src')
            imgs.append(href )
        record = f'{brand}\t{product_name}\t{price}\t{package_size}\t{package_price}\t"{product_body}"\t{imgs}\n'
        f.write(record)
        time.sleep(100)
        
    except:
        print('error, going to retry')
        time.sleep(10)
        parse(url)

for url in urls:
    if 'product/' in url:
        parse(url)
    
driver.quit()
f.close()
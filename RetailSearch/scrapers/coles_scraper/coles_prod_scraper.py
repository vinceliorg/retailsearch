from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time

driver_path = '/usr/local/bin/chromedriver'

driver = Chrome(executable_path=driver_path)

filename = 'coles_prod_urls.txt'
with open(filename) as file:
    urls = [line.rstrip() for line in file]

def parse(url):
    try: 
        print(url)
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
    except:
        print('error, going to retry')
        parse(url)

f = open("coles_products.csv", "a")

for url in urls:
    parse(url)
    

driver.quit()
f.close()
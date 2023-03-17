from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
chrome_options = Options()
# chrome_options.add_argument("--headless")

filename = '/Users/vli/Work/RetailSearch/RetailSearch/scrapers/wws_prod_urls.txt'
with open(filename) as file:
    start_urls = [line.rstrip() for line in file]

# start_urls = ['https://www.woolworths.com.au/shop/productdetails/74280/woolworths-cadbury-hot-cross-buns-made-with-cadbury-chocolate']
driver_path = 'chromedriver_mac_arm64/chromedriver'

driver = Chrome(options=chrome_options, executable_path=driver_path)

# links = set()

def extract(driver, xpath):
    details = driver.find_elements(By.XPATH,xpath)
    if len(details)>0:
        details = details[0].text
    else:
        details = ''

    return details

def parse(url, retry = 0):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="price-cents"]')))
        # wait.until(EC.visibility_of_element_located((By.XPATH, '//div[class="ingredients"]')))
        
        title = driver.find_elements(By.XPATH,'//h1')[0].text
        price = driver.find_elements(By.XPATH,'//span[@class="price-dollars"]')[0].text
        price_centsPer = driver.find_elements(By.XPATH,'//span[@class="price-cents"]')[0].text
        package_price = extract(driver, '//div[@class="shelfProductTile-cupPrice"]')
        product_details = extract(driver, '//h2[@class="product-heading"]/following-sibling::div')
        ingredients = extract(driver, '//section[@class="ingredients"]')
        allergy = extract(driver, '//section[@class="allergen"]')
        record = {}
        record['title'] =  title
        record['price'] = price+'.'+price_centsPer
        record['package_price'] = package_price
        record['product_details'] = product_details
        record['ingredients'] = ingredients
        record['allergy'] = allergy
        f.write(json.dumps(record))
        time.sleep(1)
    except Exception as e:
        # print(str(e))
        if retry > 5:
            print('exceeding maximium retry, going to skip')
            return
        print('extraction error, retry')
        time.sleep(5)
        parse(url, retry=retry+1)
        

f = open("wws_products.json", "w")
f.write('[')
ct = 0
for url in start_urls:
    print(f'parsing url:{url}')
    parse(url)
    f.write(',\n')
    ct = ct +1
    if ct/10 == 0:
        time.sleep(2)
f.write(']')
f.close()

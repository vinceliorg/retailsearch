from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
chrome_options = Options()
# chrome_options.add_argument("--headless")

start_urls = ['https://www.woolworths.com.au/shop/browse/fruit-veg',
        'https://www.woolworths.com.au/shop/browse/meat-seafood-deli',
        'https://www.woolworths.com.au/shop/browse/bakery',
        'https://www.woolworths.com.au/shop/browse/dairy-eggs-fridge',
        'https://www.woolworths.com.au/shop/browse/health-wellness',
        'https://www.woolworths.com.au/shop/browse/pantry',
        'https://www.woolworths.com.au/shop/browse/snacks-confectionery',
        'https://www.woolworths.com.au/shop/browse/lunch-box',
        'https://www.woolworths.com.au/shop/browse/freezer',
        'https://www.woolworths.com.au/shop/browse/drinks',
        'https://www.woolworths.com.au/shop/browse/liquor',
        'https://www.woolworths.com.au/shop/browse/pet',
        'https://www.woolworths.com.au/shop/browse/baby',
        'https://www.woolworths.com.au/shop/browse/beauty-personal-care',
        'https://www.woolworths.com.au/shop/browse/household'
        ]

driver_path = 'chromedriver_mac_arm64/chromedriver'

driver = Chrome(options=chrome_options, executable_path=driver_path)

links = set()
processed_links = set()
prod_linlks = set()


def parse(url):
    if url in processed_links:
        return
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        xpath = '//a'
        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@rel="next"]')))
        
        link_elements = driver.find_elements(By.XPATH,xpath)
        f = open("wws_urls.txt", "a")
        for el_link in link_elements:
            href = el_link.get_attribute('href')
            if href is not None:
                if '/shop/browse' in href and 'pageNumber' in href:
                    if href not in links:
                        links.add(href)
                        f.write(href+'\n')
                        print(href)
        f.close()
        processed_links.add(url)
        next_page = driver.find_elements(By.XPATH,'//a[@rel="next"]')
        if next_page is not None:
            parse(next_page[0].get_attribute('href'))
        time.sleep(2)
    except:
        print('extraction error, skip')
        return
    
for url in start_urls:
    parse(url)


# # lv2_links = []
# # for link in lv1_cat_links:
# #     driver.get(link)
# #     link_elements = driver.find_elements(By.XPATH,xpath)
# #     for el_link in link_elements:
# #         href = el_link.get_attribute('href')
# #         lv2_links.append(href)

# # f = open("coles_urls.txt", "a")
# # lv3_links = []
# # for link in lv2_links:
# #     driver.get(link)
# #     link_elements = driver.find_elements(By.XPATH,xpath)
# #     for el_link in link_elements:
# #         href = el_link.get_attribute('href')
# #         # print(href)
# #         lv3_links.append(href)
# #         f.write(href+'\n')

# # # get pages 
# # cat_pages = []
# # for link in lv3_links:
# #     driver.get(link)
# #     xpath = '//li[@class="page-number"]/a'
# #     link_elements = driver.find_elements(By.XPATH,xpath)
# #     if len(link_elements)>0:
# #         for el_link in link_elements:
# #             href = el_link.get_attribute('href')
# #             f.write(href+'\n')
# #             cat_pages.append(href)
# driver.quit()
# # f.close()
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
chrome_options = Options()
# chrome_options.add_argument("--headless")

filename = '/Users/vli/Work/RetailSearch/RetailSearch/scrapers/wws_urls.txt'
with open(filename) as file:
    start_urls = [line.rstrip() for line in file]

driver_path = 'chromedriver_mac_arm64/chromedriver'

driver = Chrome(options=chrome_options, executable_path=driver_path)

links = set()


def parse(url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        xpath = '//a[@class="product-title-link"]'
        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@rel="next"]')))
        
        link_elements = driver.find_elements(By.XPATH,xpath)
        f = open("wws_prod_urls.txt", "a")
        for el_link in link_elements:
            href = el_link.get_attribute('href')
            if href is not None:
                if 'shop/productdetails' in href:
                    if href not in links:
                        links.add(href)
                        f.write(href+'\n')
                        print(href)
        f.close()
        links.add(url)
        time.sleep(1)
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
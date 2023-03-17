from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By


driver_path = '/usr/local/bin/chromedriver'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--no-sandbox")

driver = Chrome(executable_path=driver_path)
driver.get('https://www.coles.com.au/browse')

xpath = '//li/a[@data-testid="category-card"]'
link_elements = driver.find_elements(By.XPATH,xpath)


lv1_cat_links = []
for el_link in link_elements:
    href = el_link.get_attribute('href')
    print(href)
    lv1_cat_links.append(href)

lv2_links = []
for link in lv1_cat_links:
    driver.get(link)
    xpath = '//li/a[@data-testid="nav-link"]'
    link_elements = driver.find_elements(By.XPATH,xpath)
    for el_link in link_elements:
        href = el_link.get_attribute('href')
        if '/browse' in href:
            lv2_links.append(href)

f = open("coles_urls_v2.txt", "a")
lv3_links = []
for link in lv2_links:
    driver.get(link)
    xpath = '//nav[@data-testid = "pagination"]//a'
    link_elements = driver.find_elements(By.XPATH,xpath)
    for el_link in link_elements:
        href = el_link.get_attribute('href')
        print(href)
        lv3_links.append(href)
        f.write(href+'\n')

# # get pages 
# cat_pages = []
# for link in lv3_links:
#     driver.get(link)
#     xpath = '//li[@class="page-number"]/a'
#     link_elements = driver.find_elements(By.XPATH,xpath)
#     if len(link_elements)>0:
#         for el_link in link_elements:
#             href = el_link.get_attribute('href')
#             f.write(href+'\n')
#             cat_pages.append(href)
# driver.quit()
# f.close()
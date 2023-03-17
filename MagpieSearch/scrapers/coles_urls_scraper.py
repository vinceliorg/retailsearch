from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

driver_path = 'chromedriver_mac_arm64/chromedriver'

driver = Chrome(executable_path=driver_path)
driver.get('https://shop.coles.com.au/a/national/everything/browse')

xpath = '//li[@class="cat-nav-item"]/a'
link_elements = driver.find_elements(By.XPATH,xpath)

lv1_cat_links = []
for el_link in link_elements:
    href = el_link.get_attribute('href')
    lv1_cat_links.append(href)

lv2_links = []
for link in lv1_cat_links:
    driver.get(link)
    link_elements = driver.find_elements(By.XPATH,xpath)
    for el_link in link_elements:
        href = el_link.get_attribute('href')
        lv2_links.append(href)

f = open("coles_urls.txt", "a")
lv3_links = []
for link in lv2_links:
    driver.get(link)
    link_elements = driver.find_elements(By.XPATH,xpath)
    for el_link in link_elements:
        href = el_link.get_attribute('href')
        # print(href)
        lv3_links.append(href)
        f.write(href+'\n')

# get pages 
cat_pages = []
for link in lv3_links:
    driver.get(link)
    xpath = '//li[@class="page-number"]/a'
    link_elements = driver.find_elements(By.XPATH,xpath)
    if len(link_elements)>0:
        for el_link in link_elements:
            href = el_link.get_attribute('href')
            f.write(href+'\n')
            cat_pages.append(href)
driver.quit()
f.close()
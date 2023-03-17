from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

driver_path = 'chromedriver_mac_arm64/chromedriver'

driver = Chrome(executable_path=driver_path)

filename = 'coles_urls_v2.txt'
with open(filename) as file:
    urls = [line.rstrip() for line in file]

f = open("coles_prod_urls.txt", "a")
for url in urls:
    driver.get(url)
    xpath = '//a[@class="product__link"]'
    link_elements = driver.find_elements(By.XPATH,xpath)

    # prod_links = []
    for el_link in link_elements:
        href = el_link.get_attribute('href')
        # prod_links.append(href)
        if href is not None:
            print(href)
            f.write(href+'\n')
driver.quit()
f.close()
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math
chrome_options = Options()
# chrome_options.add_argument("--headless")


driver_path = 'chromedriver_mac_arm64/chromedriver'

driver = Chrome(options=chrome_options, executable_path=driver_path)

links = set()

filename = '/Users/vli/Work/RetailSearch/RetailSearch/scrapers/seek_urls.txt'
with open(filename) as file:
    start_urls = [line.rstrip() for line in file]

def parse(url, retry = 0):
    global driver
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        xpath = '//article[@data-automation="normalJob"]//a'
        # wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@rel="next"]')))
        
        elememnts = driver.find_elements(By.XPATH,xpath)
        f = open("seek_job_urls.txt", "a")
        for el in elememnts:
            href = el.get_attribute('href')
            if href not in links and 'https://www.seek.com.au/job/' in href:
                print(href)
                links.add(href)
                f.write(href+'\n')
        f.close()
        time.sleep(2)
    except Exception as e:
        if retry > 5:
            print('exceeding maximium retry, going to skip')
            return
        print('extraction error, retry')
        
        driver = Chrome(options=chrome_options, executable_path=driver_path)
        print("Current session is {}".format(driver.session_id))
        time.sleep(5)
        parse(url, retry=retry+1)
    
for url in start_urls:
    parse(url)
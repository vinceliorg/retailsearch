from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math
chrome_options = Options()
# chrome_options.add_argument("--headless")

start_urls = ['https://www.seek.com.au/jobs?classification=1200',
'https://www.seek.com.au/jobs?classification=6251',
'https://www.seek.com.au/jobs?classification=6304',
'https://www.seek.com.au/jobs?classification=1203',
'https://www.seek.com.au/jobs?classification=1204',
'https://www.seek.com.au/jobs?classification=7019',
'https://www.seek.com.au/jobs?classification=6163',
'https://www.seek.com.au/jobs?classification=1206',
'https://www.seek.com.au/jobs?classification=6076',
'https://www.seek.com.au/jobs?classification=6263',
'https://www.seek.com.au/jobs?classification=6123',
'https://www.seek.com.au/jobs?classification=1209',
'https://www.seek.com.au/jobs?classification=6205',
'https://www.seek.com.au/jobs?classification=1210',
'https://www.seek.com.au/jobs?classification=1211',
'https://www.seek.com.au/jobs?classification=1212',
'https://www.seek.com.au/jobs?classification=6317',
'https://www.seek.com.au/jobs?classification=6281',
'https://www.seek.com.au/jobs?classification=1214',
'https://www.seek.com.au/jobs?classification=1216',
'https://www.seek.com.au/jobs?classification=6092',
'https://www.seek.com.au/jobs?classification=6008',
'https://www.seek.com.au/jobs?classification=6058',
'https://www.seek.com.au/jobs?classification=1220',
'https://www.seek.com.au/jobs?classification=6043',
'https://www.seek.com.au/jobs?classification=6362',
'https://www.seek.com.au/jobs?classification=1223',
'https://www.seek.com.au/jobs?classification=6261',
'https://www.seek.com.au/jobs?classification=6246',
'https://www.seek.com.au/jobs?classification=1225'
]

driver_path = 'chromedriver_mac_arm64/chromedriver'

driver = Chrome(options=chrome_options, executable_path=driver_path)

links = set()


def parse(url, retry = 0):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        xpath = '//span[@data-automation="totalJobsCount"]'
        # wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@rel="next"]')))
        
        total_count = driver.find_elements(By.XPATH,xpath)[0]
        total_count = total_count.text
        pages = math.ceil(int(total_count.replace(',',''))/22)
        print(f'total jobs: {pages}')
        f = open("seek_urls.txt", "a")
        for i in range(1, pages+1):
            links.add(f'{url}?page={i}\n')
        f.writelines(links )
        f.close()
        time.sleep(2)
    except Exception as e:
        if retry > 5:
            print('exceeding maximium retry, going to skip')
            return
        print('extraction error, retry')
        global driver
        driver = Chrome(options=chrome_options, executable_path=driver_path)
        print("Current session is {}".format(driver.session_id))
        time.sleep(5)
        parse(url, retry=retry+1)
i = 0   
for url in start_urls:
    i = i+1
    # pause
    if i/100000 == 0:
        time.sleep(600)
        global driver
        driver = Chrome(options=chrome_options, executable_path=driver_path)
        print("Current session is {}".format(driver.session_id))
    parse(url)
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math
import json
chrome_options = Options()
# chrome_options.add_argument("--headless")
import logging

logging.basicConfig(filename='/Users/vli/Work/RetailSearch/MagpieSearch/logs/indeed_scraper.log', filemode='w', level=logging.INFO)

# create logger
logger = logging.getLogger('indeed scraper')
# create console handler and set level to debug
ch = logging.StreamHandler()

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

driver_path = 'chromedriver_mac_arm64/chromedriver'

# driver = Chrome(options=chrome_options, executable_path=driver_path)

driver = Chrome(options=chrome_options)
processed_links = set()
listing_urls = set()

urls = ['https://au.indeed.com/jobs?q=&l=Victoria&sc=0kf%3Ajt%28casual%29%3B',
        'https://au.indeed.com/jobs?l=Victoria&sc=0kf%3Ajt%28fulltime%29%3B&rbl=Melbourne+VIC',
        'https://au.indeed.com/jobs?l=Victoria&sc=0kf%3Ajt%28fulltime%29%3B&rbl=Victoria',
        'https://au.indeed.com/jobs?l=Victoria&sc=0kf%3Ajt%28fulltime%29%3B&rbl=Dandenong+VIC',
        'https://au.indeed.com/jobs?l=Victoria&sc=0kf%3Ajt%28fulltime%29%3B&rbl=Melbourne+City+Centre+VIC',
        'https://au.indeed.com/jobs?l=Victoria&sc=0kf%3Ajt%28fulltime%29%3B&rbl=Geelong+VIC',
        'https://au.indeed.com/jobs?l=Victoria&sc=0kf%3Ajt%28fulltime%29%3B&rbl=Ballarat+VIC',
        'https://au.indeed.com/jobs?l=Victoria&sc=0kf%3Ajt%28fulltime%29%3B&rbl=Bendigo+VIC',
        'https://au.indeed.com/jobs?l=Victoria&sc=0kf%3Ajt%28fulltime%29%3B&rbl=Shepparton+VIC',
        'https://au.indeed.com/jobs?l=Victoria&sc=0kf%3Ajt%28fulltime%29%3B&rbl=Clayton+VIC',
        'https://au.indeed.com/jobs?l=Victoria&sc=0kf%3Ajt%28fulltime%29%3B&rbl=Richmond+VIC',
        'https://au.indeed.com/jobs?l=Victoria&sc=0kf%3Ajt%28fulltime%29%3B&rbl=Tullamarine+VIC',
        'https://au.indeed.com/jobs?l=Victoria&sc=0kf%3Ajt%28fulltime%29%3B&rbl=Port+Melbourne+VIC',
        'https://au.indeed.com/jobs?l=Victoria&sc=0kf%3Ajt%28fulltime%29%3B&rbl=Sunshine+VIC',
        'https://au.indeed.com/jobs?l=Victoria&sc=0kf%3Ajt%28fulltime%29%3B&rbl=Campbellfield+VIC',
        'https://au.indeed.com/jobs?q=&l=Victoria&sc=0kf%3Ajt%28parttime%29%3B',
        'https://au.indeed.com/jobs?q=&l=Victoria&sc=0kf%3Ajt%28permanent%29%3B',
        'https://au.indeed.com/jobs?q=&l=Victoria&sc=0kf%3Ajt%28contract%29%3B',
        'https://au.indeed.com/jobs?q=&l=Victoria&sc=0kf%3Ajt%28apprenticeship%29%3B',
        'https://au.indeed.com/jobs?q=&l=Victoria&sc=0kf%3Ajt%28subcontract29%3B',
        'https://au.indeed.com/jobs?q=&l=Victoria&sc=0kf%3Ajt%28temporary29%3B',
        'https://au.indeed.com/jobs?q=&l=Victoria&sc=0kf%3Ajt%28internship29%3B',
        'https://au.indeed.com/jobs?q=&l=Victoria&sc=0kf%3Ajt%28volunteer29%3B',
                # 'https://au.indeed.com/jobs?q=&l=New+South+Wales',
                # 'https://au.indeed.com/jobs?q=&l=South+Australia',
                # 'https://au.indeed.com/jobs?q=&l=Western+Australia',
                # 'https://au.indeed.com/jobs?q=&l=Queensland',
                # 'https://au.indeed.com/jobs?q=&l=Tasmania'
                ]
outfile = open('indeed_jobs.json', 'a')

# parse all the page links
def parse_list(url, retry = 0):
    if len(listing_urls )/1000==0 and len(listing_urls )>0:
        logger.info('sleep fpr 5 minutes')
        time.sleep(300)
    print(f'process url: {url}')
    global driver
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//nav')))

        xpath = '//div[@class="job_seen_beacon"]//td[@class="resultContent"]//a[@class="jcs-JobTitle css-jspxzf eu4oa1w0"]'
        
        job_cnt = driver.find_elements(By.XPATH,'//div[@class="jobsearch-JobCountAndSortPane-jobCount"]')
        if len(job_cnt) > 0:
            job_cnt = job_cnt[0].text
            job_cnt = job_cnt.split()[0]
            if ',' in job_cnt:
                job_cnt = job_cnt.replace(',','')
                job_cnt = int(job_cnt)
        page_size = math.ceil(job_cnt/10)

        for page in range(0,page_size):
            page_link = f'{url}&start={page*10}'
            if page_link not in listing_urls:
                logger.info(f'found link: {page_link}')
                listing_urls.add(page_link )
    except Exception as e:
        logger.error(str(e))
        print('extraction error, retry')
        time.sleep(5)

# parse a listing page
def parse(url, retry = 0):
    if len(processed_links)/1000==0 and len(processed_links)>0:
        logger.info('sleep fpr 5 minutes')
        time.sleep(300)
    print(f'process url: {url}')
    global driver
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        # xpath = '//nav'
        wait.until(EC.visibility_of_element_located((By.XPATH, '//nav')))

        xpath = '//div[@class="job_seen_beacon"]//td[@class="resultContent"]//a[@class="jcs-JobTitle css-jspxzf eu4oa1w0"]'
        
        elememnts = driver.find_elements(By.XPATH,xpath)
        links = []
        for el in elememnts:
            id = el.get_attribute('data-jk')
            job_url = 'https://au.indeed.com/viewjob?jk='+id
            if  job_url not in processed_links:
                links.append(job_url)
        logger.info(f'found {len(links)} links')
        for link in links:
            if link not in processed_links:
                # driver = Chrome(options=chrome_options)
                job = parse_jobs(driver,link)
                json.dump(job, outfile)
                outfile.write('\n')
                processed_links.add(link)
                time.sleep(3)
    except Exception as e:
        
        logger.error(str(e))
        if retry > 5:
            print('exceeding maximium retry, going to skip')
            return
        print('extraction error, retry')
        driver.close()
        driver = Chrome(options=chrome_options)
        print("Current session is {}".format(driver.session_id))
        time.sleep(5)
        parse(url, retry=retry+1)

# parse individual jobs
def parse_jobs(driver, url, retry = 0):
    try:
        logger.info(f'extracting from {url}')
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="jobDescriptionText"]')))

        xpath = '//div[@class="jobsearch-JobInfoHeader-title-container "]//span'
        
        title = driver.find_elements(By.XPATH,xpath)
        if len(title)==0:
            title = driver.find_elements(By.XPATH,'//div[@class="jobsearch-JobInfoHeader-title-container jobsearch-JobInfoHeader-title-containerEji"]')

        company = driver.find_elements(By.XPATH,'//div[@data-company-name="true"]/a')
        location = driver.find_elements(By.XPATH,'//div[@class="jobsearch-CompanyInfoContainer"]//div[@class="css-6z8o9s eu4oa1w0"]')
        qualitification = driver.find_elements(By.XPATH,'//id[@class="qualificationsSection"]')
        salary = driver.find_elements(By.XPATH,'//span[@class="css-2iqe2o eu4oa1w0"]')
        job_type = driver.find_elements(By.XPATH,'//div[@id="jobDetailsSection"]//div[@class="css-rr5fiy eu4oa1w0"]')
        description = driver.find_elements(By.XPATH,'//div[@id="jobDescriptionText"]')

        if len(location) == 0:
            location = ''
        else:
            location = location[0].text
        
        if len(company) == 0:
            company_text = ''
            company_url = ''
        else:
            print(company)
            company_text = company[0].text
            company_url = company[0].get_attribute('href')
        
        if len(salary) == 0:
            salary = ''
        else:
            salary = salary[0].text

        if len(qualitification ) == 0:
            qualitification = ''
        else:
            qualitification = qualitification[0].text
        
        if len(job_type) < 2:
            job_type = ''
        else:
            job_type = job_type[1].text
        
        if len(description) == 0:
            description = ''
        else:
            description= description[0].text
        

        
        job = {'title':title[0].text,
               'company':company_text,
               'company_url':company_url,
               'location': location,
               'salary': salary,
               'url': url,
               'jobtype': job_type,
               'qualification' : qualitification,
               'description': description
        }
        # logger.info(json.dumps(job))
        time.sleep(2)
        return job
    except Exception as e:
        print(str(e))
        if retry > 5:
            print('exceeding maximium retry, going to skip')
            return
        print('extraction error, retry')
        driver.close()
        driver = Chrome(options=chrome_options)
        print("Current session is {}".format(driver.session_id))
        time.sleep(5)
        parse_jobs(driver,url, retry=retry+1)


def main():
    for url in urls:
        parse_list(url, retry = 0)
    for url in listing_urls: 
        parse(url)

if __name__ == "__main__":
    main()
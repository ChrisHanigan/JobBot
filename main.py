# https://realpython.com/beautiful-soup-web-scraper-python/

from keywords import *
import requests
import pprint
from bs4 import BeautifulSoup

# index
#
# 1. Search functions
# 2. function executions


# search functions ############################################################# search functions
def monster():

    URL = 'https://www.monster.com/jobs/search/?q={}&where={}'.format(keyword, location)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='ResultsContainer')
    job_elems = results.find_all('section', class_='card-content')
    #python_jobs = results.find_all('h2',
    #                               string=lambda text: 'python' in text.lower())
    for job_elem in job_elems:
        title_elem = job_elem.find('h2', class_='title')
        company_elem = job_elem.find('div', class_='company')
        location_elem = job_elem.find('div', class_='location')

        if None in (title_elem, company_elem, location_elem):
            continue
        detail_link = job_elem.find('a')['href']
        detail_page = requests.get(detail_link)
        detail_soup = BeautifulSoup(detail_page.content, 'html.parser')
        detail_container = detail_soup.find(id='content')
        if None in (detail_link, detail_container):
            continue

        print(title_elem.text.strip())
        print(company_elem.text.strip())
        print(location_elem.text.strip())
        print(detail_link)
        print(detail_container.text.strip())
        print()

    # for p_job in python_jobs:

    #    link = p_job.find('a')['href']
    #    print(p_job.text.strip())
    #    print(f"Apply here: {link}\n")

def seek():
    URL = 'https://www.seek.com.au/{}-jobs/in-All-{}'.format(keyword, location)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('article')

    for job_elem in results:
        title_elem = job_elem.find('h1')
        company_elem = job_elem.find('a', class_='_3AMdmRg')
        location_elem = job_elem.find('div', class_='xxz8a1h').find('a', class_='_3AMdmRg')

        detail_link = 'https://www.seek.com.au'+title_elem.find("a")['href']
        detail_page = requests.get(detail_link)
        detail_soup = BeautifulSoup(detail_page.content, 'html.parser')
        detail_container = detail_soup.find('div', class_='_2e4Pi2B')

        print(title_elem.text)
        print(company_elem.text)
        print(location_elem.text)
        print(detail_link)
        print(detail_container.text.strip())
        print()



# executions ################################################################### function executions

# monster()
seek()

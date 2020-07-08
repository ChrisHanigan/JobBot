"""Gets jobs adverts and analyses them."""
import mmap
import csv
import sys
import requests
import pandas
# import pprint
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from parsel import Selector
from keywords import keyword, location

# index
#
# 1. universals
# 2. Search functions
# 3. function executions

# universals ###################################################### universals

jobdata = ["title", "company", "location", "url", "details"]
JOBS_COLLECTED = 0


def jobsdone():
    '''Count number of jobs while searching'''
    global JOBS_COLLECTED
    JOBS_COLLECTED = JOBS_COLLECTED + 1
    print('jobs done: ' + str(JOBS_COLLECTED))


# create File
def createfile():
    with open('data.csv', 'w', newline=''):  # as datafile:
        #   datawrite = csv.writer(datafile)
        pass


def write(jobdata):
    with open('data.csv', 'a', newline='') as datafile:
        datawrite = csv.writer(datafile)
        datawrite.writerow(jobdata)


# search functions ########################################## search functions
def monster():

    URL = 'https://www.monster.com/jobs/search/?q={}&where={}'.format(
        keyword, location)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='ResultsContainer')
    job_elems = results.find_all('section', class_='card-content')

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


def seek():
    '''Search seek.com and write job advertisements to file'''
    url = 'https://www.seek.com.au/{}-jobs/in-All-{}'.format(keyword, location)

    def scrape(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all('article')

        for job_elem in results:
            title_elem = job_elem.find('h1')
            company_elem = job_elem.find('a', class_='_3AMdmRg')
            location_elem = job_elem.find('div', class_='xxz8a1h').find(
                'a', class_='_3AMdmRg')

            detail_link = 'https://www.seek.com.au' + \
                title_elem.find("a")['href']
            detail_page = requests.get(detail_link)
            detail_soup = BeautifulSoup(detail_page.content, 'html.parser')
            detail_container = detail_soup.find('div', class_='_2e4Pi2B')

            jobdata = [
                title_elem.text, company_elem.text, location_elem.text,
                detail_link,
                detail_container.text.strip()
            ]

            write(jobdata)

            jobsdone()

        next_page = 'https://www.seek.com.au' + \
            soup.find('a', rel='next')['href']
        scrape(next_page)

    scrape(url)


def VicGov():
    # https://www.linkedin.com/pulse/how-easy-scraping-data-from-linkedin-profiles-david-craven/
    # URL = "https://jobs.careers.vic.gov.au/jobtools/"
    pass


def linkedin():
    '''Search linkedin.com and write job advertisements to file'''
    driver = webdriver.Chrome()
    # https://www.linkedin.com/pulse/how-easy-scraping-data-from-linkedin-profiles-david-craven/
    URL = 'https://www.linkedin.com/jobs/search/?keywords={}&location={}'.format(
        keyword, location)

    def scrape(URL):
        driver.get(URL)

        # page = driver.page_source.encode(sys.stdout.encoding, errors='replace')
        # soup = BeautifulSoup(page, 'html.parser')

        def checkpage():
            noEnd = True
            while noEnd is True:
                print('scrolling')
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                page = driver.page_source.encode(sys.stdout.encoding,
                                                 errors='replace')
                soup = BeautifulSoup(page, 'html.parser')
                if (soup.find(
                        'button',
                        class_='infinite-scroller__show-more-button--visible')
                    ):
                    noEnd = False
                    print('end')
            else:
                print('processing')
                results = soup.find_all('li', class_='result-card')
                for job_elem in results:
                    detail_link = job_elem.find('a')['href']
                    driver.get(detail_link)
                    page = driver.page_source.encode(sys.stdout.encoding,
                                                     errors='replace')
                    soup = BeautifulSoup(page, 'html.parser')
                    # soup. get detail sections of job page e.g. title, description

        checkpage()
        driver.quit()

    scrape(URL)


# Process results ############################################# Process results https://www.youtube.com/watch?v=vmEHCJofslg&t=904s


def process():
    '''Process results.'''
    data = pandas.read_csv('data.csv', 'utf-8', engine='python', delimiter=',')
    print(data.loc[~data['details'].str.contains('experience')])


# executions ############################################# function executions
# createfile()
# write(jobdata)

# seek()
# # monster()
# linkedin()
# VicGov()

# ---TODO---
# indeed()
# careerone()
# jobsearchaus()
# adzuna()
# aps()
process()

# threading.Thread(target=f).start() to run simultaniously

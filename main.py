from keywords import *
import requests
# import pprint
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from parsel import Selector
import sys
import csv

# index
#
# 1. universals
# 2. Search functions
# 3. function executions

# universals ###################################################### universals
# driver = webdriver.Chrome()
jobdata = ["title", "company", "location", "url", "details"]
jobscollected = 0


# counts number of jobs found !! UnboundLocalError: local variable 'jobscollected' referenced before assignment
def jobsdone():
    global jobscollected
    jobscollected = jobscollected + 1
    print('jobs done: ' + str(jobscollected))


# create File
with open('data.csv', 'w', newline='') as datafile:
    datawrite = csv.writer(datafile)


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
    URL = 'https://www.seek.com.au/{}-jobs/in-All-{}'.format(keyword, location)

    def scrape(URL):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all('article')

        for job_elem in results:
            title_elem = job_elem.find('h1')
            company_elem = job_elem.find('a', class_='_3AMdmRg')
            location_elem = job_elem.find(
                'div', class_='xxz8a1h').find('a', class_='_3AMdmRg')

            detail_link = 'https://www.seek.com.au' + \
                title_elem.find("a")['href']
            detail_page = requests.get(detail_link)
            detail_soup = BeautifulSoup(detail_page.content, 'html.parser')
            detail_container = detail_soup.find('div', class_='_2e4Pi2B')

            jobdata = [title_elem.text, company_elem.text,
                       location_elem.text, detail_link, detail_container.text.strip()]

            write(jobdata)

            jobsdone()

        next_page = 'https://www.seek.com.au' + \
            soup.find('a', rel='next')['href']
        scrape(next_page)

    scrape(URL)


def VicGov():
    # https://www.linkedin.com/pulse/how-easy-scraping-data-from-linkedin-profiles-david-craven/
    URL = "https://jobs.careers.vic.gov.au/jobtools/"


def linkedin():
    # https://www.linkedin.com/pulse/how-easy-scraping-data-from-linkedin-profiles-david-craven/
    URL = 'https://www.linkedin.com/jobs/search/?keywords={}&location={}'.format(
        keyword, location)

    def scrape(URL):
        driver.get(URL)
        page = driver.page_source.encode(sys.stdout.encoding, errors='replace')
        soup = BeautifulSoup(page, 'html.parser')
        # next_page = soup.find

        def checkpage():
            noEnd = True
            while noEnd is True:
                print('scrolling')
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                page = driver.page_source.encode(
                    sys.stdout.encoding, errors='replace')
                soup = BeautifulSoup(page, 'html.parser')
                if (soup.find('button', class_='infinite-scroller__show-more-button--visible')):
                    noEnd = False
                    print('end')
            else:
                print('processing')
                results = soup.find_all('li', class_='result-card')
                for job_elem in results:
                    detail_link = job_elem.find('a')['href']
                    driver.get(detail_link)
                    page = driver.page_source.encode(
                        sys.stdout.encoding, errors='replace')
                    soup = BeautifulSoup(page, 'html.parser')
                    # soup. get detail sections of job page e.g. title, description

        checkpage()
        driver.quit()
    scrape(URL)


# executions ############################################# function executions

write(jobdata)
# monster()
seek()
# linkedin()
# VicGov()

# TODO
# indeed()
# careerone()
# jobsearchaus()
# adzuna()
# aps()

# threading.Thread(target=f).start() to run simultaniously

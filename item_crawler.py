#! /usr/bin/env python
# coding: utf-8

import argparse
from selenium import webdriver
from random import uniform
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="Crawling Item Name")

parser.add_argument('--url', dest="url", type=str, default=None, help="URL")
parser.add_argument('--search', dest="search", type=str, default=None, help="Something to Search")

args = parser.parse_args()


def crawling_items(url, search):
    #browser = randint(0, 2)

    #if browser == 0:
    #    driver = webdriver.Chrome("C:/webdriver/chromedriver.exe")
    #elif browser == 1:
    #    driver = webdriver.Edge("C:/webdriver/MicrosoftWebDriver.exe")
    #elif browser == 2:
    #    driver = webdriver.Firefox("C:\\webdriver\\geckodriver.exe")
    #else:
    #    exit()

    driver = webdriver.Chrome("C:/webdriver/chromedriver.exe")

    driver.implicitly_wait(uniform(2.5, 4.0))

    driver.get(url)

    driver.find_element_by_id("searchinput").click()
    driver.find_element_by_id("searchinput").send_keys(search)
    driver.find_element_by_class_name("search_bar2").click()

    driver.implicitly_wait(uniform(2.5, 4.0))

    links = driver.find_elements_by_css_selector("table > tbody > tr > td > a.link")

    for link in range(len(links)):
        #link.click()
        driver.find_elements_by_css_selector("table > tbody > tr > td > a.link")[link].click()
        driver.implicitly_wait(uniform(2.5, 4.0))
        codes = driver.find_elements_by_css_selector("td > a > font")
        for code in codes:
            code.click()
            driver.implicitly_wait(uniform(2.5, 4.0))
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            items = soup.select("div#tab1 > table > tbody > tr > td")
            for item in items:
                print(item.text)
        driver.find_element_by_class_name("search_bar2").click()
        driver.implicitly_wait(uniform(2.5, 4.0))
    print(links)


def main():
    crawling_items(args.url, args.search)


if __name__ == '__main__':
    main()

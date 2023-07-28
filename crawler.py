#!/usr/bin/env python
"""
Sets up a WebDriver session using a local copy of TorBrowser, and Selenium via geckodriver. 
"""

import time
import pprint

import re
import csv
import json
import torDriver


useFirstResult = True
result = 0
justTheTip = True
timeoutInSeconds = 20
finalTimeoutInSeconds = 20
listOfSearches = []
termsToSearch = []
key = 1

torDriverInstance = torDriver.TorDriver()
# Setup the TorBrowser and geckodriver
torDriverInstance.downloadGeckodriver()
torDriverInstance.setupTor()

# @description: Crawls from a search term
# @param: searchTerm - The term to search for
# @return: A collection of objects with the data and link
def crawlFromSearch(searchTerm):
    # Setup the webdriver
    driver = torDriverInstance.setupWebdriver()

    try:
        driver.get("https://searx.thegpm.org/")
        torDriver.isVisible(driver, "#q")
        elem = driver.find_element_by_css_selector("#q")
        elem.clear()
        elem.send_keys(searchTerm)
        elem.send_keys(Keys.RETURN)
    except Exception as e:
        print(e)
        driver.quit()
        raise SystemError("Literally cannot even search")

    # Wait for some seconds
    time.sleep(timeoutInSeconds)

    try:
        torDriver.isVisible(driver, "#main_results > div.result.result-default > h4 > a")
        firstPageResults = driver.find_elements_by_css_selector("#main_results > div.result.result-default > h4 > a")
    except Exception as e:
        print(e)
        driver.quit()
        raise SystemError("Issue browsing from search")
    
    # Use just the first result for now.
    # Can start separate threads for each result here.
    firstPageResults[0].click() 

    # Wait for some seconds
    time.sleep(timeoutInSeconds)
    # torDriver.isVisible(driver, "#links div.result")

    # try:
    #     category = driver.find_elements_by_xpath("//a[contains(@href, 'companycredits')]")
    #     category.location_once_scrolled_into_view
    # except Exception as e:
    #     print(e)
    #     driver.quit()
    #     raise SystemError("Literally cannot even find a category")

    # # Use just the first result
    # category[1].location_once_scrolled_into_view
    # category[1].click()

    # # Wait for some seconds
    # time.sleep(timeoutInSeconds)

    # try:
    #     # https://developer.mozilla.org/en-US/docs/Web/CSS/Adjacent_sibling_combinator
    #     subCategory = driver.find_element_by_xpath("//h4[@id='distributors']/following-sibling::ul[1]")
    #     subCategory.location_once_scrolled_into_view
    #     subCategoryListItems = driver.find_elements_by_xpath("//h4[@id='distributors']/following-sibling::ul[1]/li")
    #     subCategoryListHrefs = driver.find_elements_by_xpath("//h4[@id='distributors']/following-sibling::ul[1]/li/a")
    # except Exception as e:
    #     print(e)
    #     driver.quit()
    #     raise SystemError("Literally cannot even find a sub category")
    
    parsedCollection = []
    # intKey = 0
    # for item in subCategoryListItems:
    #     parsedObject = {
    #         "data": item.text.encode('utf-8').strip(),
    #         "link": subCategoryListHrefs[intKey].get_attribute("href").strip()
    #     }
    #     # print(parsedObject)
    #     parsedCollection.append(parsedObject)
    #     intKey += 1

    # driver.quit()

    return parsedCollection


# Read in the search terms
with open("searches.txt", "r") as fileHandler:
    listOfSearches = fileHandler.readlines()


for searchTerm in listOfSearches:
    if searchTerm:
        # This Regex is inspired from a discussion about 
        # substituting characters that are not letters or numbers
        # https://stackoverflow.com/a/5843547/682915
        strippedWithSpaces = re.sub(r'([^\s\w]|_)+', '', itemSubStrip)
        strippedWithUnderbar = re.sub(r' ', '_', strippedWithSpaces)
        termsToSearch.append({
            "name": strippedWithSpaces,
            "file": "./results/" + strippedWithUnderbar.lower() + ".json",
            "search": ' '.join([strippedWithSpaces.lower(), 'imdb']),
            "orig": searchTerm,
            "num": "",
            "artifacts": [{}]
        })

# For each term, search and then crawl
for term in termsToSearch:
    try:
        print("Starting search...")
        print(term["name"])
        # Crawl
        artifactsCollection = crawlFromSearch(term["search"])
        term["artifacts"] = artifactsCollection
    except Exception as e:
        print(f"Something bad happened looking for {term}")
        print(e)
        continue

    print("Writing file...")
    # Write to file
    with open(term["file"], "w") as txtFile:
        txtFile.write(json.dumps(term))
        print(term["file"])

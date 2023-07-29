#!/usr/bin/env python
"""
Sets up a WebDriver session using a local copy of TorBrowser, and Selenium via geckodriver. 
"""

import time
import pprint

import re
import csv
import json
import urllib

import torDriver


from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

useFirstResult = True
result = 0
justTheTip = True
timeoutInSeconds = 5
finalTimeoutInSeconds = 5
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
        elem = driver.find_element(By.CSS_SELECTOR, "#q")
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
        firstPageResults = driver.find_elements(By.CSS_SELECTOR, "#main_results > div.result.result-default > h4 > a")
    except Exception as e:
        print(e)
        driver.quit()
        raise SystemError("Issue browsing from search")
    
    # Use just the first result for now.
    # Can start separate threads for each result here.
    pprint.pprint(firstPageResults)
    thisUrl = firstPageResults[0].get_attribute('href')
    firstPageResults[0].click()
    # Wait for the page to load

    time.sleep(timeoutInSeconds)
    torDriver.isVisible(driver, "a")

    print("This url")
    print(thisUrl)
    pprint.pprint(thisUrl)

    _url = urllib.parse.urlparse(thisUrl)
    print("Parsed url")
    pprint.pprint(_url)

    allUrls = driver.find_elements(By.XPATH, "//a")

    parsedCollection = []
    onPageUrls = []
    offPageUrls = []
    for url in allUrls:
        pprint.pprint(url.text)
        urlHref = url.get_attribute('href')
        pprint.pprint(urlHref)
        parsedObject = {
            "data": url.text, # Any data as plain text or base64.
            "link": urlHref, # Link to the data
            "parent": thisUrl # Link to the parent page
        }
        parsedCollection.append(parsedObject)

    driver.quit()

    return parsedCollection


# Read in the search terms
with open("searches.txt", "r") as fileHandler:
    listOfSearches = fileHandler.readlines()


# For each term, search and then crawl.
suffix = ""

for searchTerm in listOfSearches:
    if searchTerm:
        # This Regex is inspired from a discussion about 
        # substituting characters that are not letters or numbers
        # https://stackoverflow.com/a/5843547/682915
        strippedWithSpaces = re.sub(r'([^\s\w]|_)+', '', searchTerm).strip()
        strippedWithUnderbar = re.sub(r' ', '_', strippedWithSpaces)
        strippedLower = strippedWithUnderbar.lower().strip()
        termsToSearch.append({
            "name": strippedWithSpaces,
            "file": "./results/" + strippedLower + ".json",
            "search": ' '.join([strippedWithSpaces, suffix]),
            "orig": searchTerm,
            "num": "",
            "artifacts": None
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
        continue # Skip to the next term

    print("Writing file...", "\n", term["file"])
    # Write to file
    with open(term["file"], "w") as txtFile:
        txtFile.write(json.dumps(term))
        print("Done writing file...", "\n", term["file"])


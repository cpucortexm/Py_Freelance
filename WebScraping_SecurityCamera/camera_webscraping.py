#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Filename:    camera_webscraping.py
# @Author:      Yogesh K
# @Time:        13/07/21 9:12 AM
# =============================================================================
# Imports
# =============================================================================
import PySimpleGUI as sg
from bs4 import BeautifulSoup  # bs4 is package and Beautiful soup is module
import requests
import http.client
import re
import argparse
from pylogger import pylog
from web_link_crawler import extract_all_links

# =============================================================================
# Global Defines
# =============================================================================
URL = "https://www.flipkart.com/search?q=home%20security%20camera"


def getUsrInput():
    """
    getUsrInput() will display the user options to select feature list for camera.
    This will be then used to scrape the flipkart.com to select the camera

    :return: None
    """
    layout = [[sg.T("         "), sg.Checkbox('Do you want Night Vision', default=True, key="-IN1-")],
              [sg.T("         "), sg.Checkbox('Do you want Pan', default=True, key="-IN2-")],
              [sg.T("         "), sg.Checkbox('Do you want Wall Mount', default=True, key="-IN3-")],
              [sg.T("         "), sg.Checkbox('Do you want HDD support', default=True, key="-IN4-")],
              [sg.T("         "), sg.Checkbox('Do you want Outdoor support', default=True, key="-IN5-")],
              [sg.T("         "), sg.Checkbox('Do you want 1080p Resolution', default=True, key="-IN6-")],
              [sg.T("         "), sg.Checkbox('Do you want two channels', default=True, key="-IN7-")],
              [sg.T("         "), sg.Checkbox('Do you want white color ', default=True, key="-IN8-")],
              [sg.T("         "), sg.Checkbox('Do you want Tilt', default=True, key="-IN9-")],
              [sg.T("")], [sg.T("        "), sg.Button('Done', size=(20, 4))], [sg.T("")]
              ]

    # Setting Window
    window = sg.Window('Select/Deselect the Camera Features ', layout, size=(400, 400))

    usrCamFeatures = {  # Initialise a dictionary with default values for user feature set
        'nightVision': True,  # This dict will be used for web scraping later
        'pan': True,
        'mount-wall': True,
        'hDD': True,
        'outdoor': True,
        'resolution-1080': True,
        'no-of-channels-2': True,
        'color-white': True,
        'tilt': True
    }
    while True:
        event, values = window.read()
        usrCamFeatures.update(  # update dict based on user input
            {
                'nightVision': values["-IN1-"],
                'pan': values["-IN2-"],
                'mount-wall': values["-IN3-"],
                'hDD': values["-IN4-"],
                'outdoor': values["-IN5-"],
                'resolution-1080': values["-IN6-"],
                'no-of-channels-2': values["-IN7-"],
                'color-white': values["-IN8-"],
                'tilt': values["-IN9-"]
            }
        )
        if event == sg.WIN_CLOSED or event == "Done":
            break

    window.close()
    usr_features_to_scrape = []
    for key, value in usrCamFeatures.items():
        print(key, ':', value)
        if not value:
            continue
        usr_features_to_scrape.append(key)
    return usr_features_to_scrape


def extract_scraping_links(source_url):
    """
    extract_scraping_links() will take the source url and return the actual links which need to be scraped for
    Flipkart camera
    :return: Links to be scraped
    """
    logger.info(f'Extracting links from {source_url}')
    page = requests.get(source_url)  # reponse is 200 for success

    if page.status_code != http.client.OK:
        logger.error(f'Error retrieving {source_url}: {page}')
        return []

    soup = BeautifulSoup(page.text, "html.parser")
    #logger.info(soup.prettify())    # should print the whole html data

    # From html data extract only smartUrl links using regex. Regex is the only option as other standard procedures like
    # soup.find("tags", params) etc cannot be applied to such complex websites and such huge html data
    # Next we are looking for smartUrl keyword followed by non
    # greedy(.*?) double quotes("") to get the exact web links
    smartURL = re.findall(r"\"smartUrl\":\".*?\"", soup.prettify())  # is a list
    all_http_links = set()    # To get unique list of links
    for link in smartURL:
        #print(link)  # At this point we have all the url links of the cameras to be scraped
        el = re.search(r"\"(http:.*?)\"",
                        link)  # As we use group, search()/findall() will only return matched group and not quotes "

        # re.search() returns a string with double quotes("sssss") for the match. This double quotes around the match
        # needs to be removed , as list append() again adds a single quote to the string.
        link_remove_quote = re.sub("\"", "", el.group())  # el.group() gives the exact matched result after re.search()
        all_http_links.add(link_remove_quote)

    return all_http_links


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', type=int, help='Number of workers',
                        default=4)
    parser.add_argument('-u', type=str, help='Base site url',
                        default=URL)
    args = parser.parse_args()
    usr_features_to_scrape = getUsrInput()
    logger.debug('This is a main debug message')
    # Start extracting the links to scrape
    links_to_scrape = extract_scraping_links(args.u)
    # Now scrape all the links
    extract_all_links(links_to_scrape, args.u, usr_features_to_scrape)


# Now scraping begins for every url
# All variables defined in __name__ =='__main__' are global by default and can be used anywhere
if __name__ == '__main__':
    # Initialise Logger
    logger = pylog.get_logger(__name__)
    main()

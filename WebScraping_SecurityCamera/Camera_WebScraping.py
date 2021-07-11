#!/usr/bin/env python3
# =============================================================================
# Author  : Yogesh K
# Date    : 10 July 2021
# Scraping the web for camera info
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
from urllib.parse import urlparse, urljoin
# =============================================================================
# Global Defines
# =============================================================================
URL = "https://www.flipkart.com/search?q=security+camera+for+home"


def getUsrInput():
    """
    getUsrInput() will display the user options to select feature list for camera.
    This will be then used to scrape the flipkart.com to select the camera

    :return: None
    """
    layout = [[sg.T("         "), sg.Checkbox('Do you want Night Vision', default=True, key="-IN1-")],
              [sg.T("         "), sg.Checkbox('Do you want Pan/Tilt', default=True, key="-IN2-")],
              [sg.T("         "), sg.Checkbox('Do you want Wall Mount', default=True, key="-IN3-")],
              [sg.T("         "), sg.Checkbox('Do you want HDD support', default=True, key="-IN4-")],
              [sg.T("         "), sg.Checkbox('Do you want Outdoor support', default=True, key="-IN5-")],
              [sg.T("         "), sg.Checkbox('Do you want 1080p Resolution', default=True, key="-IN6-")],
              [sg.T("         "), sg.Checkbox('Do you want two channels', default=True, key="-IN7-")],
              [sg.T("         "), sg.Checkbox('Do you want white color ', default=True, key="-IN8-")],
              [sg.T("")], [sg.T("        "), sg.Button('Done', size=(20, 4))], [sg.T("")]
              ]

    # Setting Window
    window = sg.Window('Select the Camera Features', layout, size=(300, 300))

    usrCamFeatures = {  # Initialise a dictionary with default values for user feature set
        'nightVision': True,  # This dict will be used for web scraping later
        'pan-tilt': True,
        'mount-wall': True,
        'hDD': True,
        'outdoor': True,
        'resolution-1080': True,
        'channels-2': True,
        'color-white': True,
    }
    while True:
        event, values = window.read()
        usrCamFeatures.update(  # update dict based on user input
            {
                'nightVision': values["-IN1-"],
                'pan-tilt': values["-IN2-"],
                'mount-wall': values["-IN3-"],
                'hDD': values["-IN4-"],
                'outdoor': values["-IN5-"],
                'resolution-1080': values["-IN6-"],
                'channels-2': values["-IN7-"],
                'color-white': values["-IN8-"]
            }
        )
        if event == sg.WIN_CLOSED or event == "Done":
            break

    window.close()
    for key, value in usrCamFeatures.items():
        print(key, ':', value)


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
    only_http_link = []
    for link in smartURL:
        # print(link)  # At this point we have all the url links of the cameras to be scraped
        el = re.findall(r"\"(http:.*?)\"",
                        link)  # As we use group, findall will only return matched group and not quotes "
        print(el)
        only_http_link.append(el)

    return only_http_link

def scrape_all_links(links):
    """
    scrape_all_links() will scrape all the links
    :param: links All the links to be scraped
    :return: Links to be scraped
    """

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', type=int, help='Number of workers',
                        default=4)
    parser.add_argument('-u', type=str, help='Base site url',
                        default=URL)
    args = parser.parse_args()
    getUsrInput()
    logger.debug('This is a main debug message')
    # Start extracting the links to scrape
    links_to_scrape = extract_scraping_links(args.u)
    # Now scrape all the links
    scrape_all_links(links_to_scrape, args.u)


# Now scraping begins for every url
# All variables defined in __name__ =='__main__' are global by default and can be used anywhere
if __name__ == '__main__':
    # Initialise Logger
    logger = pylog.get_logger(__name__)
    main()

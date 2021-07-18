#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Filename:    web_link_crawler.py
# @Author:      Yogesh K
# @Time:        13/07/21 10:33 AM
# =============================================================================
# Imports
# =============================================================================
from pylogger import pylog
from urllib.parse import urlparse, urljoin
import requests
import http.client
from bs4 import BeautifulSoup  # bs4 is package and Beautiful soup is module
import re

logger = pylog.get_logger(__name__)


def handle_night_vision(soup):
    logger.info("Parsing Night Vision:")
    pattern = re.compile("Night Vision Feature")
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here.
        return True
    return False


def handle_pan(soup):
    logger.info("Parsing Pan:")
    pattern = re.compile("Pan")
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here.
        return True
    return False


def handle_wall_mounting(soup):
    logger.info("Parsing Wall mount:")
    pattern = re.compile("\"Mounting Type\".*?Wall", re.IGNORECASE)  # .*? to get non greedy match or minimum match
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here, instead of 2 steps
        return True
    return False


def handle_HDD(soup):
    logger.info("Parsing HDD:")
    pattern = re.compile("\"HDD Available\".*?Yes", re.IGNORECASE)  # .*? to get non greedy match or minimum match
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here, instead of 2 steps
        return True
    return False


def handle_outdoor(soup):
    logger.info("Parsing Outdoor:")
    pattern = re.compile("outdoor", re.IGNORECASE)  # .*? to get non greedy match or minimum match
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here, instead of 2 steps
        return True
    return False


def handle_1080(soup):
    logger.info("Parsing 1080p:")
    # .*? to get non greedy match or minimum match
    pattern = re.compile("\"Video Recording Resolution\".*?1080", re.IGNORECASE)
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here, instead of 2 steps
        return True
    return False


def handle_no_of_channels(soup):
    logger.info("Parsing No of channels:")
    # .*? to get non greedy match or minimum match
    pattern = re.compile("\"Number of Channels\".*?2", re.IGNORECASE)
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here, instead of 2 steps
        return True
    return False


def handle_color_white(soup):
    logger.info("Parsing White color:")
    # .*? to get non greedy match or minimum match
    pattern = re.compile("\"Color\".*?White", re.IGNORECASE)
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here, instead of 2 steps
        return True
    return False


def handle_tilt(soup):
    logger.info("Parsing Tilt:")
    pattern = re.compile("Tilt", re.IGNORECASE)
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here.
        return True
    return False


def handle_default(soup):
    logger.error("Default case , Error key:")
    return False


# Dict table to scrape
scrape_table_dict = {
    'nightVision': handle_night_vision,
    'pan': handle_pan,
    'mount-wall': handle_wall_mounting,
    'hDD': handle_HDD,
    'outdoor': handle_outdoor,
    'resolution-1080': handle_1080,
    'no-of-channels-2': handle_no_of_channels,
    'color-white': handle_color_white,
    'tilt': handle_tilt
    # Add below this line new feature
}


def search_scrape_text(soup, features_to_scrape):
    for feature in features_to_scrape:
        # We use Walrus operator than the traditional if (cond) else so as to avoid code bloat
        if scrape_result := scrape_table_dict.get(feature, handle_default)(soup):
            continue
        return False
    return True


def process_page(page, usr_features_to_scrape):
    soup = BeautifulSoup(page.text, "html.parser")
    # logger.info(soup.prettify()) # print the whole html page info
    return search_scrape_text(soup, usr_features_to_scrape)


def show_usr_camera_list(usr_camera_list):
    logger.info("........Suggested cameras links...........")
    if not usr_camera_list:
        logger.info("Unfortunately, No cameras match the given user features")
    for cam in usr_camera_list:
        logger.info(cam)


def extract_all_links(source_links, worker_threads, usr_features_to_scrape):
    # parsed_source = urlparse(source_links)
    # Should be replaced by multi processes or threads.
    count_cam = 0
    list_suggest_cameras = []

    for link in source_links:
        print(link)
        page = requests.get(link)
        if page.status_code != http.client.OK:
            logger.error(f'Error retrieving {link}: {page}')
            continue   # We move to next Link
        if 'html' not in page.headers['Content-type']:
            logger.info(f'Link {link} is not an HTML page')
            continue  # We move to next link
        # We suggest only the first 2 cameras with all the user features satisfied, else whatever the number < 2
        # Then break
        if page_result := process_page(page, usr_features_to_scrape):
            if count_cam == 2:
                break
            list_suggest_cameras.append(link)
            count_cam += 1
        continue   # It comes here if process_page was False, so move to next link
    show_usr_camera_list(list_suggest_cameras)
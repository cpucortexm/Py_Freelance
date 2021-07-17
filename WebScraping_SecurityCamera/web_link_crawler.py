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


# To scrape use mostly regex
# Highlights , Specifications -> General, Product Details, Additional Features
# For Highlights find the line with <div class="_3a9CI2">
# For Specifications -> General, find the line with <div class="flxcaE">General</div>
# For Specification  -> Product Details, find line with <div class="flxcaE">Product Details</div>
# For Specification  -> Additional Features, find line with <div class="flxcaE">Additional Features</div>


def handle_night_vision(soup):
    print("In NV")
    pass


def handle_pan(soup):
    pass


def handle_wall_mounting(soup):
    pass


def handle_HDD(soup):
    pass


def handle_outdoor(soup):
    pass


def handle_1080(soup):
    pass


def handle_no_of_channels(soup):
    pass


def handle_color_white(soup):
    pass


def handle_tilt(soup):
    pass


def handle_default(soup):
    pass


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
}


def search_scrape_text(soup, features_to_scrape):
    for feature in features_to_scrape:
        scrape_table_dict.get(feature, handle_default)(soup)


def process_page(page, usr_features_to_scrape, link):
    soup = BeautifulSoup(page.text, "html.parser")
    # logger.info(soup.prettify()) # print the whole html page info
    search_scrape_text(soup, usr_features_to_scrape)


def extract_all_links(source_links, worker_threads, usr_features_to_scrape):
    # parsed_source = urlparse(source_links)
    # Should be replaced by multi processes or threads.
    for link in source_links:
        print(link)
        page = requests.get(link)
        if page.status_code != http.client.OK:
            logger.error(f'Error retrieving {link}: {page}')
            return []
        if 'html' not in page.headers['Content-type']:
            logger.info(f'Link {link} is not an HTML page')
            return []
        process_page(page, usr_features_to_scrape, link)

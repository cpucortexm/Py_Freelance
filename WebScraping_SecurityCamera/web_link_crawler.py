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
import concurrent.futures
import csv

logger = pylog.get_logger(__name__)

# Tomorrow Continue from Here, Handle True and False correctly
# What should happen if required is False and what when required is true.
def handle_night_vision(soup, required):
    logger.info("Night Vision needed: {}".format(required))
    pattern = re.compile("Night Vision Feature")
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here.
        if required is False:   # Case where search is successful, but we dont need it. We should move to next link, hence return False
            return False
        return True   # Case where search is successful and we need it. We should process this link further, hence return True
    else:
        if required is False:     # Case where search is not successful, and we dont need it. Return True, as we must still process the link further
            return True
        return False       # Case where search is not successful, and we need it. Return False, as we must move to next link



def handle_pan(soup, required):
    logger.info("Pan needed: {}".format(required))
    pattern = re.compile("Pan")
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here.
        if required is False:   # Case where search is successful, but we dont need it. We should move to next link, hence return False
            return False
        return True     # Case where search is successful and we need it. We should process this link further, hence return True
    else:
        if required is False:  # Case where search is not successful, and we dont need it. Return True, as we must still process the link further
            return True
        return False        # Case where search is not successful, and we need it. Return False, as we must move to next link



def handle_wall_mounting(soup, required):
    logger.info("Wall mount needed: {}".format(required))
    pattern = re.compile("\"Mounting Type\".*?Wall", re.IGNORECASE)  # .*? to get non greedy match or minimum match
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here, instead of 2 steps
        if required is False:   # Case where search is successful, but we dont need it. We should move to next link, hence return False
           return False
        return True         # Case where search is successful and we need it. We should process this link further, hence return True
    else:
        if required is False:  # Case where search is not successful, and we dont need it. Return True, as we must still process the link further
            return True
        return False    # Case where search is not successful, and we need it. Return False, as we must move to next link



def handle_HDD(soup, required):
    logger.info("HDD needed: {}".format(required))
    pattern = re.compile("\"HDD Available\",\"values\"\:\[\"Yes\"\]", re.IGNORECASE)  # .*? to get non greedy match or minimum match
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here, instead of 2 steps
        if required is False:  # Case where search is successful, but we dont need it. We should move to next link, hence return False
            return False   
        return True # Case where search is successful and we need it. We should process this link further, hence return True
    else:
        if required is False:  # Case where search is not successful, and we dont need it. Return True, as we must still process the link further
            return True
        return False    # Case where search is not successful, and we need it. Return False, as we must move to next link



def handle_outdoor(soup, required):
    logger.info("Outdoor needed: {}".format(required))
    pattern = re.compile("outdoor", re.IGNORECASE)  # .*? to get non greedy match or minimum match
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here, instead of 2 steps
        if required is False:   # Case where search is successful, but we dont need it. We should move to next link, hence return False
            return False
        return True      # Case where search is successful and we need it. We should process this link further, hence return True
    else:
        if required is False:   # Case where search is not successful, and we dont need it. Return True, as we must still process the link further
            return True
        return False    # Case where search is not successful, and we need it. Return False, as we must move to next link



def handle_1080(soup, required):
    logger.info("1080p needed: {}".format(required))
    # .*? to get non greedy match or minimum match
    pattern = re.compile("\"Video Recording Resolution\".*?1080", re.IGNORECASE)
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here, instead of 2 steps
        if required is False:   # Case where search is successful, but we dont need it. We should move to next link, hence return False
            return False
        return True
    else:
        if required is False:
            return True
        return False



def handle_no_of_channels(soup, required):
    logger.info("2 channel needed: {}".format(required))
    # .*? to get non greedy match or minimum match
    pattern = re.compile("\"Number of Channels\".*?\[\"2\"\]", re.IGNORECASE)
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here, instead of 2 steps
        if required is False:   # Case where search is successful, but we dont need it. We should move to next link, hence return False
            return False
        return True
    else:
        if required is False:  # Case where search is not successful, and we dont need it. Return True, as we must still process the link further
            return True
        return False  # Case where search is not successful, and we need it. Return False, as we must move to next link


def handle_color_white(soup, required):
    logger.info("White color needed: {}".format(required))
    # .*? to get non greedy match or minimum match
    pattern = re.compile("\"Color\".*?White", re.IGNORECASE)
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here, instead of 2 steps
        if required is False:   # Case where search is successful, but we dont need it. We should move to next link, hence return False
            return False
        return True
    else:
        if required is False: # Case where search is not successful, and we dont need it. Return True, as we must still process the link further
            return True
        return False # Case where search is not successful, and we need it. Return False, as we must move to next link



def handle_tilt(soup,required):
    logger.info("Tilt needed: {}".format(required))
    pattern = re.compile("Tilt", re.IGNORECASE)
    if result := re.search(pattern, soup.prettify()) is not None:  # Walrus operator is used here.
        if required is False:   # Case where search is successful, but we dont need it. We should move to next link, hence return False
            return False
        return True
    else:
        if required is False: # Case where search is not successful, and we dont need it. Return True, as we must still process the link further
            return True
        return False   # Case where search is not successful, and we need it. Return False, as we must move to next link



def handle_default(soup, required):
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
    for key, value in features_to_scrape.items():
        # We use Walrus operator than the traditional if (cond) else so as to avoid code bloat
        if scrape_result := scrape_table_dict.get(key, handle_default)(soup, value):
            continue
        return False
    return True


def process_page(page, usr_features_to_scrape):
    soup = BeautifulSoup(page.text, "html.parser")
    # logger.info(soup.prettify()) # print the whole html page info
    return search_scrape_text(soup, usr_features_to_scrape)


def show_usr_camera_list(usr_camera_list):
    csv_file = open('camera_list.csv', 'w')
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['SL No', 'Camera Link'])
    logger.info("..........................................")
    logger.info("|                                        |")
    logger.info("........Suggested cameras links...........")
    logger.info("|                                        |")
    logger.info("..........................................")
    if not usr_camera_list:
        logger.info("Unfortunately, No cameras match the given user features")
        csv_writer.writerow(['NONE', 'Unfortunately, No cameras match the given user features'])
    for index, cam in enumerate(usr_camera_list, 1):
        logger.info(cam)
        csv_writer.writerow([index, cam])
    csv_file.close()


# Enable this if you dont need Multi threading. It will process in a for loop
'''
def extract_all_links(source_links, worker_threads, usr_features_to_scrape):

    # extract_all_links() takes all source links and user features needed, processes each link separately,
    # to check if it has all the user features needed
    # :return: List of cameras to be displayed to users

    # parsed_source = urlparse(source_links)
    # Should be replaced by multi processes or threads.
    count_cam = 0
    list_suggest_cameras = []

    for link in source_links:
        logger.info('processing link: {}'.format(link))
        page = requests.get(link)
        if page.status_code != http.client.OK:
            logger.error(f'Error retrieving {link}: {page}')
            continue   # We move to next Link
        if 'html' not in page.headers['Content-type']:
            logger.info(f'Link {link} is not an HTML page')
            continue  # We move to next link
        # We suggest only the first 2 cameras with all the user features satisfied, else whatever the number < 2
        # Then break
        if page_result := process_page(page, usr_features_to_scrape): # Use walrus operator, calls the function and also assigns true/false in one line
            if count_cam == 2:
                break
            list_suggest_cameras.append(link)
            count_cam += 1
        continue   #  If process_page was False, move to next link
    show_usr_camera_list(list_suggest_cameras)
'''



def process_link(link, usr_features_to_scrape):
    logger.info('processing link: {}'.format(link))
    page = requests.get(link)

    if page.status_code != http.client.OK:
        logger.error(f'Error retrieving {link}: {page}')
        return
        #continue   # We move to next Link
    if 'html' not in page.headers['Content-type']:
        logger.info(f'Link {link} is not an HTML page')
        return
    if page_result := process_page(page, usr_features_to_scrape): # Use walrus operator, calls the function and also assigns true/false in one line
        logger.info("Success:{}".format(link))
        return link


# This uses multi threading technique to get the processing done and is faster
# Hence enabled by default
def extract_all_links(source_links, worker_threads, usr_features_to_scrape):
    """
    extract_all_links() takes all source links and user features needed, processes each link separately,
    to check if it has all the user features needed
    :return: List of cameras to be displayed to users
    """
    cameras_to_display = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker_threads) as executor:
        futures = [executor.submit(process_link, url, usr_features_to_scrape) for url in source_links] 
        for future in concurrent.futures.as_completed(futures):
            logger.info('Result: {}'.format(future.result()))
            if future.result() is not None:    # append list only if link is not none
                cameras_to_display.append(future.result())

    show_usr_camera_list(cameras_to_display) # Display user the camera list

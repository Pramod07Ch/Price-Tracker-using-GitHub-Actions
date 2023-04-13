import os
import re
import sys
import requests
import pandas as pd
import unicodedata
from bs4 import BeautifulSoup as bs
from datetime import datetime
from pytz import timezone
import logging
import logging.handlers



def extract_from_URL(url):
    ''' Extracts the product name and price from the URL and returns a list

    Args:
        url (str): URL of the product

    Returns:
        list: [product_name, price, time_now]
    '''

    # Check if URL is valid
    if not url.startswith(url):
        return None
    
    # Create a session object for the requests
    session = requests.Session()

    # Make the request using the session object
    request = session.get(url)

    # if request was successful
    if request.status_code != 200:
        return None
    
    # HtML prasing
    soup = bs(request.content,'html.parser')

    # Check product name is present on the page
    product_name_elem = soup.find("span",{"class":"B_NuCI"})
    if not product_name_elem:
        return None
    
    # Extract and normalize the product name
    product_name = unicodedata.normalize("NFKD", product_name_elem.get_text())

    # Check if price is present on the page
    price_elem = soup.find("div",{"class":"_30jeq3 _16Jk6d"})
    if not price_elem:
        return None
    
    # Extract the price
    price = int(''.join(re.findall(r'\d+', price_elem.get_text())))
    
    # Get the current time from the timezone
    # time_now = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M')

    return [product_name, price]

URL= "https://www.flipkart.com/apple-iphone-14-pro-max-space-black-128-gb/p/itm9aed88fe43457?pid=MOBGHWFHCNVGGMZF&lid=LSTMOBGHWFHCNVGGMZFEEIZN3&marketplace=FLIPKART&q=iphone+14+pro+max&store=tyy%2F4io&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_2_9_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_9_na_na_na&fm=organic&iid=6e7af0b4-e3cc-48d5-a304-7e8aadce016a.MOBGHWFHCNVGGMZF.SEARCH&ppt=hp&ppn=homepage&ssid=w0apy6ro0g0000001681107610607&qH=37e37d60a349d989"
output = extract_from_URL(URL)

# logger object name specified
logger = logging.getLogger(output[0])
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
                    "capture.log",  # name of the file
                    maxBytes=1024 * 1024,
                    backupCount=1,
                    encoding="utf8",
                )

# formatter to log objects
formatter = logging.Formatter("%(name)s; %(message)s; %(asctime)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)


# log message
logger.info(int(output[1]))
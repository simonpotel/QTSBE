import os
import sys
import requests
from bs4 import BeautifulSoup
from loguru import logger

# import the lib DEXcryptoLib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from DEXcryptoLib.Lib import *

class algo(object):
    def __init__(self,
                 name="",
                 version="",
                 author="",
                 description="",
                 db_connect=True):
        self.name = name
        self.version = version 
        self.author = author 
        self.description = description
        if db_connect:
            self.db_smartswap_data = init_database(
                "smartswap_data",
                os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../configs/db_config.json")
                )
            self.db_smartswap_data.connect()
            logger.info("Connected to database")

    def get_crypto_logo_from_table_str(self, text):
        tokens = text.split("_")
        last_logo_link = None
        for token in tokens:
            logo_link = self.get_crypto_logo(token)
            if logo_link:
                last_logo_link = logo_link
        return last_logo_link

    def get_crypto_logo(self, token_name, width=None, height=None):
        url = "https://cryptologos.cc/logos/"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                logo_links = soup.find_all("a", string=lambda text: token_name.lower() in text.lower())
                if logo_links:
                    logo_link = logo_links[0]['href']
                    if width and height:
                        logo_link += f"?width={width}&height={height}"
                    logger.info(f"Logo link retrieved for {token_name}: {logo_link}")
                    return logo_link
                else:
                    logger.warning(f"No logo found for {token_name}")
                    return None 
            else:
                logger.error("Failed to make the request.")
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")

import requests
from bs4 import BeautifulSoup

def get_crypto_logo(token_name, width=None, height=None):
    """
    Fetch the logo URL for a given cryptocurrency token name.

    Args:
    - token_name (str): The name of the cryptocurrency token.
    - width (int, optional): The width of the logo.
    - height (int, optional): The height of the logo.

    Returns:
    - str or None: The URL of the logo if found, otherwise None.
    """
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
                return logo_link
            else:
                return None 
        else:
            print("The request failed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def get_crypto_logo_from_table_str(text):
    """
    Parse a string of tokens separated by underscores and fetch the logo URL for each token.

    Args:
    - text (str): The input string containing tokens separated by underscores.

    Returns:
    - str or None: The URL of the last found logo if any, otherwise None.
    """
    tokens = text.split("_")
    last_logo_link = None
    for token in tokens:
        logo_link = get_crypto_logo(token)
        if logo_link:
            last_logo_link = logo_link
    return last_logo_link

if __name__ == "__main__":
    text = "DOGE"
    logo_link = get_crypto_logo_from_table_str(text)
    if logo_link:
        print(f"Logo URL: {logo_link}")
    else:
        print("No logo found.")

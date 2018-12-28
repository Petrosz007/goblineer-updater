from dotenv import load_dotenv
from os import getenv
import requests
from tqdm import tqdm


def get_oauth_token(client_id: str, client_secret: str, url: str='https://us.battle.net/oauth/token') -> str:
    """
    Fetches the OAuth token from the url

    Args:
        client_id: str: OAuth Client ID
        client_secret: str: OAuth Client Secret
        url: str: OAuth server URL, the default is the Blizzard OAuth Token URL
    
    Returns:
        str: The generated OAuth token
    
    Raises:
        TypeError: If the provided arguments are of the wrong type
        ValueError: If the data provided by the user is incorrect
        ConnectionError: Any other error that prevens connection to the API
    """

    # Type checking
    if not (isinstance(client_id, str) and isinstance(client_secret, str) and isinstance(url, str)):
        raise TypeError

    # Executing the request
    data = {
        'grant_type': 'client_credentials'
    }

    try:
        response = requests.post(url, data=data, auth=(client_id, client_secret))
    except requests.exceptions.ConnectionError as err:
        raise ConnectionError('Request make to Blizzard servers failed, are you sure you entered the correct client information? Error:', err)

    # Checking if the request is successful
    if not response.status_code == 200:
        if response.status_code == 401:
            raise ValueError('Invorrect client and/or secret. Please check that they are correct. HTTP error:', response.status_code)
        else:
            raise ConnectionError('Request make to Blizzard servers failed, are you sure you entered the correct client information? HTTP error:', response.status_code)

    # Returning the data
    return response.json()['access_token']


def get_auction_data_status(oauth_token: str, region: str, realm: str, locale: str='en_US') -> dict:
    """
    Fetches the status of the Auctionhouse data

    Args:
        oauth_token: str: OAuth Token
        region: str: Region of the realm
        realm: str: The realm of the data
        locale: str: The locale the data should be in, default is en_US
    
    Returns:
        dict: The time when the Auctionhouse data was last modified and the url of the data
    
    Raises:
        TypeError: If the provided arguments are of the wrong type
        ValueError: If the data provided by the user is incorrect
        ConnectionError: Any other error that prevens connection to the API
    """
    
    # Type checking
    if not (isinstance(oauth_token, str) and isinstance(region, str) and isinstance(realm, str) and isinstance(locale, str)):
        raise TypeError

    # Executing the request
    try:
        response = requests.get('https://{}.api.blizzard.com/wow/auction/data/{}?locale={}&access_token={}'.format(region, realm, locale, oauth_token))
    except requests.exceptions.ConnectionError as err:
        raise ConnectionError('Request make to Blizzard servers failed, are you sure you entered the correct client information? Error:', err)


    # Checking if the request is successful
    if not response.status_code == 200:
        if response.status_code == 401:
            raise ValueError('Invorrect client and/or secret. Please check that they are correct. HTTP error:', response.status_code)
        else:
            raise ConnectionError('Request make to Blizzard servers failed, are you sure you entered the correct client information? HTTP error:', response.status_code)

    # Returning the data
    return response.json()['files'][0]


def get_auction_data(url: str) -> dict:
    """
    Fetches the Auctionhouse data from the specified url

    Args:
        url: str: The url of the auction data
    
    Returns:
        dict: The auction data, converted to dict from json
    
    Raises:
        TypeError: If the provided arguments are of the wrong type
        ConnectionError: Any other error that prevens connection to the API
    """

    # Type checking
    if not isinstance(url, str):
        raise TypeError

    # Trying to execute the request
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError as err:
        raise ConnectionError('Request make to Blizzard servers failed, are you sure you entered the correct client information? Error:', err)


    # Checking if the request is successful
    if not response.status_code == 200:
        raise ConnectionError('Request make to Blizzard servers failed, are you sure you entered the correct client information? HTTP error:', response.status_code)

    # Returning the data
    return response.json()



def main():
    load_dotenv()

    oauth_token = get_oauth_token(getenv('OAUTH_CLIENT'), getenv('OAUTH_SECRET'))
    print(oauth_token)

    ah_status = get_auction_data_status(oauth_token, getenv("REGION"), getenv("REALM"), getenv("LOCALE"))
    print(ah_status)

    auction_data = get_auction_data(ah_status['url'])

    print('Done!')


if __name__ == "__main__":
    main()
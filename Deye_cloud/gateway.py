import os
import logging
import time
import requests
from dotenv import load_dotenv

load_dotenv()
API_URL= os.getenv('API_URL') 


access_token = 0
token_expiry = 0



def get_access_token():
    global access_token, token_expiry  # Declare the variables as global
 
    # Check if we already have a valid token
    if access_token and token_expiry > time.time():
        logging.info(f"Reusing existing access token. Token expires in {token_expiry - time.time():.2f} seconds.")
        return access_token


    # If the token is expired or not available, request a new one
    

    login_url = f"{API_URL}/token"
    payload = {
         'username': os.getenv('API_USER'),
         'password': os.getenv('API_PASS')
        # to run with getenv from termina paste following:
        # export API_USER='my_username'
        # export API_PASS='my_password'
    }

    if os.getenv('API_USER') == None or os.getenv('API_PASS') == None:
        logging.error("FAILED to  obtain user credentials using os.getenv method")
        return None

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        # Perform the POST request to fetch the token
        response = requests.post(login_url, data=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the JSON response
        token_data = response.json()
        access_token = token_data.get('access_token')
        print(access_token)
        expires_in = token_data.get('expires_in', 3600)  # Default to 1 hour if not provided

        if not access_token:
            raise ValueError("Access token not found in response.")

        # Set token expiration to expire a bit earlier to handle clock skew
        token_expiry = time.time() + expires_in - 10  # Subtracting 10 seconds

        logging.info(f"New access token retrieved, valid for {expires_in} seconds.")
        return access_token

    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP error occurred: {err}")
        logging.error(f"Response content: {response.text}")
    except ValueError as err:
        logging.error(f"Value error: {err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")

    return None 
get_access_token()
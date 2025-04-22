import requests
import os
import hashlib
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time
import logging

load_dotenv()
appId=os.getenv('APPID')
appSecret=os.getenv('APPSECRET')
email=os.getenv('EMAIL')
password=os.getenv('PASSWORD')


class ObtainToken:
    class Token:
        def __init__(self,access_token=None,refresh_token=None,expires_in=None):
            self.access_token= access_token
            self.refresh_token=refresh_token
            self.expires_in=expires_in
            self.token_expiry=0
    def __init__(self,appId,appSecret,email,password):
        self.appId=appId
        self.appSecret=appSecret
        self.email=email
        self.password=password
        self.token=self.Token()
    
        



    def encrypt_string(self,hash_string):
        sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
        return sha_signature
    
    def obtain_token(self):    
        if self.token and self.token.token_expiry>time.time():   #FIX THIS LINE IF TOKEN GIVES WRONG
            logging.info(f"Reusing existing access token. Token expires in {self.token.token_expiry - time.time():.2f} seconds.")
            return self.token
        hashed_password=self.encrypt_string(self.password)
        url = 'https://eu1-developer.deyecloud.com/v1.0/account/token?appId={}'.format(self.appId)
        headers = {
            'Content-Type': 'application/json'
        }
        # Body
        data = {
            "appSecret": self.appSecret,
            "email": self.email,  #email of DeyeCloud account
            "password":hashed_password,  #password of DeyeCloud account
        }
        if self.appId == None or self.appSecret == None:
            logging.error("FAILED to  obtain appID credentials using os.getenv method")
            return None

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  
                  
            data=response.json()
           
            self.token.access_token=data.get('accessToken')
            self.token.refresh_token=data.get('refreshToken')
            self.token.expires_in=int(data.get('expiresIn'))
            self.token.token_expiry=time.time() + self.token.expires_in-10
            if not self.token.access_token:
                raise ValueError("Access token not found in response.")
            logging.info(f"New access token retrieved, valid for {self.token.expires_in} seconds.")
            return self.token
        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTP error occurred: {err}")
            logging.error(f"Response content: {response.text}")
        except ValueError as err:
            logging.error(f"Value error: {err}")
        except Exception as err:
            logging.error(f"An error occurred: {err}")
        return None 

    def __str__(self):
        return self.appId

##TESTING
if(__name__=="__main__"):
    token=ObtainToken(appId=appId,appSecret=appSecret,email=email,password=password)
    obtained=token.obtain_token()
    print(obtained.access_token)
    time.sleep(10)
    obtained=token.obtain_token()
    print(obtained.access_token)
    

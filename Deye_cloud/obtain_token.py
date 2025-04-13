import requests
import os
import hashlib
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
appId=os.getenv('APPID')
appSecret=os.getenv('APPSECRET')
email=os.getenv('EMAIL')
password=os.getenv('PASSWORD')


class ObtainToken:
    def __init__(self,appId,appSecret,email,password):
        self.appId=appId
        self.appSecret=appSecret
        self.email=email
        self.password=password
    class Token:
        def __init__(self,access_token,refresh_token,expires_in):
            self.access_token= access_token
            self.refresh_token=refresh_token
            self.expires_in=expires_in
            self.expiery_date=datetime.now() + timedelta(seconds=int(expires_in))
        def is_expired(self):
            """Check if the token has expired"""
            return datetime.now() >= self.expiery_date
        



    def encrypt_string(self,hash_string):
        sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
        return sha_signature
    
    def obtain_token(self):    
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
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  
                  
            data=response.json()
           
            access_token=data.get('accessToken')
            refresh_token=data.get('refreshToken')
            expires_in=data.get('expiresIn')
            return self.Token(access_token=access_token,refresh_token=refresh_token,expires_in=expires_in)
            

        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as err:
            print(f"Other error occurred: {err}")

    def refresh_token(self, refresh_token):
            """Refresh an expired access token using the refresh token"""
            url = 'https://eu1-developer.deyecloud.com/v1.0/account/token/refresh'
            headers = {
                'Content-Type': 'application/json'
            }
            # Body
            data = {
                "appId": self.appId,
                "appSecret": self.appSecret,
                "refreshToken": refresh_token
            }
            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                
                data = response.json()
                
                access_token = data.get('accessToken')
                new_refresh_token = data.get('refreshToken')  # Some services return a new refresh token
                expires_in = data.get('expiresIn')
                
                # Use the new refresh token if provided, otherwise keep the old one
                effective_refresh_token = new_refresh_token if new_refresh_token else refresh_token
                
                return self.Token(access_token=access_token, 
                                refresh_token=effective_refresh_token, 
                                expires_in=expires_in)
                
            except requests.exceptions.HTTPError as err:
                print(f"HTTP error occurred while refreshing token: {err}")
                # If refresh fails, you might want to get a brand new token
                return self.obtain_token()
            except Exception as err:
                print(f"Other error occurred while refreshing token: {err}")
                return None



    def __str__(self):
        return self.appId

##TESTING
if(__name__=="__main__"):
    token=ObtainToken(appId=appId,appSecret=appSecret,email=email,password=password)
    obtained_token=token.obtain_token()
    print(obtained_token.expiery_date)
    print(obtained_token.access_token)
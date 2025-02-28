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
            self.access_token=access_token
            self.refresh_token=refresh_token
            self.expires_in=expires_in
            self.expiery_date=datetime.now() + timedelta(seconds=int(expires_in))
        
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
            # print response status
            print(response.status_code)
            data=response.json()
            access_token=data.get('accessToken')
            refresh_token=data.get('refreshToken')
            expires_in=data.get('expiresIn')
            return self.Token(access_token=access_token,refresh_token=refresh_token,expires_in=expires_in)
            

        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
    def __str__(self):
        return self.appId

##TESTING

# token=ObtainToken(appId=appId,appSecret=appSecret,email=email,password=password)
# print(token)
# token.obtain_token()
# print(token.expiery_date)
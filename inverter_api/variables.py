from obtain_token import ObtainToken
import obtain_token
from dotenv import load_dotenv
import os

#User Credentials


class Variables:
    def __init__(self):
        
        load_dotenv()
        self.appId=os.getenv('APPID')
        self.appSecret=os.getenv('APPSECRET')
        self.email=os.getenv('EMAIL')
        self.password=os.getenv('PASSWORD')
        self.token=ObtainToken(appId=self.appId,appSecret=self.appSecret,email=self.email,password=self.password)
        self.new_token=self.token.obtain_token()
        self.baseurl = "https://eu1-developer.deyecloud.com/v1.0"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'bearer ' + self.new_token.access_token
        }
from obtain_token import ObtainToken
import obtain_token
from dotenv import load_dotenv
import os

#User Credentials


class Variables:
    def __init__(self,battery_id=2):
        load_dotenv()
        self.appId=os.getenv(f'BAT{battery_id}_APP_ID')
        self.appSecret=os.getenv(f'BAT{battery_id}_APP_SECRET')
        self.email=os.getenv(f'BAT{battery_id}_EMAIL')
        self.password=os.getenv('PASSWORD')
        self.token=ObtainToken(appId=self.appId,appSecret=self.appSecret,email=self.email,password=self.password)
        self.new_token=self.token.obtain_token()
        self.baseurl = "https://eu1-developer.deyecloud.com/v1.0"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'bearer ' + self.new_token.access_token
        }
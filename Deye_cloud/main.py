from dotenv import load_dotenv
from gateway import MainController
from gateway import APIToken
import time
import threading 

import os
load_dotenv()

api_url= os.getenv('API_URL') 
username=os.getenv('API_USER')
password= os.getenv('API_PASS')

c=MainController(api_url=api_url,username=username,password=password)

def action():
    while True:
       c.action_controller()
       time.sleep(60)

def history():
    while True:
        c.history_controller(2)
        time.sleep(1)

battery_controll_thread=threading.Thread(target=action)
history_fetching_thread=threading.Thread(target=history)

battery_controll_thread.start()
history_fetching_thread.start()





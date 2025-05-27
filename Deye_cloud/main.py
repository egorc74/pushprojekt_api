from dotenv import load_dotenv
from gateway import MainController
import time
import threading
import os
import logging
logging.basicConfig(filename='logging/inverter.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

load_dotenv()

api_url = os.getenv('API_URL') 
username = os.getenv('API_USER')
password = os.getenv('API_PASS')

c = MainController(api_url=api_url, username=username, password=password)

# Global flag to control thread execution
running = True

def action(battery_list):
    last_time=0
    while running:
        current_time=time.time()
        if (current_time-last_time>=60): 
            last_time=current_time      
            for battery in battery_list:
                c.action_controller(battery)

            
def history(battery_list):
    last_time=0
    while running:
        current_time=time.time()
        if (current_time-last_time>=60): 
            last_time=current_time      
            for battery in battery_list:
                c.history_controller(battery_id=battery)

def get_battery_list():
    list=c.get_battery_list()
    return list


if __name__ == "__main__":
    battery_list=get_battery_list()
    logging.info(f"get_battery_list:{battery_list}")
    battery_control_thread = threading.Thread(target=action,args=(battery_list,))
    history_fetching_thread = threading.Thread(target=history,args=(battery_list,))
    battery_control_thread.start()
    history_fetching_thread.start()

    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        print("\nShutting down threads...")
        running = False  # Signal threads to stop
        battery_control_thread.join()  # Wait for thread to finish
        history_fetching_thread.join()  # Wait for thread to finish
        print("All threads stopped. Exiting.")
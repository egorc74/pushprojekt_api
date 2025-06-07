from dotenv import load_dotenv
from gateway import MainController
import time
import threading
import os
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

load_dotenv()

api_url = os.getenv('API_URL')
username = os.getenv('API_USER')
password = os.getenv('API_PASS')

c = MainController(api_url=api_url, username=username, password=password)

# Global flag to control thread execution
running = True

def action():
    last_time=0
    while running:
        current_time=time.time()
        if (current_time-last_time>=60):
            last_time=current_time
            battery_list=[]
            battery_list = get_battery_list()  # Get fresh battery list every minute
            if (len(battery_list)>0):
                logging.info(f"get_battery_list:Succesfully received battery list:{battery_list}")
                for battery in battery_list:
                    c.change_battery_id(battery['id'])  # Set the correct battery_id for this battery
                    c.action_controller(battery['id'])
            else:
                logging.info(f"get_battery_list:Battery list is empty:{battery_list}")



def history():
    time.sleep(1) #delay betwee threads 
    last_time=0
    while running:
        current_time=time.time()
        if (current_time-last_time>=60):
            last_time=current_time
            battery_list=[]
            battery_list = get_battery_list()  # Get fresh battery list every minute
            if (len(battery_list)>0):
                logging.info(f"get_battery_list:Succesfully received battery list:{battery_list}")
                for battery in battery_list:
                    c.change_battery_id(battery['id'])  # Set the correct battery_id for this battery
                    c.history_controller(battery_id=battery['id'])
            else:
                logging.info(f"get_battery_list:Battery list is empty:{battery_list}")

            

def get_battery_list():
    list=c.get_battery_list()
    return list


if __name__ == "__main__":
    battery_control_thread = threading.Thread(target=action)
    history_fetching_thread = threading.Thread(target=history)
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
from dotenv import load_dotenv
from gateway import MainController
import time
import threading
import os
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

load_dotenv()

api_url = os.getenv('API_URL')
username = os.getenv('API_USER')
password = os.getenv('API_PASS')

c = MainController(api_url=api_url, username=username, password=password)

running = True  # Global flag to control thread execution


def ensure_battery_list_dir():
    os.makedirs("battery_lists", exist_ok=True)


def get_battery_list():
    return c.get_battery_list()


def read_cached_battery_list():
    try:
        with open("battery_lists/latest_battery_list.json", "r") as f:
            data = json.load(f)
            logging.info(f"get_battery_list:Battery list is empty, opened the latest battery list: {data}")
            return data
    except FileNotFoundError:
        logging.warning("No previous battery list file found. Skipping this iteration.")
        return []


def action():
    ensure_battery_list_dir()
    last_time = 0
    while running:
        current_time = time.time()
        if current_time - last_time >= 60:
            last_time = current_time
            try:
                battery_list = get_battery_list()
                if battery_list:
                    logging.info(f"get_battery_list: Successfully received battery list: {battery_list}")
                    with open("battery_lists/latest_battery_list.json", "w") as f:
                        json.dump(battery_list, f, indent=4)
                else:
                    battery_list = read_cached_battery_list()

                for battery in battery_list:
                    c.change_battery_id(battery['id'])
                    c.action_controller(battery['id'])
            except Exception as e:
                logging.error(f"Error in action Thread: {e}")


def history():
    ensure_battery_list_dir()
    time.sleep(1)  # delay between threads
    last_time = 0
    while running:
        current_time = time.time()
        if current_time - last_time >= 60:
            last_time = current_time
            try:
                battery_list = get_battery_list()
                if battery_list:
                    logging.info(f"get_battery_list: Successfully received battery list: {battery_list}")
                    with open("battery_lists/latest_battery_list.json", "w") as f:
                        json.dump(battery_list, f, indent=4)
                else:
                    battery_list = read_cached_battery_list()

                for battery in battery_list:
                    c.change_battery_id(battery['id'])
                    c.history_controller(battery['id'])
            except Exception as e:
                logging.error(f"Error in history Thread: {e}")


if __name__ == "__main__":
    battery_control_thread = threading.Thread(target=action)
    history_fetching_thread = threading.Thread(target=history)

    battery_control_thread.start()
    history_fetching_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down threads...")
        running = False
        battery_control_thread.join()
        history_fetching_thread.join()
        print("All threads stopped. Exiting.")

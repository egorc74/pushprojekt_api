import os
from dotenv import load_dotenv
from gateway import MainController
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()
api_url = os.getenv('API_URL')
username = os.getenv('API_USER')
password = os.getenv('API_PASS')

def main():
    # Initialize controller
    controller = MainController(api_url=api_url, username=username, password=password)
    
    # Get battery list
    batteries = controller.get_battery_list()   
    if not batteries:
        logging.error("Failed to get battery list")
        return
    
    # Print battery information
    for battery in batteries:
        logging.info("\nBattery Information:")
        logging.info(f"ID: {battery.get('id')}")
        logging.info(f"Name: {battery.get('name')}")
        logging.info(f"Serial Number: {battery.get('serial_number')}")
        
        # Initialize commission for this battery
        controller.change_battery_id(battery.get('id'))
        
        # Get battery configuration from Deye
        logging.info("\nChecking Deye API for battery configuration...")
        controller.commission.update_serial(sn=battery.get('serial_number'))
        
        # Get battery config
        logging.info("\nBattery Configuration:")
        controller.commission.battery_config()
        
        # Get system config
        logging.info("\nSystem Configuration:")
        controller.commission.system_config()
        
        # Get current battery state
        logging.info("\nCurrent Battery State:")
        response = controller.commission.get_lattest_history()
        if response and 'deviceDataList' in response:
            for data in response['deviceDataList'][0]['dataList']:
                if data['key'] in ['SOC', 'BatteryPower', 'BatteryCurrent', 'BatteryVoltage', 'BMSChargeVoltage', 'BMSDisChargeVoltage']:
                    logging.info(f"{data['key']}: {data['value']} {data['unit']}")
        
        # Try to change system mode to LOAD_FIRST
        logging.info("\nAttempting to change system mode to LOAD_FIRST...")
        try:
            # First change energy pattern
            controller.commission.sys_energy_pattern_update("LOAD_FIRST")
            logging.info("Energy pattern change command sent")
            
            # Then change work mode
            controller.commission.sys_work_mode_update("LOAD_FIRST")
            logging.info("Work mode change command sent")
            
            # Wait a moment and check the new configuration
            time.sleep(5)
            logging.info("\nChecking new system configuration:")
            controller.commission.system_config()
            
        except Exception as e:
            logging.error(f"Failed to change system mode: {e}")

if __name__ == "__main__":
    main() 
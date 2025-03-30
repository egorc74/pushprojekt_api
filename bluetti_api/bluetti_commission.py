from dotenv import load_dotenv
import os

import hashlib
import secrets
import time
import json
import requests
from typing import Dict, Any



class BluettiClient:
    
    def __init__(self, app_key: str, app_secret: str, device_sn: str):
        self.app_key = app_key
        self.app_secret = app_secret
        self.device_sn = device_sn
        self.function_codes = {
    "system_control": {
        "min": 0,
        "max": 3,
        "description": "System control (1: Off grid, 2: Grid connected)"
    },
    "active_power_of_L1_phase_inverter": {
        "min": -10000,
        "max": 10000,
        "description": "Active power L1"
    },
    "reactive_power_of_L1_phase_inverter": {
        "min": -10000,
        "max": 10000,
        "description": "Reactive power L1"
    },
    "active_power_of_L2_phase_inverter": {
        "min": -10000,
        "max": 10000,
        "description": "Active power L2"
    },
    "reactive_power_of_L2_phase_inverter": {
        "min": -10000,
        "max": 10000,
        "description": "Reactive power L2"
    },
    "active_power_of_L3_phase_inverter": {
        "min": -10000,
        "max": 10000,
        "description": "Active power L3"
    },
    "reactive_power_of_L3_phase_inverter": {
        "min": -10000,
        "max": 10000,
        "description": "Reactive power L3"
    }
    }
    def generate_nonce(self) -> str:
        return secrets.token_hex(16)

    def get_timestamp(self) -> int:
        return int(time.time())

    def create_signature(self, nonce_str: str, timestamp: int) -> str:
        raw_string = f"appKey={self.app_key}&appSecret={self.app_secret}&nonceStr={nonce_str}&timeStamp={timestamp}"
        return hashlib.sha256(raw_string.encode()).hexdigest().upper()



    def change_settings(self, function_code: str, set_value: float):
        nonce_str = self.generate_nonce()
        timestamp = self.get_timestamp()
        signature = self.create_signature(nonce_str, timestamp)
        headers = {
            'Authorization': signature,
            'Date': str(timestamp),
            'ETag': nonce_str,
            'x-app-key': self.app_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # Format the value according to function code
        if function_code == "system_control":
            formatted_value = str(set_value).rjust(2, '0')
        else:
            formatted_value = f"{set_value:.1f}"

        request_body = {
            'deviceSn': self.device_sn,
            'functionCode': function_code,
            'setValue': formatted_value
        }

        print("Sending Request:", json.dumps(request_body, indent=2, ensure_ascii=False))

        try:
            response = requests.post(
                'https://open.bluetti.com/open/bluiotdata/device/telemetry/v1/telemetryDeviceSetUp',
                json=request_body,
                headers=headers
            )
            response.raise_for_status()
            print('Setting Updated:', json.dumps(response.json(), indent=2, ensure_ascii=False))
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            if e.response is not None:
                try:
                    error_data = e.response.json()
                    print('Response:', json.dumps(error_data, indent=2, ensure_ascii=False))
                    return error_data
                except json.JSONDecodeError:
                    print('Response:', e.response.text)
    def get_data(self,  pageNo, pageSize, start_time=int((time.time()-24*3600)*1000), end_time=int(time.time()*1000)):
        nonce_str = self.generate_nonce()
        timestamp = self.get_timestamp()
        signature = self.create_signature(nonce_str, timestamp)
        headers = {
            'Authorization': signature,
            'Date': str(timestamp),
            'ETag': nonce_str,
            'x-app-key': self.app_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        request_body = {
            'beginTimestamp': start_time,
            'deviceSn': self.device_sn,
            'endTimestamp': end_time,
            'pageNo': pageNo,
            'pageSize': pageSize
        }

        print("Sending Request:", json.dumps(request_body, indent=2, ensure_ascii=False))

        try:
            response = requests.post(
                'https://open.bluetti.com/open/bluiotdata/device/telemetry/v1/telemetryDeviceReportedData',
                json=request_body,
                headers=headers
            )
            response.raise_for_status()
            print('Setting Updated:', json.dumps(response.json(), indent=2, ensure_ascii=False))
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            if e.response is not None:
                try:
                    error_data = e.response.json()
                    print('Response:', json.dumps(error_data, indent=2, ensure_ascii=False))
                    return error_data
                except json.JSONDecodeError:
                    print('Response:', e.response.text)

if __name__ == "__main__":
    # Configuration
    load_dotenv()

    APP_KEY =os.getenv('APP_KEY')   # Add your app key
    APP_SECRET = os.getenv('APP_SECRET')  # Add your app secret
    DEVICE_SN = os.getenv('TEST_DEVICE_SN')  # Add your device SN



    # Initialize and start client
    client = BluettiClient(APP_KEY, APP_SECRET, DEVICE_SN) 
    client.get_data(1,10)

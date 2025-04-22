import os
import logging
import time
import requests
from dotenv import load_dotenv
from commision import Commision

load_dotenv()
api_url= os.getenv('API_URL') 
username=os.getenv('API_USER')
password= os.getenv('API_PASS')

class APIToken:
    class Token:
        def __init__(self,access_token=None,token_expiry=None):
            self.access_token=access_token
            self.token_expiry=0
            self.expires_in=0
    def __init__(self,url,username,password):
        self.api_url=url
        self.username=username
        self.password=password
        self.token=self.Token()
    
    def get_access_token(self):
        if self.token and self.token.token_expiry > time.time():
            logging.info(f"Reusing existing access token. Token expires in {self.token.token_expiry - time.time():.2f} seconds.")
            return self.token.access_token     

        login_url = f"{self.api_url}/token"
        payload = {
            'username': self.username,
            'password': self.password
        }

        if self.username == None or self.password == None:
            logging.error("FAILED to  obtain user credentials using os.getenv method")
            return None

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            # Perform the POST request to fetch the token
            response = requests.post(login_url, data=payload, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes

            # Parse the JSON response
            token_data = response.json()
            self.token.access_token = token_data.get('access_token')
            print(self.token.access_token)
            self.token.expires_in = token_data.get('expires_in', 3600)  # Default to 1 hour if not provided

            if not self.token.access_token:
                raise ValueError("Access token not found in response.")
            logging.info(f"New access token retrieved, valid for {self.token.expires_in} seconds.")

            # Set token expiration to expire a bit earlier to handle clock skew
            self.token_expiry = time.time() + self.token.expires_in - 10  # Subtracting 10 seconds

            return self.token.access_token

        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTP error occurred: {err}")
            logging.error(f"Response content: {response.text}")
        except ValueError as err:
            logging.error(f"Value error: {err}")
        except Exception as err:
            logging.error(f"An error occurred: {err}")
        return None 
    


class MainController:
    def __init__(self,api_url,username,password):
        self.apitoken=APIToken(url=api_url,username=username,password=password)
        self.api_url=api_url
        self.username=username
        self.password=password
        self.commission=Commision()
    def get_token(self):
        return self.apitoken.get_access_token()


##READING BATTERY ACTIONS AND CONTROLL THEM


    def patch_action(self,id,status):
        try:
            url= f"{self.api_url}/battery-actions/{id}"
            if status:
                payload = {
                    "action_executed":True
                }
            else:
                payload = {
                    "action_executed":False
                }
            token=self.get_token()
            headers = {'Authorization': f'Bearer {token}'}
            response=requests.patch(url=url,headers=headers,data=payload)
            response.raise_for_status()
            data=response.json()
            success=data[0]["action_executed"]
            if success:
                return success
            else:
                raise Exception(f"Patching was not succesfull for request id{id}")
        except Exception as err:
            logging.error(f"An error occurred: {err}")
        return None

    def controll_battery(self,action,power,battery_id=2):
        try:
            serial_number="2407264006"
            self.commission.update_serial(sn=serial_number)
            if(action==-1):
                response=self.commission.battery_discharge(power=power)
                success=response.get('success')
                if(success==True):
                    return success
                else:
                    raise Exception(f"Unsuccessful command{success}")
            if(action==0):
                response=self.commission.battery_stop()
                success=response.get('success')
                if(success==True):
                    return success
                else:
                    raise Exception(f"Unsuccessful command{success}")
            if(action==-1):
                response=self.commission.battery_charge(power=power)
                success=response.get('success')
                if(success==True):
                    return success
                else:
                    raise Exception(f"Unsuccessful command{success}")
        except Exception as e: 
            print(f"An unexpected error occurred: {e}")     

            
            

    def get_battery_action(self,battery_id): #returns [battery_id,action,power]
        url= f"{self.api_url}/battery-actions?battery_id={battery_id}&action_executed=false"
        
        token=self.get_token()
        headers = {'Authorization': f'Bearer {token}'}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()
            
            id=data[0]["id"]
            battery_id=data[0]["battery_id"]
            action=data[0]["action"]
            power=data[0]["target_power"]
            if (id==None):
                logging.error(f"Error in retrieving id of order{data}")
            return [id,battery_id,action,power]


        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTP error occurred: {err}")
            logging.error(f"Response content: {response.text}")
        except ValueError as err:
            logging.error(f"Value error: {err}")
        except Exception as err:
            logging.error(f"An error occurred: {err}")
        return None 



    def action_controller(self): #main function
        try:
            actions=self.get_battery_action(self,2)
            success=self.controll_battery(batery_id=actions[1],action=actions[2],power=actions[3])
            result=self.patch_action(self,id=actions[0],status=success)
            if not result: 
                raise Exception(f"Action controller was unsuccessful. Actions retrieved from EMS:{actions}")
            logging.info(f"Action was succesfuly executed and patched. actions:{actions},execution success:{success},patching result{result}")
        except Exception as err:
            logging.error(f"Unknown error occured{err}")



##RETRIEVING CURRENT PRODUCTION RECORDS AND SAVING THEM IN SYSTEM
    def get_power_records(self,battery_id):     #TODo update parameters
        serial_number="2407264006"
        self.commission.update_serial(sn=serial_number)
        history=self.commission.get_lattest_history()
        return history
        # try:
        #     for  item in history["deviceDataList"][0]["dataList"]:
        #         if item["key"] =="SOC": soc_value=item["value"] 
        #         if item["key"] =="BatteryVoltage": voltage_value=item["value"] 
        #         if item["key"] =="BatteryPower": power_value=item["value"] 
        #         if item["key"] =="BatteryCurrent": current_value=item["value"] 
        #         if item["key"] =="SOC": soc_value=item["value"] 
        #     params={
        #         "soc":int(soc_value),
        #         "power":int(power_value),
        #         "voltage":int(voltage_value),
        #         "current":int(current_value),
        #     }

        # except StopIteration as err:
        #     print(f"{err} not found in data!")
        # except (KeyError, IndexError) as err:
        #     print(f"{err}Invalid data structure!")
        # except ValueError as err:
        #     print(f"{err} is not a valid number!")
    

    def fetch_power_records(self,battery_id,records):
        url= f"{self.api_url}/battery-records"
        token=self.get_token()
        headers = {'Authorization': f'Bearer {token}'}
        params={'battery_id':battery_id,
                'location_id':0,
                'data':records,
        }
        try:
            response = requests.post(url,data=params, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            logging.info(f"Records were succesfully fetched{response.json()}")

        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTP error occurred: {err}")
            logging.error(f"Response content: {response.text}")
        except ValueError as err:
            logging.error(f"Value error: {err}")
        except Exception as err:
            logging.error(f"An error occurred: {err}")
        return None 
    
    def history_controller(self,battery_id):
            records=self.get_power_records(battery_id)
            self.fetch_power_records(battery_id,records=records)   
            

        
        
       




        




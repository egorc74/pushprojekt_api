import os
import logging
import time
import requests
import json
from dotenv import load_dotenv
from commision import Commision
from datetime import datetime
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
        if self.token.access_token and self.token.token_expiry > time.time():
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
            self.token.expires_in = token_data.get('expires_in', 3600)  # Default to 1 hour if not provided

            if not self.token.access_token:
                raise ValueError("Access token not found in response.")
           
            # Set token expiration to expire a bit earlier to handle clock skew
            self.token.token_expiry = time.time() + self.token.expires_in - 10  # Subtracting 10 seconds
            logging.info(f"New access token retrieved, valid for {self.token.expires_in},current time{time.time()}, seconds until {self.token.token_expiry}.")

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
    def __init__(self,api_url,username,password,battery_id):
        self.apitoken=APIToken(url=api_url,username=username,password=password)
        self.api_url=api_url
        self.username=username
        self.password=password
        self.commission=Commision(battery_id=battery_id)
    def get_token(self):
        return self.apitoken.get_access_token()

    def change_battery_id(self,battery_id):
        self.commission=Commision(battery_id=battery_id)

##GET LIST OF BATTARIES
    def get_battery_list(self):
        url=f"{self.api_url}/batteries"
        token=self.get_token()
        headers = {'Authorization': f'Bearer {token}'}
        try:
            params = {
                # Optional parameters:
                "skip": 0,
                "limit": 10,
                "sort_by": "name",
                "sort_order": "asc"
            }

            response = requests.get(url, headers=headers,params=params)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()  # Decodes JSON automatically
            battery_list = [item['id'] for item in data]
   
            return battery_list


        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTP error occurred: {err}")
            logging.error(f"Response content: {response.text}")
        except ValueError as err:
            logging.error(f"Value error: {err}")
        except Exception as err:
            logging.error(f"An error occurred: {err}")
        return None 





##READING BATTERY ACTIONS AND CONTROLL THEM

    def get_battery_action(self,battery_id): #returns [battery_id,action,power]
            url= f"{self.api_url}/battery-actions?battery_id={battery_id}&action_executed=false"
            
            token=self.get_token()
            headers = {'Authorization': f'Bearer {token}'}
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise an error for bad status codes
                data = response.json()
                if data:
                    logging.info(f"get_battery_actions:Succesffuly received battery actions:{data}")
                    id=data[0]["id"]
                    if (id==None):
                        logging.error(f"Error in retrieving id of order{data}")
                    battery_id=data[0]["battery_id"]
                    action=data[0]["action"]
                    power=data[0]["target_power"]
                    return [id,battery_id,action,power]

                else: 
                    logging.error(f"get_battery_actions:Error in receiving actions{data}")

                    return 0


            except requests.exceptions.HTTPError as err:
                logging.error(f"get_battery_actions:HTTP error occurred: {err}")
                logging.error(f"get_battery_actions:Response content: {response.text}")
            except ValueError as err:
                logging.error(f"get_battery_actions:Value error: {err}")
            except Exception as err:
                logging.error(f"get_battery_actions:An error occurred: {err}")
            return None 


    def controll_battery(self,action,power,battery_id=2):
        try:
            serial_number="2407264006"
            self.commission.update_serial(sn=serial_number)
            if(action==-1):
                response=self.commission.battery_discharge(power=power)
                success=response.get('success')
                if(success==True):
                    logging.info(f"controll_battery:response from sending actions{response}")
                    return success
                else:
                    logging.error(f"controll_battery:response from sending actions{response}")
                    raise Exception(f"controll_battery:Unsuccessful command{success}")

            if(action==0):
                response=self.commission.battery_stop()
                success=response.get('success')

                if(success==True):
                    logging.info(f"controll_battery:response from sending actions{response}")
                    return success
                else:
                    logging.error(f"controll_battery:response from sending actions{response}")
                    raise Exception(f"controll_battery:Unsuccessful command{success}")
            if(action==1):
                response=self.commission.battery_charge(power=power)
                success=response.get('success')

                if(success==True):
                    logging.info(f"controll_battery:response from sending actions{response}")
                    return success
                else:
                    logging.error(f"controll_battery:response from sending actions{response}")
                    raise Exception(f"controll_battery:Unsuccessful command{success}")
        except Exception as e: 
            logging.info(f"controll_battery:An unexpected error occurred: {e}")     

    def patch_action(self,id,status):
        try:
            url= f"{self.api_url}/battery-actions/{id}"
            if status:
                payload = {
                    "action_executed":True
                }
            else:
                ##IF BATTERY DOESNT RESPOND POST 0 POWER AND ERROR
                # self.post_battery_disconnection(battery_id=id)
                payload = {
                    "action_executed":False
                }
            token=self.get_token()
            headers = {'Authorization': f'Bearer {token}'}
            response=requests.patch(url=url,headers=headers,data=json.dumps(payload))
            response.raise_for_status()
            data=response.json()
            logging.info(f"patch_actions:response from patching actions{data}")
            success=data[0]["action_executed"]
            if success:
                return success
            else:
                raise Exception(f"patch_action:Patching was not succesfull for request id{id}")

        except requests.exceptions.HTTPError as errh:
            print(f"patch_action:HTTP Error: {errh}")
            if response.text:
                print("patch_action:Error details:", response.json())
        except requests.exceptions.RequestException as err:
            print(f"patch_action:Request Error: {err}")
        except ValueError as json_err:
            print(f"patch_action:JSON Decode Error: {json_err}")

            

    


    def action_controller(self,bat): #main function
        try:
            result=0
            actions=self.get_battery_action(battery_id=bat)
            if actions:
                success=self.controll_battery(battery_id=actions[1],action=actions[2],power=4000)
                result=self.patch_action(id=actions[0],status=success)
            if not result: 
                raise Exception(f"action_controller:Action controller was unsuccessful. Actions retrieved from EMS:{actions}")
            logging.info(f"action_controller:Action was succesfuly executed and patched. actions:{actions},execution success:{success},patching result{result}")
        except requests.exceptions.HTTPError as err:
            logging.error(f"action_controller:HTTP error occurred: {err}")
            logging.error(f"action_controller:Response content: {result.text}")
        except ValueError as err:
            logging.error(f"action_controller:Value error: {err}")
        except Exception as err:
            logging.error(f"action_controller:An error occurred: {err}")
        return None 
                



##RETRIEVING CURRENT PRODUCTION RECORDS AND SAVING THEM IN SYSTEM
    def get_power_records(self,battery_id):     #TODo update parameters
        serial_number="2407264006"
        self.commission.update_serial(sn=serial_number)
        try:
            response=self.commission.get_lattest_history()
            logging.info(f"get_power_records:Records were succesfully received{response}")
            return response

        except requests.exceptions.HTTPError as err:
            logging.error(f"get_power_records:HTTP error occurred: {err}")
            logging.error(f"get_power_records:Response content: {response.text}")
        except ValueError as err:
            logging.error(f"get_power_records:Value error: {err}")
        except Exception as err:
            logging.error(f"get_power_records:An error occurred: {err}")
        return None 
                

    def fetch_power_records(self,battery_id,records):
        url= f"{self.api_url}/battery-records/raw"
        token=self.get_token()
        headers = {'Authorization': f'Bearer {token}'}
        records['battery_id']=battery_id
        try:
            response = requests.post(url,data=json.dumps(records), headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            logging.info(f"fetch_power_records:Records were succesfully fetched{response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as err:
            logging.error(f"fetch_power_records:HTTP error occurred: {err}")
            logging.error(f"fetch_power_records:Response content: {response.text}")
        except ValueError as err:
            logging.error(f"fetch_power_records:Value error: {err}")
        except Exception as err:
            logging.error(f"fetch_power_records:An error occurred: {err}")
        return None 
    
    def post_battery_disconnection(self,battery_id,battery_location_id=""):
        url= f"{self.api_url}/battery-records/"
        token=self.get_token()
        headers = {'Authorization': f'Bearer {token}'}


        payload = {
            "battery_id": battery_id,
            "location_id": battery_location_id,
            "timestamp": datetime.utcnow().isoformat(),
            "soc": 0,
            "soh": 0,
            "power": 0,
            "voltage": 0,
            "current": 0,
            "temperature":0,
            "state": 0,
            "error_code":"400 battery is disconnected"
        }

        try:
            response = requests.post(url,data=json.dumps(payload), headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            logging.info(f"Records were succesfully fetched{response.json()}")
            return response.json()
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
            response=self.fetch_power_records(battery_id,records=records)   


if __name__=="__main__":
    c=MainController(api_url=api_url,username=username,password=password)
    print(c.get_power_records(1))

    

        
        
       




        




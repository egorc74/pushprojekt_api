from variables import Variables
import requests
import json
import time
from datetime import datetime, timedelta
import logging

class Commision:
    def __init__(self,serial_number="",station_id="",battery_id=None):
        self.serial_number=serial_number
        self.variable=Variables(battery_id=battery_id)
        self.station_id=station_id

    def update_serial(self,sn):
        self.serial_number=sn

    def device_measure_points(self,device_type="INVERTER"):
        url = self.variable.baseurl + '/device/measurePoints'
        headers = self.variable.headers
        data = {
            "deviceSn": self.serial_number,
            "deviceType": device_type
        }
        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())

    def tou_config(self):
        url = self.variable.baseurl + '/config/tou'
        headers = self.variable.headers

        data = {
            "deviceSn": self.serial_number,
        }

        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())

    """Returns history data for devices at different granularities.
granularity=1: the field 'startAt' should be in format 'yyyy-MM-dd'. Field 'measurePoints' has to be passed. Returns measure-point data for the day specified by 'startAt'
granularity=2: the field 'startAt' and 'endAt' should be in format 'yyyy-MM-dd'. Returns statistics data between 'startAt' and 'endAt' (up to 31 days) with intervals of one day
granularity=3: the field 'startAt' and 'endAt' should be in format 'yyyy-MM'. Returns statistics data between 'startAt' and 'endAt' (up to 12 months) with intervals of one month
granularity=4: the field 'startAt' and 'endAt' should be in format 'yyyy'. Returns yearly statistics data between 'startAt' and 'endAt'
Value for field of 'measurePoints' could be got through endpint '/v1.0/device/measurePoints'"""

    def station_history(self,startAt,granularity=1,endAt="null"):
        url = self.variable.baseurl + 'station/history'
        headers = self.variable.headers

        data = {
            "deviceSn": self.serial_number,
            "startAt":startAt,
            "endAt":endAt,
            "granularity":granularity
        }

        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())

    """timestamps in seconds from now"""
    def station_history_power(self,startTimestamp=600,endTimestamp=0):
        url = self.variable.baseurl + 'station/history/power'
        headers = self.variable.headers

        data = {
            "stationId": self.station_id,
            "starTimestamp":startTimestamp,
            "endTimestamp":endTimestamp,
        }

        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())

    """ Enable or disable the chargeMode """
    def battery_mode_control(self,action,mode_type=""):
        url = self.variable.baseurl + '/order/battery/modeControl'
        headers = self.variable.headers
        data = {
            "deviceSn": self.serial_number,
            "batteryModeType": mode_type,
            "action": action
        }
        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())
        return response.json()

    """
    Set the value for MAX_CHARGE_CURRENT and MAX_DISCHARGE_CURRENT
    e.g.Field paramterType=MAX_CHARGE_CURRENT, Field value=the value you want to set
    PARAMS:MAX_CHARGE_CURRENT, MAX_DISCHARGE_CURRENT, GRID_CHARGE_AMPERE, BATT_LOW
    VALUE: int64
    """

    def battery_parameter_update(self,parameter_type,value):
        url = self.variable.baseurl + '/order/battery/parameter/update'
        headers = self.variable.headers
        data = {
            "deviceSn": self.serial_number,
            "paramterType": parameter_type,
            "value": value
        }

        response = requests.post(url, headers=headers, json=data)
        print(response.status_code)
        print(response.json())

    """
    If the inverter type is Three phase LV Hybrid or Single phase LV Hybrid, 4 battery types supported: BATT_V;
    BATT_SOC; LI; NO_BATTERY.
    
    If the inverter type is Three phase HV Hybrid, 3 battery types supported: BATT_V; LI; NO_BATTERY.
    """

    def battery_type(self,type):
        url = self.variable.baseurl + '/order/battery/type/update'
        headers = self.variable.headers

        data = {
            "deviceSn": self.serial_number,
            "batteryType":type
        }

        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())

    """""
        Order status
    """""

    def get_contol_res(self,order_id):
        orderId = order_id   # Replace with orderId you sent
        url = self.variable.baseurl + '/order/' + orderId
        headers = self.variable.headers

        response = requests.get(url, headers=headers)

        print(response.status_code)
        print(response.json())

    """"
    options:BATTERY_FIRST;LOAD_FIRST
    """

    def sys_energy_pattern_update(self,pattern):
        url = self.variable.baseurl + '/order/sys/energyPattern/update'
        headers = self.variable.headers
        data = {
            "deviceSn": self.serial_number,
            "energyPattern": pattern
        }

        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())

    """
        Hybrid 3Phase and 1Phase inverter support max_sell_power(powerType= MAX_SELL_POWER) and max_solar_power Control(powerType= MAX_SOLAR_POWER)
        Microinverter and String inverter only support max_sell_power max solar power, the value of max solar power should not exceed rated power
        powerType= MAX_SELL_POWER or MAX_SOLAR_POWER; value=the value you want to set
    """

    def sys_power_update(self,power_type,value):
        url = self.variable.baseurl + '/order/sys/power/update'
        headers = self.variable.headers

        data = {
            "deviceSn": self.serial_number,
            "powerType": power_type,
            "value": value
        }

        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())

    """
    Enable: action=on; Disable: action=off
    """

    def sys_solar_sell_control(self,action):
        url = self.variable.baseurl + '/order/sys/solarSell/control'
        headers = self.variable.headers
        data = {
            "action": action,            # Enable: action=on; Disable: action=off
            "deviceSn": self.serial_number
        }

        response = requests.post(url, headers=headers, json=data)
        print(response.status_code)
        print(response.json())

    """ 
    TimeFormat: 02:00 and timesettings have to be in 5-minute intervals.For example(02:05,02:10)
        If SOC, power, or voltage you set exceeds the range specified on LC screen or manual, it will be set to its boundary value


        Parse Json data:    enableGeneration*	boolean
                            Want to enableGenaration set true otherwise set false

                            enableGridCharge*	boolean
                            Want to enableGridCharge set true otherwise set false

                            power*	integer($int32)
                            soc	integer($int32)
                            time*	string
                            voltage	integer($int32)
                            If enabled batterty voltage mode, this field should be set.
    """

    def sys_tou_update(self,timeUseSettingItems):
        url = self.variable.baseurl + '/order/sys/tou/update'
        headers = self.variable.headers

        # request body
        data = {
            "deviceSn": self.serial_number,
            "timeUseSettingItems":timeUseSettingItems,
            "timeoutSeconds": 30
        }

        # request post
        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())
        return response.json()

    """Turn off TOU: 'action'=off, not necessary to fill in the field 'days'
        Turn on TOU: 'action'=on, If you don't fill in the field 'days', by default, MONDAY to SUNDAY are all active
        Fill in 'days' specifying which day you want to make active. For example days=[MONDAY, THURSDAY] means MONDAY and THURSDAY are active;TUESDAY,WEDNESDAY,FRIDAY,SATURDAY,SUNDAY are inactive
        Notice:
        value in field 'days' should be in uppercase
    """

    def sys_tou_switch(self,action,days=""):
        url = self.variable.baseurl + '/order/sys/tou/switch'
        headers = self.variable.headers

        # request body
        data = {
            "action":action,
            "deviceSn": self.serial_number,

        }
        if(days):
            data["days"]=days

        # request post
        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())
        return response.json()

    """ 
    Set system work mode as SELLING_FIRST,ZERO_EXPORT_TO_LOAD or ZERO_EXPORT_TO_CT 
    """

    def sys_work_mode_update(self,mode):
        url = self.variable.baseurl + '/order/sys/workMode/update'
        headers = self.variable.headers
        data = {
            "deviceSn": self.serial_number,
            "workMode": mode     # options: SELLING_FIRST; ZERO_EXPORT_TO_LOAD; ZERO_EXPORT_TO_CT
        }

        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())

    def system_config(self):
        url = self.variable.baseurl + '/config/system'
        headers = self.variable.headers
        data = {
            "deviceSn": self.serial_number,
        }

        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())

    def battery_config(self):
        url = self.variable.baseurl + '/config/battery'
        headers = self.variable.headers
        data = {
            "deviceSn": self.serial_number,
        }

        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())
    def get_order(self,order_id):
        url = self.variable.baseurl + f'/order/{order_id}'

        headers = self.variable.headers

        response = requests.get(url, headers=headers)

        print(response.status_code)
        print(response.json())

    ## MAIN CHARGING ACTIONS
    def battery_charge(self,power,SOC=100):
        url = self.variable.baseurl + '/strategy/dynamicControl'
        headers = self.variable.headers

        targetSOC = SOC;
        power = power;  #this is just an example,fill in your target power (Reference valu : power = min(maxAcharge current, gridChargeAmpere) * vol)
        # request body
        data = {
            "deviceSn": self.serial_number,
            "gridChargeAction": "on",
            #"gridChargeAmpere": 0,  # BMSCharge current limit;
            "touAction": "on",
            "touDays": ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"],
            # 7days: SUNDAY to SATURDAY
            "workMode": "SELLING_FIRST",  #  ZERO_EXPORT_TO_CT(if CT exists) or ZERO_EXPORT_TO_LOAD
            "timeUseSettingItems": [
                {
                    "enableGeneration": False,
                    "enableGridCharge": True,
                    "soc": targetSOC,  # high value
                    "power":power,
                    "time": "00:00"  # your control time
                },
                {
                    "enableGeneration": False,
                    "enableGridCharge": True,
                    "soc": targetSOC,  # high value
                    "power": power,
                    "time": "04:00"  # your control time
                },
                {
                    "enableGeneration": False,
                    "enableGridCharge": True,
                    "soc": targetSOC,  # high value
                    "power": power,
                    "time": "08:00"  # your control time
                },
                {
                    "enableGeneration": False,
                    "enableGridCharge": True,
                    "soc": targetSOC,  # high value
                    "power": power,
                    "time": "16:00"  # your control time
                },
                {
                    "enableGeneration": False,
                    "enableGridCharge": True,
                    "soc": targetSOC,  # high value
                    "power": power,
                    "time": "20:00"  # your control time
                },
                {
                    "enableGeneration": False,
                    "enableGridCharge": True,
                    "soc": targetSOC,  # high value
                    "power": power,
                    "time": "00:00"  # your control time
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        return response.json()

    def battery_discharge(self,power,SOC=35):
        url = self.variable.baseurl + '/strategy/dynamicControl'
        headers = self.variable.headers

        targetSOC = SOC;
        power = power;  #this is just an example,fill in your target power (Reference valu : power = min(maxAcharge current, gridChargeAmpere) * vol)
        # request body
        data = {
            "deviceSn": self.serial_number,
            "gridChargeAction": "on",
            #"gridChargeAmpere": 0,  # BMSCharge current limit;
            "touAction": "on",
            "touDays": ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"],
            # 7days: SUNDAY to SATURDAY
            "workMode": "SELLING_FIRST",  #  ZERO_EXPORT_TO_CT(if CT exists) or ZERO_EXPORT_TO_LOAD
            "timeUseSettingItems": [
                {
                    "enableGeneration": True,
                    "enableGridCharge": True,
                    "soc": targetSOC,  # high value
                    "power":power,
                    "time": "00:10"  # your control time
                },
                {
                    "enableGeneration": True,
                    "enableGridCharge": True,
                    "soc": targetSOC,  # high value
                    "power": power,
                    "time": "02:10"  # your control time
                },
                {
                    "enableGeneration": True,
                    "enableGridCharge": True,
                    "soc": targetSOC,  # high value
                    "power": power,
                    "time": "04:10"  # your control time
                },
                {
                    "enableGeneration": True,
                    "enableGridCharge": True,
                    "soc": targetSOC,  # high value
                    "power": power,
                    "time": "15:10"  # your control time
                },
                {
                    "enableGeneration": True,
                    "enableGridCharge": True,
                    "soc": targetSOC,  # high value
                    "power": power,
                    "time": "20:10"  # your control time
                },
                {
                    "enableGeneration": True,
                    "enableGridCharge": True,
                    "soc": targetSOC,  # high value
                    "power": power,
                    "time": "23:10"  # your control time
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        return response.json()

    def battery_stop(self):
        url = self.variable.baseurl + '/strategy/dynamicControl'
        headers = self.variable.headers


        data = {
            "deviceSn": self.serial_number,
            "gridChargeAction": "off",
            "touAction": "off",
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    ## GET CURRENT DATA
    def current_device_history(self,startAt,measurePoints="SOC",granularity=1,endAt=""):
        url = self.variable.baseurl + '/device/history'
        headers = self.variable.headers
        data = {
            "deviceSn": self.serial_number,
            "startAt":startAt,
            "endAt":endAt,
            "granularity":granularity,
            "measurePoints":measurePoints
        }

        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())

    def get_raw_current_data(self):
        current_time = datetime.now()
        end_timestamp = int(current_time.timestamp() * 1000)

        one_hour_ago = current_time - timedelta(days=7)
        start_timestamp = int(one_hour_ago.timestamp() * 1000)

        url = self.variable.baseurl + '/device/historyRaw'
        headers = self.variable.headers
        data = {
            "deviceSn": self.serial_number,
            "endTimestamp":end_timestamp,
            "startTimestamp":start_timestamp,
            "measurePoints":["SOC"]
        }
        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())
        return response.json()

    def get_lattest_history(self,device_list=[]):
        try:
            url = self.variable.baseurl + '/device/latest'
            headers = self.variable.headers
            if(not device_list):
                list=[self.serial_number]

            else:
                list=device_list
            data = {
                "deviceList": list
            }
            response = requests.post(url, headers=headers, json=data)
            return response.json()
        except Exception as err:
            logging.error(f"Error occured{err}")


    def get_lattest_errors(self):
        end_timestamp = int(time.time())
        start_timestamp = end_timestamp-1*3600
        try:
            url = self.variable.baseurl + '/device/alertList'
            headers = self.variable.headers

            data = {
                "deviceId": self.serial_number,
                "endTimestamp": end_timestamp,
                "startTimestamp": start_timestamp
            }
            response = requests.post(url, headers=headers, json=data)
            print(response.json())
            return response.json()
        except Exception as err:
            logging.error(f"Error occured{err}")

if(__name__=="__main__"):
    co=Commision("2407264006")
    print(co.battery_stop())
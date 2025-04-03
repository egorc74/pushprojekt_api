from variables import Variables   
import requests 


class Commision:
    def __init__(self,serial_number="",station_id=""):
        self.serial_number=serial_number
        self.variable=Variables()
        self.station_id=station_id



    """Returns history data for devices at different granularities.
granularity=1: the field ‘startAt’ should be in format 'yyyy-MM-dd’. Field ‘measurePoints’ has to be passed. Returns measure-point data for the day specified by ‘startAt’
granularity=2: the field ‘startAt’ and 'endAt’ should be in format 'yyyy-MM-dd’. Returns statistics data between ‘startAt’ and ‘endAt’ (up to 31 days) with intervals of one day
granularity=3: the field ‘startAt’ and 'endAt’ should be in format 'yyyy-MM’. Returns statistics data between ‘startAt’ and ‘endAt’ (up to 12 months) with intervals of one month
granularity=4: the field ‘startAt’ and 'endAt’ should be in format 'yyyy’. Returns yearly statistics data between ‘startAt’ and ‘endAt’
Value for field of ‘measurePoints‘ could be got through endpint ‘/v1.0/device/measurePoints’"""



    
    def device_history(self,startAt,measurePoints="SOC",granularity=1,endAt=0):
        url = self.variable.baseurl + 'device/history'
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
    
    
    def station_history(self,startAt,granularity=1,endAt=0):
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

    
    """
    Enable or disable the chargeMode
    """
    
    
    def batteryModeControl(self,action):
        url = self.variable.baseurl + '/order/battery/modeControl'
        headers = self.variable.headers
        data = {
                "deviceSn": self.serial_number,
                "batteryModeType": "GRID_CHARGE",
                "action": action
        }

        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())



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



    """ TimeFormat: 02:00 and timesettings have to be in 5-minute intervals.For example(02:05,02:10)
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

    
    def sys_tou_update(self,json_settings):
        url = self.variable.baseurl + '/order/sys/tou/update'
        headers = self.variable.headers

        # request body
        data = {
            "deviceSn": self.serial_number,
            "timeUseSettingItems": json_settings,
            "timeoutSeconds": 30
        }

        # request post
        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())
    


    """Turn off TOU: 'action’=off, not necessary to fill in the field ‘days’
        Turn on TOU: 'action’=on, If you don’t fill in the field 'days’, by default, MONDAY to SUNDAY are all active
        Fill in ‘days’ specifying which day you want to make active. For example days=[MONDAY, THURSDAY] means MONDAY and THURSDAY are active;TUESDAY,WEDNESDAY,FRIDAY,SATURDAY,SUNDAY are inactive
        Notice:
        value in field ‘days’ should be in uppercase
    """
    def sys_tou_switch(self,action,days):
        url = self.variable.baseurl + '/order/sys/tou/switch'
        headers = self.variable.headers

        # request body
        data = {
            "action":action,
            "deviceSn": self.serial_number,
            "days": days
        }

        # request post
        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())
    

    """ set system work mode as SELLING_FIRST,ZERO_EXPORT_TO_LOAD or ZERO_EXPORT_TO_CT 
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

        

        

###TEST 
if( __name__=="__main__"):
    serialn="2407264006"
    test=Commision(serialn)
    #SAMO TEST
    test.battery_type("LI")

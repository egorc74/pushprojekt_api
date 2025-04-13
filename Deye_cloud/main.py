from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import requests
from commision import  Controller

app = FastAPI()

# Pydantic models for request validation
class BatteryCommand(BaseModel):
    deviceSn: str
    power: Optional[int] = None
    mode: Optional[str] = None  # options: SELLING_FIRST; ZERO_EXPORT_TO_LOAD; ZERO_EXPORT_TO_CT

class Order(BaseModel):
    order: str
    serialNumber: str

# Battery Controller Endpoints
@app.post("/battery/start-charging")
async def start_charging(command: BatteryCommand):
    """
    Start battery charging with specified parameters
    """
    try:
        # Here you would implement the actual charging logic
        # For now, we'll just return the received command
        controller=Controller(command.deviceSn)
        execution=controller.charge_battery()

        return {
            "status": "charging_started",
            "device": command.deviceSn,
            "power": command.power,
            "execution":execution,
            "mode": command.mode if command.mode else "default"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/battery/start-discharging")
async def start_discharging(command: BatteryCommand):
    """
    Start battery discharging with specified parameters
    """
    try:
        controller=Controller(command.deviceSn)
        execution=controller.discharge_battery(command.power)
        return {
            "status": "discharging_started",
            "device": command.deviceSn,
            "power": command.power,
            "execution":execution,
            "mode": command.mode if command.mode else "default"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/battery/stop")
async def stop_battery(command: BatteryCommand):
    """
    Stop battery charging/discharging
    """
    try:
        controller=Controller(command.deviceSn)
        execution=controller.stop_charge_battery()
        return {
            "status": "stopped",
            "device": command.deviceSn,
            "execution":execution,

            
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Order Processing Endpoint
@app.post("/process-order")
async def process_order(order: Order):
    """
    Process an order with serial number
    """
    try:
        # Process the order here
        return {
            "status": "order_processed",
            "order_id": order.order,
            "serial_number": order.serialNumber
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Test Client
if __name__ == "__main__":
    # Test the start-charging endpoint
    url = 'http://127.0.0.1:8000/battery/stop'
    data = {
        "deviceSn": "2407264006",
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raises an exception for 4XX/5XX responses
        print("Status Code:", response.status_code)
        print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error making request:", e)
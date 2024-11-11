import json
import os

WATER_PUMP_STATUS_FILE = 'water_pump_status.json'
CONFIG_FILE_NAME = 'config.json'


def get_current_water_pump_status() -> list:
    """
    Reads the current water_pump_status.txt file and renders it
    """
    history: list = []
    if os.path.exists(WATER_PUMP_STATUS_FILE):
        with open(WATER_PUMP_STATUS_FILE, "r") as file:
            history = json.load(file)
            history = history[-100:]  # Limit to last 100 items

    return history


def save_current_water_pump_status(history: list) -> None:
    with open(WATER_PUMP_STATUS_FILE, "w") as file:
        json.dump(history, file, default=str, indent=4)


def save_config(config: dict) -> None:
    with open(CONFIG_FILE_NAME, 'w') as f:
        f.write(json.dumps(config))


def read_config() -> dict:
    with open(CONFIG_FILE_NAME, 'r') as f:
        return json.loads(f.read())

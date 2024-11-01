import 

FILE_NAME='water_pump_status.json'
CONFIG_FILE_NAME='config.json'

def get_current_status() -> str:
    """
    Reads the current water_pump_status.txt file and renders it
    """
    with open(FILE_NAME, 'r') as f:
        return f.read().rstrip()
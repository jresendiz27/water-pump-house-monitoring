import os
import logging
from string import Template

WATER_PUMP_WITHOUT_WATER = """
The water pump is not detecting water flow, You should stop the water pump and check.
Extra Information:
"""

WATER_PUMP_IS_ABOUT_TO_BE_TURNED_OFF = """
The water pump was programed to be turned off automatically. Water pump will turn off at {should_turn_off_at}.
"""

WATER_PUMP_HAS_BEEN_OVERRIDDEN = """
The water pump has already been overridden with the following configuration:
> Now: {now} 
> Should Turn Off At: {should_turn_off_at}
> Minutes: {minutes}
"""


class TelegramService(object):
    enabled: bool

    def __init__(self):
        self.enabled = os.getenv('TELEGRAM_ENABLED', False)
        self.telegram_api_key = os.getenv('TELEGRAM_API_KEY')

    def notify_water_pump_without_water_flow(self):
        message_template = Template(WATER_PUMP_WITHOUT_WATER)
        message = message_template.substitute()

        return self.notify_event(message)

    def water_pump_is_about_to_be_turned_off(self, water_pump_data: dict = None):
        message_template = Template(WATER_PUMP_WITHOUT_WATER)
        message = message_template.substitute(water_pump_data)

        return self.notify_event(message)

    def water_pump_has_been_overridden(self, water_pump_data: dict = None):
        message_template = Template(WATER_PUMP_HAS_BEEN_OVERRIDDEN)
        message = message_template.substitute(water_pump_data)

        return self.notify_event(message)

    def notify_event(self, message):  # Here goes the telegram integration
        if self.enabled:
            pass
        else:
            logging.warning("Telegram is disabled, ignoring message...")

from datetime import datetime, timedelta
import logging
from api import utils
from api.telegram_service import TelegramService

WATER_PUMP_MIC_MIN_THRESHOLD = 100
TANK_MIN_MIC_THRESHOLD = 200


class WaterPumpService:
    def __init__(self, notification_service: TelegramService = None):
        self.current_status = None
        self.history = []
        self.notification_service = notification_service
        self.load_data()

    def load_data(self):
        # Load the JSON file data, limiting to the most recent 100 items

        self.history: list = utils.get_current_water_pump_status()
        if self.history:
            # Load the latest entry as the current status
            self.current_status = self.history[-1]
        else:
            # Initialize default status if no history is found
            self.current_status = self.default_status()
            self.history.append(self.current_status)

        logging.info("Data loaded from json file ...")

    def save_data(self):
        # Add the current status to history, limit to last 100 entries, then save
        self.history.append(self.current_status)
        self.history = self.history[-100:]  # Limit to last 100 items

        utils.save_current_water_pump_status(self.history)

        logging.info("Data saved to json file ...")

    def default_status(self):
        # Default values for a new status
        now = datetime.now()
        return {
            "created_at": now,
            "updated_at": now,
            "is_overridden": False,
            "water_pump_microphone_status": True,
            "water_pump_microphone_value": 0,
            "tank_microphone_status": True,
            "tank_microphone_value": 0,
            "water_pump_status": False,
            "last_checked_at": now,
            "current_metric_date": now,
            "previous_metric_date": now,
        }

    def are_sensors_valid(self):
        return self.current_status["water_pump_microphone_status"] and self.current_status["tank_microphone_status"]

    def is_overridden(self):
        should_turn_on_at = self.current_status.get("should_turn_on_at", None)
        should_turn_off_at = self.current_status.get("should_turn_off_at", None)
        return ((should_turn_on_at is not None and should_turn_off_at is not None)
                and
                (should_turn_on_at <= datetime.now() < should_turn_off_at))

    def determine_water_pump_status(self):
        water_pump_status = self.are_sensors_valid() or self.is_overridden()
        if water_pump_status is False:  # Or the sensors are not receiving information, or it's overridden
            self.notification_service.notify_water_pump_without_water_flow()
        return water_pump_status

    def update_metrics(self, water_pump_microphone_value, tank_microphone_value):
        # Update metrics, calculate if pump should be on/off
        now = datetime.now()
        self.current_status["previous_metric_date"] = self.current_status["current_metric_date"]
        self.current_status["current_metric_date"] = now
        self.current_status["water_pump_microphone_value"] = water_pump_microphone_value
        self.current_status["tank_microphone_value"] = tank_microphone_value
        self.current_status["updated_at"] = now
        self.current_status["last_checked_at"] = now

        # Check microphone status based on value (e.g., if value is above 0, assume it's "on")
        self.current_status["water_pump_microphone_status"] = water_pump_microphone_value > WATER_PUMP_MIC_MIN_THRESHOLD
        self.current_status["tank_microphone_status"] = tank_microphone_value > TANK_MIN_MIC_THRESHOLD

        self.current_status["water_pump_status"] = self.determine_water_pump_status()

        self.save_data()  # Save to JSON after updating

    def override_pump(self, status: bool, turn_off_at_minutes: int = None):
        # Manually override the pump status
        logging.info("Overriding water pump information, turn_off_at_minutes: %s", turn_off_at_minutes)
        now = datetime.now()
        future_date = now + timedelta(minutes=turn_off_at_minutes)
        self.current_status["is_overridden"] = True
        self.current_status["water_pump_status"] = status
        self.current_status["updated_at"] = now

        if status and turn_off_at_minutes:
            self.current_status["should_turn_off_at"] = future_date

        self.save_data()
        self.notification_service.water_pump_has_been_overridden({
            'now': now,
            'should_turn_off_at': future_date,
            'minutes': turn_off_at_minutes
        })

    def reset_override(self):
        # Reset the override to allow normal operation
        self.current_status["is_overridden"] = False
        self.save_data()

    def get_status(self):
        # Returns the current status dictionary
        return self.current_status

    def resolve_action(self) -> int:
        """
        This method will return 1  water is flowing as expected keeping the water pump on, 0 otherwise
        """
        return 1 if self.current_status["water_pump_status"] else 0

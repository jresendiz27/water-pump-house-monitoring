import logging
import secrets
from datetime import datetime, timedelta

from api.db_connection import DatabaseManager
from api.telegram_service import TelegramService

WATER_PUMP_MIC_MIN_THRESHOLD = 100
TANK_MIN_MIC_THRESHOLD = 200


class WaterPumpService(DatabaseManager):
    def __init__(self, notification_service: TelegramService = None):
        super().__init__()
        self.current_status = None
        self.current_pump_status = None
        self.history = []
        self.notification_service = notification_service
        self.load_telemetry_data()
        self.load_pump_status()

    def load_telemetry_data(self):
        latest_metric = """
        SELECT * FROM pump_telemetry p order by p.created_at DESC LIMIT 1
        """
        result = self.fetch_one(latest_metric)
        self.current_status = dict(result) if result is not None else self.default_telemetry_data()

        logging.info("Data loaded from json file ...")

    def save_telemetry_data(self):
        now = datetime.now()
        unique_id = secrets.token_hex(8)
        query = '''
                INSERT INTO pump_telemetry 
                    (
                    id, 
                    water_pump_microphone_value, 
                    water_tank_microphone_value, 
                    created_at,
                    water_pump_status, 
                    water_tank_status
                    )
                VALUES (?, ?, ?, ?, ?, ?)
                '''

        self.execute_query(query, (
            unique_id,
            self.current_status['water_pump_microphone_value'],
            self.current_status['water_tank_microphone_value'],
            now,
            self.current_status["water_pump_status"],
            self.current_status["water_tank_status"]))
        # utils.save_current_water_pump_status(self.history)

        logging.info("Data saved to json file ...")

    def save_pump_status(self, water_pump_enabled: bool = None):
        if self.current_pump_status.get('enabled', False) != water_pump_enabled:
            now = datetime.now()
            unique_id = secrets.token_hex(8)
            insert_query = """
            
            INSERT INTO pump_status(unique_id, enabled, created_at) values (?,?,?)
            """
            self.execute_query(insert_query, (unique_id, water_pump_enabled, now))
            self.load_pump_status()

    def load_pump_status(self):
        latest_pump_status_query = """
        SELECT * FROM pump_status p order by p.created_at DESC LIMIT 1
        """
        result = self.fetch_one(latest_pump_status_query)
        self.current_pump_status = dict(result) if result is not None else {}

    def default_telemetry_data(self):
        # Default values for a new status
        now = datetime.now()
        return {
            "created_at": now,
            "water_pump_status": False,
            "water_pump_microphone_value": 0,
            "water_tank_status": False,
            "water_tank_microphone_value": 0
        }

    def are_sensors_valid(self):
        return self.current_status["water_pump_status"] and self.current_status["water_tank_status"]

    def is_overridden(self):
        should_turn_on_at = self.current_pump_status.get("turn_on_at", None)
        should_turn_off_at = self.current_pump_status.get("turn_off_at", None)
        is_overridden = self.current_pump_status.get("is_overridden", False)
        return (is_overridden
                and
                (should_turn_on_at is not None and should_turn_off_at is not None)
                and
                (should_turn_on_at <= datetime.now() < should_turn_off_at))

    def determine_water_pump_status(self):
        water_pump_status = self.are_sensors_valid() or self.is_overridden()
        if water_pump_status is False:  # Or the sensors are not receiving information, or it's overridden
            self.notification_service.notify_water_pump_without_water_flow()
        return water_pump_status

    def save_telemetry(self, water_pump_microphone_value, tank_microphone_value):
        self.current_status["water_pump_microphone_value"] = water_pump_microphone_value
        self.current_status["water_tank_microphone_value"] = tank_microphone_value

        # Check microphone status based on value (e.g., if value is above 0, assume it's "on")
        self.current_status["water_pump_status"] = water_pump_microphone_value > WATER_PUMP_MIC_MIN_THRESHOLD
        self.current_status["water_tank_status"] = tank_microphone_value > TANK_MIN_MIC_THRESHOLD

        self.current_status["water_pump_status"] = self.determine_water_pump_status()

        self.save_telemetry_data()
        self.save_pump_status(bool(self.current_status.get("water_pump_status", False)))

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

        self.save_telemetry_data()
        self.notification_service.water_pump_has_been_overridden({
            'now': now,
            'should_turn_off_at': future_date,
            'minutes': turn_off_at_minutes
        })

    def reset_override(self):
        pass

    def get_status(self):
        # Returns the current status dictionary
        return self.current_status

    def resolve_action(self) -> int:
        """
        This method will return 1  water is flowing as expected keeping the water pump on, 0 otherwise
        """
        return 1 if self.current_pump_status.get("enabled", 0) else 0

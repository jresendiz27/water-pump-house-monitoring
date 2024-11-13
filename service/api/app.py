import os
import logging
from flask import Flask, request, jsonify

from api.telegram_service import TelegramService
from water_pump_service import WaterPumpService

app = Flask(__name__)

notification_service = TelegramService()


@app.before_request
def before_request():
    if os.environ.get('AUTH_ENABLED') == "true":
        if "Authorization" not in request.headers:
            return "Forbidden", 403
        auth_header = request.headers["Authorization"]

        if auth_header != os.environ.get('VALID_AUTH_HEADER'):
            return "Forbidden", 403


@app.route("/ping", methods=['GET'])
def health():
    return "pong"


@app.route("/water-pump/status", methods=['GET'])
def water_pump_status():
    return jsonify(WaterPumpService().current_status), 200


@app.route("/water-pump/override", methods=['POST'])
def water_pump_override():
    water_pump_service = WaterPumpService(notification_service)

    overridden_action: bool = bool(request.form.get("overridden_action", False))
    turn_off_at_minutes: int = int(request.form.get("turn_on_at_minutes", 5))
    water_pump_service.override_pump(overridden_action, turn_off_at_minutes=turn_off_at_minutes)
    return "true"


@app.route("/water-pump/action", methods=['POST'])
def water_pump_action():
    """
    This method will isolate the logic behind the water-pump, receiving the desired metrics and returning the action
    if the water-pump must be turned on/off based on what's collected or overridden in the configuration
    """
    water_microphone: int = int(request.form.get("water_microphone_value"))
    tank_microphone: int = int(request.form.get("tank_microphone_value"))

    logging.info("Getting information from water-pump, water_microphone: %s, tank_microphone: %s",
                 water_microphone, tank_microphone)

    water_pump_service = WaterPumpService(notification_service)

    water_pump_service.save_telemetry(water_microphone, tank_microphone)

    resolved_action = water_pump_service.resolve_action()

    logging.info("Resolved water pump action: %s" % resolved_action)
    if request.args.get("format") == "json":
        return jsonify({"action": f"{resolved_action}"}), 200
    return f"{resolved_action}", 200


if __name__ == '__main__':
    app.run(debug=True)

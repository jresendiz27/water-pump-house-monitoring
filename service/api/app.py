from flask import Flask
import utils

app = Flask(__name__)

@app.route("/ping", methods=['GET'])
def health():
    return "pong"

@app.route("/water-pump/status", methods=['GET'])
def water_pump_status():
    return utils.get_current_status()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
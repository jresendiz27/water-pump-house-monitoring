# Water Pump Service

## Files Definitions

To make the service as simple as possible, we'll be using just two files that will be used as database and configuration file, both as json format.

### Water Pump Status file

The water pump status file, contains the following information:

* created_at : datetime, contains the information where the information was created (utc)
* updated_at : datetime, contains the information of when the json file was updated (utc)
* is_overridden : boolean, returns true if the water pump information was overridden using a direct post (this must be changed manually)
* water_pump_microphone_status: boolean, returns true if the water pump microphone is receiving information as expected
* water_pump_microphone_value: int, the received value from the arduino uno
* tank_microphone_status: boolean, returns true if the tank microphone is receiving information as expected
* tank_microphone_value: int, the received value from the arduino uno
* water_pump_status: boolean, returns true if the switch is on, should return false if it's overridden or if the tank_microphone_status is false (there's no water flow)
* last_checked_at: datetime, contains the information of when was the last time the arduino sent telemetry from the water pump/tank
* should_turn_on_at: datetime, contains the information (in the future), of when should the water_pump should be active
* should_turn_off_at: datetime, contains the information (in the future), of when should the water_pump be turned off, it's always higher than should_turn_on_at and is_overridden is true
* current_metric_date: datetime, the most recent metric date (default to datetime.datetime.now() in the constructor)
* previous_metric_date: datetime, this will be assigned with the value of `current_metric_date` as soon as the new request arrived


This information will be loaded in the `WaterPumpService` class file in Python, and should read/save the information in a json file, containing max 100 items, to keep track of historical information, also we should always load the last one (which will be the most recent one)
so we can understand if the water pump must be kept on or should be turned off (based on the metrics or if it was programmed)

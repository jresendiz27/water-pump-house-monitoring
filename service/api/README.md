# Water Pump Service

## Files Definitions

To make the service as simple as possible, we'll be using just two files that will be used as database and configuration file, both as json format.

### Water Pump Status file

The water pump status file, contains the following information:

* created_at : datetime, contains the information where the information was created (utc)
* updated_at : datetime, contains the information of when the json file was updated (utc)
* is_overriden : boolean, returns true if the water pump information was overriden using a direct post (this must be changed manually)
* water_pump_microphone_status: boolean, returns true if the water pump microphone is receiving information as expected
* tank_microphone_status: boolean, returns true if the tank microphone is receiving information as expected
* water_pump_status: boolean, returns true if the switch is on, should return false if it's overriden or if the tank_microphone_status is false (there's no water flow)
* last_checked_at: datetime, contains the information of when was the last time the arduino sent telemetry from the water pump/tank
* should_turn_on_at: datetime, contains the information (in the future), of when should the water_pump should be active
* should_turn_off_at: datetime, contains the information (in the future), of when should the water_pump be turned off, its always higher than should_turn_on_at and is_overriden is true
* 

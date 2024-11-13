CREATE TABLE IF NOT EXISTS pump_status (
    unique_id TEXT PRIMARY KEY,
    enabled BOOLEAN DEFAULT 1,
    created_at DATE,
    is_overridden BOOLEAN DEFAULT 0,
    turn_on_at DATE,
    turn_off_at DATE
);


CREATE TABLE IF NOT EXISTS pump_telemetry (
    id TEXT PRIMARY KEY,
    water_pump_microphone_value INTEGER DEFAULT 0,
    water_tank_microphone_value INTEGER DEFAULT 0,
    created_at DATE,
    water_pump_status BOOLEAN DEFAULT 0,
    water_tank_status BOOLEAN DEFAULT 0
);


CREATE TABLE IF NOT EXISTS pump_weekly_telemetry (
    water_pump_p50 FLOAT,
    water_pump_p75 FLOAT,
    water_pump_p90 FLOAT,
    water_tank_p50 FLOAT,
    water_tank_p75 FLOAT,
    water_tank_p90 FLOAT
);

CREATE TABLE IF NOT EXISTS configuration (
    telemetry_enabled BOOLEAN DEFAULT 0,
    water_pump_min_threshold FLOAT,
    water_tank_min_threshold FLOAT,
    notifications_enabled BOOLEAN DEFAULT 0
);


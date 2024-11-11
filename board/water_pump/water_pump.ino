#include <WiFi.h>
#include <Servo.h>
#include <ArduinoHttpClient.h>
#include "secrets.h"  // Include the file containing the WiFi credentials

// Constants
int METRICS_DELAY_TIME = 60000; // 60 seconds
// Pin location

int PIN_SERVO_LOCATION = 8;
int PIN_TANK_LOCATION = 0;
int PIN_PUMP_LOCATION = 1;

//Clients
WiFiClient wifi;
HttpClient http = HttpClient(wifi, "jsonplaceholder.typicode.com", 80);

//

void connectWifi() {
  // Start the WiFi connection
  Serial.println("Connecting to WiFi...");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  // Wait until connected
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // Print the IP address when connected
  Serial.println("\nConnected to WiFi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void makeGetRequest() {

  http.get("/posts/1");
  int code = http.responseStatusCode();
  if (code >= 200 && code < 400) {
    Serial.println("Code: " + code);
    String payload = http.responseBody();
    Serial.println("Response payload:");
    Serial.println(payload);
  } else {
    Serial.println("Error!!!!!");
  }
}

void setup() {
  Serial.begin(115200);  // Start the serial communication
  delay(1000);

  connectWifi();
}

void sendMetrics(){


}

void changeWaterPumpState(int status) {


}

void loop() {
  // Your code here (e.g., HTTP requests, sensor data, etc.)
  Serial.println("Stuff");
  makeGetRequest();
  delay(5000);
}

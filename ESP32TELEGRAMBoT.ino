#include <WiFi.h>
#include <WiFiUdp.h>
#include <coap-simple.h>
#include <Adafruit_AHTX0.h>

// Wi-Fi credentials
const char *ssid = "CarteaJunglei";
const char *password = "daniel321";

// CoAP UDP and handler objects
WiFiUDP udp;
Coap coap(udp);

// AHT sensor initialization
Adafruit_AHTX0 aht;

// CoAP server callback function for handling data requests
void callback_light(CoapPacket &packet, IPAddress ip, int port);

// CoAP client response callback function
void callback_response(CoapPacket &packet, IPAddress ip, int port);

// Function to get formatted temperature and humidity data as "temp humidity"
String getFormattedSensorData() {
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);

  // Create a char array to hold the formatted data
  char dataString[12];
  
  // Format the temperature and humidity values
  dtostrf(temp.temperature, 5, 2, dataString);
  dataString[5] = ' ';
  dtostrf(humidity.relative_humidity, 5, 2, dataString + 6);

  return String(dataString); // Return as a String for easy handling
}

void setup() {
  Serial.begin(9600);                   // Debugging
  Serial2.begin(9600, SERIAL_8N1, 15, 4); // UART TX: GPIO 4, RX: GPIO 15 for Arduino communication
  Serial.println("Setting up AHT10/AHT20 and WiFi...");

  // Initialize the AHT sensor
  if (!aht.begin()) {
    Serial.println("Could not find AHT? Check wiring");
    while (1) delay(10);
  }
  Serial.println("AHT10/AHT20 sensor initialized");

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected. IP address: ");
  Serial.println(WiFi.localIP());

  // Set up CoAP server and response callbacks
  coap.server(callback_sensor, "sensor");
  coap.response(callback_response);
  coap.start();
}

// CoAP callback function that handles the request and sends temperature and humidity data
void callback_sensor(CoapPacket &packet, IPAddress ip, int port) {
  Serial.println("[Sensor] READINGS request received");

  // Get sensor data
  String dataString = getFormattedSensorData();

  // Send response back to CoAP client
  coap.sendResponse(ip, port, packet.messageid, dataString.c_str());
  Serial.print("CoAP Response Sent: ");
  Serial.println(dataString);
}

// CoAP client response callback function
void callback_response(CoapPacket &packet, IPAddress ip, int port) {
  Serial.println("[Coap Response received]");
  char p[packet.payloadlen + 1];
  memcpy(p, packet.payload, packet.payloadlen);
  p[packet.payloadlen] = NULL;
  Serial.println(p);
}

void loop() {
  // Regularly send sensor data via UART (Serial2)
  String dataString = getFormattedSensorData();

  Serial2.println(dataString);  // Send data via Serial2
  Serial.print("Data sent to Arduino: ");
  Serial.println(dataString);

  delay(2000);  // Wait before sending the next set of data

  coap.loop();  // Handle CoAP requests in the background
}

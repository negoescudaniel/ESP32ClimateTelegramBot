// Arduino Uno Code
// include the library code:
#include <LiquidCrystal.h>

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  Serial.begin(9600); // Initialize serial communication for debugging
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.print("Daniel's Project");
}

void loop() {
  if (Serial.available()) {          // Check if data is available to read
    String message = Serial.readStringUntil('\n'); // Read until newline
    Serial.println("Received: " + message); // Print the received message

    // Split the message into temperature and humidity
    int spaceIndex = message.indexOf(' ');  // Find the space separator
    String tempString = message.substring(0, spaceIndex);  // Extract temperature as a substring
    String humidityString = message.substring(spaceIndex + 1);  // Extract humidity as a substring

    // Convert the substrings to float values
    float temp = tempString.toFloat();
    float humidity = humidityString.toFloat();
    lcd.clear();
    // Print the Temperature on the LCD
    lcd.setCursor(0, 0);
    lcd.print("Temp: ");
    lcd.print(temp);
    lcd.print(" C");

    // Print the Humidity on the LCD
    lcd.setCursor(0, 1);
    lcd.print("Hum(RH): ");
    lcd.print(humidity);
    lcd.print(" %");
  }
}


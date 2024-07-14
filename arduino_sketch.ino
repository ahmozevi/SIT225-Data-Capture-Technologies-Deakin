int ledPin = 13;  // LED connected to digital pin 13

void setup() {
  Serial.begin(9600);  // Start serial communication at 9600 baud rate
  pinMode(ledPin, OUTPUT);  // Set the LED pin as output
}

void loop() {
  if (Serial.available() > 0) {
    // Read the number sent from Python script
    int number = Serial.parseInt();
    
    // Blink the LED 'number' of times
    for (int i = 0; i < number; i++) {
      digitalWrite(ledPin, HIGH);
      delay(1000);  // Wait for 1 second
      digitalWrite(ledPin, LOW);
      delay(1000);  // Wait for 1 second
    }
    
    // Send a random number back to Python script
    int responseNumber = random(1, 5);
    Serial.println(responseNumber);
  }
}

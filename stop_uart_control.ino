const int motorPin1 = 9;  // Motor direction pin
const int motorPin2 = 10; // Motor direction pin
const int enablePin = 5;  // Motor speed (PWM)

char receivedChar;

void setup() {
  Serial.begin(9600);
  
  // Setup motor pins
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(enablePin, OUTPUT);

  // Start with motors running (robot moving)
  moveForward();
}

void loop() {
  // Check if data is available
  if (Serial.available() > 0) {
    receivedChar = Serial.read();

    if (receivedChar == '1') {
      stopMotors();  // Stop if '1' received
    } else if (receivedChar == '0') {
      moveForward(); // Keep moving if '0' received
    }
  }
}

// Function to move forward
void moveForward() {
  digitalWrite(motorPin1, HIGH);
  digitalWrite(motorPin2, LOW);
  analogWrite(enablePin, 200); // Speed (0–255)
}

// Function to stop motors
void stopMotors() {
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  analogWrite(enablePin, 0);
}

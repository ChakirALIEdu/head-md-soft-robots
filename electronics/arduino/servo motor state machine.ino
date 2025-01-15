#include <Servo.h>

// Define the servo pin
const int servoPin = 9;

// Initialize the servo
Servo myServo;

// Define states
String currentState = "SILENT";

// Movement parameters
int neutralAngle = 90;  // Neutral position
int narrowMin = 80;     // Minimum angle for narrow movements
int narrowMax = 100;    // Maximum angle for narrow movements
int wideMin = 45;       // Minimum angle for wide movements
int wideMax = 135;      // Maximum angle for wide movements
int dynamicRange = 10;  // Initial dynamic range for movements

// Timing and movement variables
unsigned long lastMoveTime = 0;   // Track the last movement time
float currentAngle = neutralAngle; // Current servo position
float stepSize = 0.5;             // Step size for smooth movement
bool increasing = true;           // Track direction of movement

void setup() {
  Serial.begin(9600);        // Initialize serial communication
  myServo.attach(servoPin);  // Attach the servo to the pin
  myServo.write(neutralAngle);  // Initialize servo to neutral position
  Serial.println("Arduino ready to receive state data");
}

void loop() {
  // Check if data is available from the Raspberry Pi
  if (Serial.available() > 0) {
    String receivedState = Serial.readStringUntil('\n'); // Read the incoming state
    receivedState.trim(); // Remove any extra whitespace

    // Update the current state if it has changed
    if (receivedState != currentState) {
      currentState = receivedState;
      Serial.print("State changed to: ");
      Serial.println(currentState);
      resetMovementParams(); // Reset movement parameters for the new state
    }
  }

  // Control servo based on the current state
  if (currentState == "OBSERVE") {
    handleObserveMovement();
  } else if (currentState == "CALM") {
    handleCalmMovement();
  } else if (currentState == "BREATHING") {
    handleBreathingMovement();
  } else if (currentState == "ERRATIC") {
    handleErraticMovement();
  } else if (currentState == "SILENT") {
    handleSilentState();
  }
}

// Reset movement parameters for new state
void resetMovementParams() {
  lastMoveTime = 0;
  increasing = true;
  currentAngle = neutralAngle;
  stepSize = 0.5; // Default step size for smooth movements
  dynamicRange = random(5, 15); // Randomize range for more natural movement
}

// Handle OBSERVE state movement
void handleObserveMovement() {
  moveServoContinuous(narrowMin, narrowMax, 10); // Slow, continuous narrow movement
}

// Handle CALM state movement
void handleCalmMovement() {
  moveServoContinuous(wideMin, wideMax + dynamicRange, 30); // Wide, continuous smooth movement with dynamic range
}

// Handle BREATHING state movement
void handleBreathingMovement() {
  moveServoContinuous(wideMin, wideMax + dynamicRange, 50); // Very slow and fluid wide movement with pauses
}

// Handle ERRATIC state movement
void handleErraticMovement() {
  moveServoSharp(wideMin, wideMax, random(50, 150)); // Quick, sharp movements with random delays
}

// Handle SILENT state
void handleSilentState() {
  myServo.write(neutralAngle);  // Ensure servo stays in neutral
}

// Move the servo continuously between a range with variable speed
void moveServoContinuous(int minAngle, int maxAngle, unsigned long speed) {
  unsigned long currentTime = millis();
  if (currentTime - lastMoveTime >= speed) {
    if (increasing) {
      currentAngle += stepSize;
      if (currentAngle >= maxAngle) increasing = false;
    } else {
      currentAngle -= stepSize;
      if (currentAngle <= minAngle) increasing = true;
    }
    myServo.write((int)currentAngle); // Cast to integer for servo command
    lastMoveTime = currentTime;
  }
}

// Sharply move the servo between a range with random delays
void moveServoSharp(int minAngle, int maxAngle, unsigned long speed) {
  unsigned long currentTime = millis();
  if (currentTime - lastMoveTime >= speed) {
    if (increasing) {
      currentAngle = maxAngle;
      increasing = false;
    } else {
      currentAngle = minAngle;
      increasing = true;
    }
    myServo.write((int)currentAngle); // Cast to integer for servo command
    lastMoveTime = currentTime;
  }
}

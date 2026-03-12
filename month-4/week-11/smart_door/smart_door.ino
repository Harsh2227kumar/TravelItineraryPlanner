/*
 * Week 11: Smart Door Automation
 * 
 * System using IR proximity sensor to detect person approach,
 * trigger servo motor for door open/close, and log events via Serial.
 * 
 * Components:
 *   - IR Proximity Sensor (connected to pin 2)
 *   - Servo Motor (connected to pin 9)
 *   - LED indicator (connected to pin 13)
 * 
 * Wiring:
 *   IR Sensor VCC → 5V
 *   IR Sensor GND → GND
 *   IR Sensor OUT → Digital Pin 2
 *   Servo Signal  → Digital Pin 9
 *   Servo VCC     → 5V
 *   Servo GND     → GND
 *   LED Anode     → Pin 13 (via 220Ω resistor)
 *   LED Cathode   → GND
 */

#include <Servo.h>

// ── Pin Definitions ──────────────────────────────────────────
#define IR_SENSOR_PIN   2
#define SERVO_PIN       9
#define LED_PIN         13

// ── Configuration ────────────────────────────────────────────
#define DOOR_OPEN_ANGLE   90    // Servo angle for open door
#define DOOR_CLOSED_ANGLE 0     // Servo angle for closed door
#define DOOR_OPEN_TIME    5000  // Keep door open for 5 seconds (ms)
#define DEBOUNCE_DELAY    500   // Debounce delay (ms)

Servo doorServo;
bool doorOpen = false;
unsigned long lastTriggerTime = 0;
int eventCount = 0;

void setup() {
    Serial.begin(9600);
    Serial.println("=== Smart Door Automation System ===");
    Serial.println("Initializing...");

    pinMode(IR_SENSOR_PIN, INPUT);
    pinMode(LED_PIN, OUTPUT);

    doorServo.attach(SERVO_PIN);
    doorServo.write(DOOR_CLOSED_ANGLE);
    digitalWrite(LED_PIN, LOW);

    Serial.println("System ready. Monitoring for approach...");
    Serial.println("------------------------------------");
}

void loop() {
    int sensorValue = digitalRead(IR_SENSOR_PIN);
    unsigned long currentTime = millis();

    // IR sensor: LOW = object detected (active-low for most IR modules)
    if (sensorValue == LOW && !doorOpen && (currentTime - lastTriggerTime > DEBOUNCE_DELAY)) {
        // Person detected — open door
        eventCount++;
        doorOpen = true;
        lastTriggerTime = currentTime;

        Serial.print("[EVENT #");
        Serial.print(eventCount);
        Serial.print("] Person detected at ");
        Serial.print(currentTime / 1000);
        Serial.println("s — Opening door.");

        doorServo.write(DOOR_OPEN_ANGLE);
        digitalWrite(LED_PIN, HIGH);

        // Keep door open for configured time
        delay(DOOR_OPEN_TIME);

        // Close door
        doorServo.write(DOOR_CLOSED_ANGLE);
        digitalWrite(LED_PIN, LOW);
        doorOpen = false;

        Serial.print("[EVENT #");
        Serial.print(eventCount);
        Serial.println("] Door closed.");
        Serial.println("------------------------------------");
    }

    delay(100); // Small polling delay
}

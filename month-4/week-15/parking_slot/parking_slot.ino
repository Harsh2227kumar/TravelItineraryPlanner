/*
 * Week 15: Parking Slot Occupancy
 * 
 * PIR proximity sensors monitor vehicle entry/exit at each parking slot.
 * Updates a slot status array and transmits data via Bluetooth (SoftwareSerial).
 * 
 * Components:
 *   - 3x PIR Motion Sensors (pins 2, 3, 4)
 *   - HC-05 Bluetooth Module (TX→pin10, RX→pin11)
 *   - 3x LEDs — Red=occupied, Green=free (pins 5,6,7 and 8,9,12)
 *   - LCD 16x2 (I2C) for local display
 * 
 * Wiring:
 *   PIR Sensor 1 → Pin 2
 *   PIR Sensor 2 → Pin 3
 *   PIR Sensor 3 → Pin 4
 *   Red LED 1    → Pin 5 (via 220Ω)
 *   Red LED 2    → Pin 6 (via 220Ω)
 *   Red LED 3    → Pin 7 (via 220Ω)
 *   Green LED 1  → Pin 8 (via 220Ω)
 *   Green LED 2  → Pin 9 (via 220Ω)
 *   Green LED 3  → Pin 12 (via 220Ω)
 *   HC-05 TX     → Pin 10 (SoftwareSerial RX)
 *   HC-05 RX     → Pin 11 (SoftwareSerial TX, via voltage divider)
 */

#include <SoftwareSerial.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ── Pin Definitions ──────────────────────────────────────────
#define NUM_SLOTS 3

const int pirPins[NUM_SLOTS]      = {2, 3, 4};
const int redLedPins[NUM_SLOTS]   = {5, 6, 7};
const int greenLedPins[NUM_SLOTS] = {8, 9, 12};

#define BT_RX_PIN  10
#define BT_TX_PIN  11

// ── Configuration ────────────────────────────────────────────
#define OCCUPY_TIMEOUT 10000  // Time before slot is considered vacant (ms)
#define UPDATE_INTERVAL 2000  // Bluetooth transmit interval (ms)

SoftwareSerial bluetooth(BT_RX_PIN, BT_TX_PIN);
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Slot state tracking
bool slotOccupied[NUM_SLOTS] = {false, false, false};
unsigned long lastMotion[NUM_SLOTS] = {0, 0, 0};
unsigned long lastTransmit = 0;

void setup() {
    Serial.begin(9600);
    bluetooth.begin(9600);

    Serial.println("=== Parking Slot Occupancy System ===");
    Serial.println("Monitoring 3 parking slots...");

    for (int i = 0; i < NUM_SLOTS; i++) {
        pinMode(pirPins[i], INPUT);
        pinMode(redLedPins[i], OUTPUT);
        pinMode(greenLedPins[i], OUTPUT);

        // Initially all slots free (green)
        digitalWrite(greenLedPins[i], HIGH);
        digitalWrite(redLedPins[i], LOW);
    }

    lcd.init();
    lcd.backlight();
    updateDisplay();

    bluetooth.println("PARKING_SYSTEM_READY");
}

void loop() {
    unsigned long now = millis();

    // Read each PIR sensor
    for (int i = 0; i < NUM_SLOTS; i++) {
        if (digitalRead(pirPins[i]) == HIGH) {
            // Motion detected — slot occupied
            lastMotion[i] = now;

            if (!slotOccupied[i]) {
                slotOccupied[i] = true;
                Serial.print("Slot ");
                Serial.print(i + 1);
                Serial.println(": OCCUPIED");

                // Red LED on, Green off
                digitalWrite(redLedPins[i], HIGH);
                digitalWrite(greenLedPins[i], LOW);
            }
        }

        // Check for vacancy timeout
        if (slotOccupied[i] && (now - lastMotion[i] > OCCUPY_TIMEOUT)) {
            slotOccupied[i] = false;
            Serial.print("Slot ");
            Serial.print(i + 1);
            Serial.println(": VACANT");

            // Green LED on, Red off
            digitalWrite(greenLedPins[i], HIGH);
            digitalWrite(redLedPins[i], LOW);
        }
    }

    // Update LCD
    updateDisplay();

    // Transmit via Bluetooth at regular intervals
    if (now - lastTransmit > UPDATE_INTERVAL) {
        lastTransmit = now;
        transmitStatus();
    }

    delay(100);
}

void updateDisplay() {
    int freeCount = 0;
    for (int i = 0; i < NUM_SLOTS; i++) {
        if (!slotOccupied[i]) freeCount++;
    }

    lcd.setCursor(0, 0);
    lcd.print("Parking: ");
    lcd.print(freeCount);
    lcd.print("/");
    lcd.print(NUM_SLOTS);
    lcd.print(" free ");

    lcd.setCursor(0, 1);
    for (int i = 0; i < NUM_SLOTS; i++) {
        lcd.print("S");
        lcd.print(i + 1);
        lcd.print(":");
        lcd.print(slotOccupied[i] ? "X " : "O ");
    }
}

void transmitStatus() {
    // Build JSON-like status string
    String status = "{\"slots\":[";
    for (int i = 0; i < NUM_SLOTS; i++) {
        if (i > 0) status += ",";
        status += "{\"id\":";
        status += (i + 1);
        status += ",\"status\":\"";
        status += (slotOccupied[i] ? "occupied" : "free");
        status += "\"}";
    }
    status += "]}";

    bluetooth.println(status);
    Serial.print("[BT TX] ");
    Serial.println(status);
}

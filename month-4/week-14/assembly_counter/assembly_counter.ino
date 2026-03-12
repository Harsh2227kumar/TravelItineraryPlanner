/*
 * Week 14: Assembly Line Object Counter
 * 
 * Inductive proximity sensor detects metal parts on a conveyor belt,
 * increments a counter, and sends data to LCD + Serial.
 * 
 * Components:
 *   - Inductive Proximity Sensor NPN (pin 2)
 *   - 16x2 LCD (I2C address 0x27)
 *   - Green LED — part detected flash (pin 12)
 *   - Red LED — count milestone indicator (pin 11)
 * 
 * Wiring:
 *   Inductive Sensor → Pin 2 (with 10kΩ pull-up to 5V)
 *   LCD SDA          → A4
 *   LCD SCL          → A5
 *   Green LED        → Pin 12 (via 220Ω)
 *   Red LED          → Pin 11 (via 220Ω)
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ── Pin Definitions ──────────────────────────────────────────
#define SENSOR_PIN     2
#define GREEN_LED_PIN  12
#define RED_LED_PIN    11

// ── Configuration ────────────────────────────────────────────
#define DEBOUNCE_MS    300   // Debounce delay between counts
#define MILESTONE      10    // Flash red LED every N parts
#define BATCH_SIZE     50    // Log batch completion

LiquidCrystal_I2C lcd(0x27, 16, 2);

volatile unsigned long partCount = 0;
unsigned long lastDetection = 0;
unsigned long lastDisplayUpdate = 0;
unsigned long startTime = 0;

void setup() {
    Serial.begin(9600);
    Serial.println("=== Assembly Line Object Counter ===");
    Serial.println("Counting metal parts on conveyor...");
    Serial.println("Time(s) | Count | Rate(parts/min)");
    Serial.println("--------|-------|----------------");

    pinMode(SENSOR_PIN, INPUT);
    pinMode(GREEN_LED_PIN, OUTPUT);
    pinMode(RED_LED_PIN, OUTPUT);

    lcd.init();
    lcd.backlight();
    lcd.setCursor(0, 0);
    lcd.print("Assembly Counter");
    lcd.setCursor(0, 1);
    lcd.print("Parts: 0");

    startTime = millis();
}

void loop() {
    unsigned long now = millis();

    // Read inductive sensor (HIGH when metal detected for NPN type)
    if (digitalRead(SENSOR_PIN) == HIGH && (now - lastDetection > DEBOUNCE_MS)) {
        lastDetection = now;
        partCount++;

        // Flash green LED
        digitalWrite(GREEN_LED_PIN, HIGH);
        delay(50);
        digitalWrite(GREEN_LED_PIN, LOW);

        // Milestone indicator
        if (partCount % MILESTONE == 0) {
            digitalWrite(RED_LED_PIN, HIGH);
            delay(200);
            digitalWrite(RED_LED_PIN, LOW);
        }

        // Serial logging
        float elapsedMin = (now - startTime) / 60000.0;
        float rate = (elapsedMin > 0) ? partCount / elapsedMin : 0;

        Serial.print((now - startTime) / 1000);
        Serial.print("s\t| ");
        Serial.print(partCount);
        Serial.print("\t| ");
        Serial.print(rate, 1);
        Serial.println(" parts/min");

        // Batch completion
        if (partCount % BATCH_SIZE == 0) {
            Serial.println(">>> BATCH COMPLETE <<<");
            Serial.print("Total: ");
            Serial.print(partCount);
            Serial.println(" parts");
        }
    }

    // Update LCD every 500ms
    if (now - lastDisplayUpdate > 500) {
        lastDisplayUpdate = now;
        updateLCD(now);
    }

    delay(10);
}

void updateLCD(unsigned long now) {
    float elapsedMin = (now - startTime) / 60000.0;
    float rate = (elapsedMin > 0.01) ? partCount / elapsedMin : 0;

    lcd.setCursor(0, 0);
    lcd.print("Parts: ");
    lcd.print(partCount);
    lcd.print("       ");  // Clear trailing chars

    lcd.setCursor(0, 1);
    lcd.print("Rate: ");
    lcd.print(rate, 1);
    lcd.print(" p/m   ");
}

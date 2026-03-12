/*
 * Week 13: Vending Machine Dispenser
 * 
 * Capacitive proximity sensor detects hand near the pickup slot,
 * relay activates dispenser motor, and inventory is tracked in EEPROM.
 * 
 * Components:
 *   - Capacitive Proximity Sensor (pin 2)
 *   - Relay Module (pin 7) — controls dispenser motor
 *   - 16x2 LCD (I2C address 0x27)
 *   - Push button for item select (pin 3)
 *   - EEPROM (built-in) for inventory count
 * 
 * Wiring:
 *   Cap Sensor OUT → Pin 2
 *   Relay IN       → Pin 7
 *   Button         → Pin 3 (with pull-up)
 *   LCD SDA        → A4
 *   LCD SCL        → A5
 */

#include <EEPROM.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ── Pin Definitions ──────────────────────────────────────────
#define CAP_SENSOR_PIN  2
#define RELAY_PIN       7
#define BUTTON_PIN      3

// ── EEPROM Addresses ─────────────────────────────────────────
#define EEPROM_SLOT_A   0   // Inventory count for Slot A
#define EEPROM_SLOT_B   1   // Inventory count for Slot B
#define EEPROM_SLOT_C   2   // Inventory count for Slot C

// ── Configuration ────────────────────────────────────────────
#define MAX_INVENTORY   10  // Max items per slot
#define DISPENSE_TIME   2000 // Relay on time (ms)
#define DEBOUNCE_MS     500

LiquidCrystal_I2C lcd(0x27, 16, 2);

int selectedSlot = 0; // 0=A, 1=B, 2=C
unsigned long lastPress = 0;
unsigned long lastDispense = 0;

void setup() {
    Serial.begin(9600);
    Serial.println("=== Vending Machine Dispenser ===");

    pinMode(CAP_SENSOR_PIN, INPUT);
    pinMode(RELAY_PIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT_PULLUP);

    digitalWrite(RELAY_PIN, LOW);

    lcd.init();
    lcd.backlight();

    // Initialize EEPROM with max inventory if first run
    for (int i = 0; i < 3; i++) {
        if (EEPROM.read(i) > MAX_INVENTORY || EEPROM.read(i) == 255) {
            EEPROM.write(i, MAX_INVENTORY);
        }
    }

    updateDisplay();
    Serial.println("System ready.");
}

void loop() {
    unsigned long now = millis();

    // Button press to cycle through slots
    if (digitalRead(BUTTON_PIN) == LOW && (now - lastPress > DEBOUNCE_MS)) {
        lastPress = now;
        selectedSlot = (selectedSlot + 1) % 3;
        updateDisplay();
        Serial.print("Selected slot: ");
        Serial.println((char)('A' + selectedSlot));
    }

    // Capacitive sensor detects hand — dispense item
    if (digitalRead(CAP_SENSOR_PIN) == HIGH && (now - lastDispense > DEBOUNCE_MS * 4)) {
        lastDispense = now;
        dispenseItem();
    }

    delay(50);
}

void dispenseItem() {
    int addr = selectedSlot; // EEPROM address matches slot index
    int count = EEPROM.read(addr);

    if (count <= 0) {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Slot ");
        lcd.print((char)('A' + selectedSlot));
        lcd.print(" EMPTY!");
        lcd.setCursor(0, 1);
        lcd.print("Please refill");

        Serial.println("ERROR: Slot empty!");
        delay(2000);
        updateDisplay();
        return;
    }

    // Activate relay to dispense
    Serial.print("Dispensing from Slot ");
    Serial.print((char)('A' + selectedSlot));
    Serial.println("...");

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Dispensing...");

    digitalWrite(RELAY_PIN, HIGH);
    delay(DISPENSE_TIME);
    digitalWrite(RELAY_PIN, LOW);

    // Update inventory in EEPROM
    count--;
    EEPROM.write(addr, count);

    Serial.print("Dispensed! Remaining: ");
    Serial.println(count);

    lcd.setCursor(0, 1);
    lcd.print("Done! Left: ");
    lcd.print(count);
    delay(1500);

    updateDisplay();
}

void updateDisplay() {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Vending Machine");
    lcd.setCursor(0, 1);

    // Show selected slot with inventory
    lcd.print(">");
    lcd.print((char)('A' + selectedSlot));
    lcd.print(":");
    lcd.print(EEPROM.read(selectedSlot));

    // Show all slots
    lcd.print(" A:");
    lcd.print(EEPROM.read(0));
    lcd.print(" B:");
    lcd.print(EEPROM.read(1));
    lcd.print(" C:");
    lcd.print(EEPROM.read(2));
}

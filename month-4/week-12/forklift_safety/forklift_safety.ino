/*
 * Week 12: Forklift Safety Alert
 * 
 * Ultrasonic sensor on forklift for pedestrian detection.
 * Activates buzzer and LED when object is within 2m.
 * Stops DC motor if object is dangerously close (<1m).
 * 
 * Components:
 *   - HC-SR04 Ultrasonic Sensor (Trig: pin 7, Echo: pin 6)
 *   - Piezo Buzzer (pin 8)
 *   - Red LED (pin 12)
 *   - Yellow LED (pin 11)
 *   - DC Motor via L293D H-Bridge (Enable: pin 5, IN1: pin 3, IN2: pin 4)
 * 
 * Wiring:
 *   HC-SR04 VCC  → 5V
 *   HC-SR04 GND  → GND
 *   HC-SR04 Trig → Pin 7
 *   HC-SR04 Echo → Pin 6
 *   Buzzer (+)   → Pin 8
 *   Buzzer (-)   → GND
 *   Red LED      → Pin 12 (via 220Ω)
 *   Yellow LED   → Pin 11 (via 220Ω)
 *   L293D EN1    → Pin 5 (PWM)
 *   L293D IN1    → Pin 3
 *   L293D IN2    → Pin 4
 */

// ── Pin Definitions ──────────────────────────────────────────
#define TRIG_PIN       7
#define ECHO_PIN       6
#define BUZZER_PIN     8
#define RED_LED_PIN    12
#define YELLOW_LED_PIN 11
#define MOTOR_EN_PIN   5
#define MOTOR_IN1_PIN  3
#define MOTOR_IN2_PIN  4

// ── Thresholds (cm) ──────────────────────────────────────────
#define DANGER_ZONE    100   // < 1m: STOP motor, rapid buzzer
#define WARNING_ZONE   200   // < 2m: slow buzzer, yellow LED

// ── Motor speed ──────────────────────────────────────────────
#define MOTOR_SPEED    200   // PWM value (0-255)

void setup() {
    Serial.begin(9600);
    Serial.println("=== Forklift Safety Alert System ===");

    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    pinMode(BUZZER_PIN, OUTPUT);
    pinMode(RED_LED_PIN, OUTPUT);
    pinMode(YELLOW_LED_PIN, OUTPUT);
    pinMode(MOTOR_EN_PIN, OUTPUT);
    pinMode(MOTOR_IN1_PIN, OUTPUT);
    pinMode(MOTOR_IN2_PIN, OUTPUT);

    // Start motor forward
    startMotor();
    Serial.println("Motor running. Monitoring for obstacles...");
}

void loop() {
    long distance = measureDistance();

    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");

    if (distance > 0 && distance < DANGER_ZONE) {
        // 🔴 DANGER — Stop motor, rapid buzzer
        stopMotor();
        digitalWrite(RED_LED_PIN, HIGH);
        digitalWrite(YELLOW_LED_PIN, LOW);

        // Rapid buzzer pattern
        for (int i = 0; i < 5; i++) {
            tone(BUZZER_PIN, 2000, 100);
            delay(150);
        }

        Serial.println("⚠️  DANGER! Object within 1m — MOTOR STOPPED!");

    } else if (distance > 0 && distance < WARNING_ZONE) {
        // 🟡 WARNING — Slow buzzer, motor continues
        startMotor();
        digitalWrite(RED_LED_PIN, LOW);
        digitalWrite(YELLOW_LED_PIN, HIGH);

        tone(BUZZER_PIN, 1000, 300);
        delay(500);

        Serial.println("⚠️  Warning: Object within 2m");

    } else {
        // 🟢 SAFE — Normal operation
        startMotor();
        digitalWrite(RED_LED_PIN, LOW);
        digitalWrite(YELLOW_LED_PIN, LOW);
        noTone(BUZZER_PIN);
    }

    delay(200);
}

long measureDistance() {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    long duration = pulseIn(ECHO_PIN, HIGH, 30000); // 30ms timeout
    if (duration == 0) return -1; // No echo
    return duration * 0.034 / 2; // Convert to cm
}

void startMotor() {
    analogWrite(MOTOR_EN_PIN, MOTOR_SPEED);
    digitalWrite(MOTOR_IN1_PIN, HIGH);
    digitalWrite(MOTOR_IN2_PIN, LOW);
}

void stopMotor() {
    analogWrite(MOTOR_EN_PIN, 0);
    digitalWrite(MOTOR_IN1_PIN, LOW);
    digitalWrite(MOTOR_IN2_PIN, LOW);
}

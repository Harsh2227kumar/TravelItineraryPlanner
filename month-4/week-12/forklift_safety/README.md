# Week 12: Forklift Safety Alert

## Objective
Implement an ultrasonic sensor on a forklift for pedestrian detection.
Activate buzzer and stop motor if an object is detected within 2m.

## Components Required
| Component | Quantity | Connection |
|-----------|----------|------------|
| Arduino Uno | 1 | — |
| HC-SR04 Ultrasonic Sensor | 1 | Trig→Pin7, Echo→Pin6 |
| Piezo Buzzer | 1 | Pin 8 |
| Red LED | 1 | Pin 12 + 220Ω |
| Yellow LED | 1 | Pin 11 + 220Ω |
| L293D Motor Driver | 1 | EN→Pin5, IN1→Pin3, IN2→Pin4 |
| DC Motor | 1 | Via L293D |
| Jumper Wires | ~15 | — |

## Behavior
| Distance | Alert Level | Action |
|----------|-------------|--------|
| > 2m | 🟢 Safe | Motor runs normally |
| 1m–2m | 🟡 Warning | Yellow LED + slow buzzer, motor still runs |
| < 1m | 🔴 Danger | Red LED + rapid buzzer, **motor STOPPED** |

## Wiring Diagram
```
Arduino Uno
    ┌────────────┐
    │  Pin 7 ────┤──── HC-SR04 Trig
    │  Pin 6 ────┤──── HC-SR04 Echo
    │  Pin 8 ────┤──── Buzzer (+)
    │  Pin 12 ───┤──── Red LED (+) via 220Ω
    │  Pin 11 ───┤──── Yellow LED (+) via 220Ω
    │  Pin 5 ────┤──── L293D Enable (PWM)
    │  Pin 3 ────┤──── L293D IN1
    │  Pin 4 ────┤──── L293D IN2
    │  5V ───────┤──── HC-SR04 VCC, L293D VCC
    │  GND ──────┤──── All GND connections
    └────────────┘
```

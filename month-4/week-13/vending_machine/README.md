# Week 13: Vending Machine Dispenser

## Objective
Use a capacitive proximity sensor to detect hand, dispense item via relay,
and count inventory stored in EEPROM.

## Components Required
| Component | Quantity | Connection |
|-----------|----------|------------|
| Arduino Uno | 1 | — |
| Capacitive Proximity Sensor | 1 | Pin 2 |
| Relay Module (5V) | 1 | Pin 7 |
| Push Button | 1 | Pin 3 (internal pull-up) |
| 16x2 LCD (I2C) | 1 | SDA→A4, SCL→A5 |
| DC Motor (dispenser) | 1 | Via Relay |
| Jumper Wires | ~12 | — |

## Features
- **3 Slots (A, B, C)** — cycle with button press
- **EEPROM** — inventory persists across power cycles
- **LCD Display** — shows selected slot and inventory counts
- **Capacitive Sensor** — contactless hand detection for dispensing

## Wiring Diagram
```
Arduino Uno
    ┌────────────┐
    │  Pin 2 ────┤──── Capacitive Sensor OUT
    │  Pin 3 ────┤──── Push Button (to GND)
    │  Pin 7 ────┤──── Relay IN
    │  A4 ───────┤──── LCD SDA
    │  A5 ───────┤──── LCD SCL
    │  5V ───────┤──── Sensor VCC, Relay VCC, LCD VCC
    │  GND ──────┤──── All GND connections
    └────────────┘
```

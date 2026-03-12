# Week 15: Parking Slot Occupancy

## Objective
PIR proximity sensors monitor vehicle entry/exit at parking slots.
Update slot status array and transmit via Bluetooth.

## Components Required
| Component | Quantity | Connection |
|-----------|----------|------------|
| Arduino Uno | 1 | — |
| PIR Motion Sensor | 3 | Pins 2, 3, 4 |
| HC-05 Bluetooth Module | 1 | TX→Pin10, RX→Pin11 |
| Red LED | 3 | Pins 5, 6, 7 + 220Ω |
| Green LED | 3 | Pins 8, 9, 12 + 220Ω |
| 16x2 LCD (I2C) | 1 | SDA→A4, SCL→A5 |

## Features
- **3 parking slots** monitored independently
- **Red/Green LED** per slot — visual indicator
- **LCD Display** — shows free count and per-slot status
- **Bluetooth** — transmits JSON status every 2 seconds
- **Auto-vacancy** — slot marked free after 10s of no motion

## Bluetooth Data Format
```json
{"slots":[{"id":1,"status":"occupied"},{"id":2,"status":"free"},{"id":3,"status":"free"}]}
```

## Wiring Diagram
```
Arduino Uno
    ┌────────────┐
    │  Pin 2 ────┤──── PIR Sensor 1 (Slot 1)
    │  Pin 3 ────┤──── PIR Sensor 2 (Slot 2)
    │  Pin 4 ────┤──── PIR Sensor 3 (Slot 3)
    │  Pin 5-7 ──┤──── Red LEDs (via 220Ω)
    │  Pin 8,9,12┤──── Green LEDs (via 220Ω)
    │  Pin 10 ───┤──── HC-05 TX
    │  Pin 11 ───┤──── HC-05 RX (via voltage divider)
    │  A4 ───────┤──── LCD SDA
    │  A5 ───────┤──── LCD SCL
    │  5V ───────┤──── All VCC
    │  GND ──────┤──── All GND
    └────────────┘
```

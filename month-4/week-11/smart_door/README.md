# Week 11: Smart Door Automation

## Objective
Design a system using an IR proximity sensor to detect user approach,
trigger a servo motor for door open/close, and log events via Serial.

## Components Required
| Component | Quantity | Connection |
|-----------|----------|------------|
| Arduino Uno | 1 | — |
| IR Proximity Sensor | 1 | Digital Pin 2 |
| Servo Motor (SG90) | 1 | Digital Pin 9 |
| LED (Green) | 1 | Pin 13 + 220Ω resistor |
| Jumper Wires | ~10 | — |
| Breadboard | 1 | — |

## Wiring Diagram
```
Arduino Uno
    ┌────────────┐
    │            │
    │  Pin 2 ────┤──── IR Sensor OUT
    │  Pin 9 ────┤──── Servo Signal (Orange)
    │  Pin 13 ───┤──── LED (+) via 220Ω
    │  5V ───────┤──── IR VCC, Servo VCC (Red)
    │  GND ──────┤──── IR GND, Servo GND (Brown), LED (-)
    │            │
    └────────────┘
```

## How It Works
1. IR sensor continuously monitors for nearby objects
2. When a person approaches (sensor goes LOW), the servo rotates to 90° (door opens)
3. Green LED turns on to indicate door is open
4. After 5 seconds, servo returns to 0° (door closes), LED turns off
5. Each event is logged to Serial Monitor with timestamp and event number

## Testing in Tinkercad
1. Go to [tinkercad.com/circuits](https://www.tinkercad.com/circuits)
2. Add: Arduino Uno, IR Sensor, Servo Motor, LED, 220Ω resistor
3. Wire as shown above
4. Copy `smart_door.ino` into the code editor
5. Click "Start Simulation" and trigger the IR sensor

## Serial Output Example
```
=== Smart Door Automation System ===
Initializing...
System ready. Monitoring for approach...
------------------------------------
[EVENT #1] Person detected at 3s — Opening door.
[EVENT #1] Door closed.
------------------------------------
```

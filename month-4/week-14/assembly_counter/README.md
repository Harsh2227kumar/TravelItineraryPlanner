# Week 14: Assembly Line Object Counter

## Objective
Inductive sensor detects metal parts on a conveyor, increments counter,
and sends data to LCD serially.

## Components Required
| Component | Quantity | Connection |
|-----------|----------|------------|
| Arduino Uno | 1 | — |
| Inductive Proximity Sensor (NPN) | 1 | Pin 2 + 10kΩ pull-up |
| 16x2 LCD (I2C) | 1 | SDA→A4, SCL→A5 |
| Green LED | 1 | Pin 12 + 220Ω |
| Red LED | 1 | Pin 11 + 220Ω |

## Features
- Real-time part count with debouncing
- Parts/minute rate calculation
- Green LED flash per part detected
- Red LED flash every 10 parts (milestone)
- Batch completion logging every 50 parts
- LCD shows count and rate

## Serial Output Example
```
=== Assembly Line Object Counter ===
Time(s) | Count | Rate(parts/min)
--------|-------|----------------
2s      | 1     | 30.0 parts/min
4s      | 2     | 30.0 parts/min
...
20s     | 10    | 30.0 parts/min
>>> BATCH COMPLETE <<<
```

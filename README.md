# Pressure-Activated Audio System (Arduino + MP3-TF-16P + FSR402)

## Overview

This system uses a **Force Sensitive Resistor (FSR402)** to detect applied pressure and trigger audio playback through an **MP3-TF-16P / DFPlayer Mini** module controlled by an **Arduino**.

When pressure exceeds a threshold, the Arduino sends a serial command to the MP3 module to play a preloaded sound file.  
It’s a simple, reliable way to make **pressure-sensitive interactive devices** or **sound-triggered systems**.

---

## Features

- Pressure detection using **FSR402**
- MP3 playback via **MP3-TF-16P / DFPlayer Mini**
- Adjustable **trigger threshold** and **hysteresis**
- Single playback per activation (no repetition)
- Compact and USB 5 V powered

---

## Hardware Components

| Component | Qty | Description |
|------------|-----|-------------|
| Arduino Nano / Uno | 1 | Main controller |
| MP3-TF-16P / DFPlayer Mini | 1 | MP3 playback module |
| FSR402 sensor | 1 | Force Sensitive Resistor |
| Resistor 10 kΩ | 1 | Forms voltage divider with FSR |
| Resistor 1 kΩ | 1 | Between D10 and DFPlayer RX |
| MicroSD card (FAT32) | 1 | Stores audio files |
| Speaker 8 Ω / 3 W | 1 | Connects to DFPlayer SPK+ / SPK– |
| USB 5 V Power Source | 1 | Arduino power |
| Jumper wires | — | Connections |

---

## Wiring

| From | Pin | To | Pin | Notes |
|------|-----|----|-----|-------|
| Arduino | 5V | FSR402 | one leg | Power |
| Arduino | A0 | FSR402 + 10 kΩ resistor | junction | Analog signal |
| Arduino | GND | 10 kΩ resistor | other leg | Ground |
| Arduino | D10 | MP3-TF-16P | RX *(via 1 kΩ resistor)* | Serial TX |
| Arduino | D11 | MP3-TF-16P | TX | Serial RX |
| Arduino | 5V | MP3-TF-16P | VCC | Power |
| Arduino | GND | MP3-TF-16P | GND | Common ground |
| DFPlayer | SPK+ / SPK– | Speaker | — | Audio output |

**Note:** Keep all grounds common between Arduino, DFPlayer, and FSR circuit.

---

## SD Card Setup

Your microSD card should be formatted as **FAT32** and contain an mp3 folder of yoour sounds. 
<32gb is preferred. 

## Library used

Make sure to install the DFRobotDFPlayerMini library and to include the mp3tf16p.h in the folder. 
mp3tf16p.h provided by https://dev.azure.com/overlording/The%20Last%20Outpost%20Workshop/_git/MP3-TF-16P
 -> Make sure to watch his content if you have some common errors.  

#!/usr/bin/env python

### ###########################
### Countdown
### ###########################
LATCH = 23 # Pin 12 Latch clock
CLK = 27 # Pin 11 shift clock
dataBit = 22 # Pin 14 A
BeepPin = 24

### ###########################
### Buttons
### ###########################
startButton = 25
stopButton = 9

### ###########################
### Sensors
### ###########################
sensors = {1: 18, 2:17}

events = {0: "start", 1: "sensor 1", 2: "sensor 2", 3: "stop", 4: "reset"}

filename = "results.txt"
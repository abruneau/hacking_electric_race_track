#!/usr/bin/env python

### ###########################
### Countdown
### ###########################
LATCH = 17 # Pin 12 Latch clock
CLK = 27 # Pin 11 shift clock
dataBit = 4 # Pin 14 A
BeepPin = 26

### ###########################
### Buttons
### ###########################
startButton = 19
stopButton = 13

### ###########################
### Sensors
### ###########################
sensors = {1: 5, 2:6}

events = {0: "start", 1: "sensor 1", 2: "sensor 2", 3: "stop", 4: "reset"}

filename = "results.txt"

# def log(f, t, e, p):
#     try:
#         lock.acquire()

#         event = {
#             "time": t.isoformat(),
#             "event": e
#         }

#         j = json.dumps(event)

#         f.write("{0}\n".format(j))
#         f.flush()

#         lock.release()
#         if p:
#             print t, env.events[e]
#     except Exception as e: 
#         print("An exception occurred")
#         print(e)
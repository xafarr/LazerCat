#!/usr/bin/python
# Import required libraries
import sys
import time

import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO signals to use
# Physical pins 11,15,16,18
# GPIO17,GPIO22,GPIO23,GPIO24
StepPins = [17, 22, 23, 24]

# Set all pins as output
for pin in StepPins:
    print
    "Setup pins"
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

# Define advanced sequence
# as shown in manufacturers datasheet
Seq = [[1, 0, 0, 1],
       [1, 0, 0, 0],
       [1, 1, 0, 0],
       [0, 1, 0, 0],
       [0, 1, 1, 0],
       [0, 0, 1, 0],
       [0, 0, 1, 1],
       [0, 0, 0, 1]]

StepCount = len(Seq)
StepDir = 1  # Set to 1 or 2 for clockwise
# Set to -1 or -2 for anti-clockwise

# Read wait time from command line
if len(sys.argv) > 1:
    WaitTime = int(sys.argv[1]) / float(10000)
else:
    WaitTime = 10 / float(10000)

# Initialise variables
StepCounter = 0

directionSwitchCounter = 0

# Start main loop
while True:

    print("StepCounter = " + str(StepCounter))
    print("Seq[StepCounter] = " + str(Seq[StepCounter]) )

    for pin in range(0, 4):
        xpin = StepPins[pin]
        if Seq[StepCounter][pin] != 0:
            print("Enable GPIO " + str(xpin))
            GPIO.output(xpin, True)
        else:
            GPIO.output(xpin, False)

    StepCounter += StepDir


    # If we reach the end of the sequence
    # start again
    if (StepCounter >= StepCount):
        directionSwitchCounter += 1
        StepCounter = 0
    if (StepCounter < 0):
        directionSwitchCounter += 1
        StepCounter = StepCount + StepDir
    if directionSwitchCounter >= 500:
        directionSwitchCounter = 0
        if StepDir == 1:
            StepDir = -1
        else:
            StepDir = 1

    # Wait before moving on
    time.sleep(WaitTime)

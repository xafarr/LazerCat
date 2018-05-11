#!/usr/bin/python

# MIT License
# 
# Copyright (c) 2017 John Bryan Moore
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import time
from gtts import gTTS
import os

import RPi.GPIO as GPIO
import VL53L0X

from test import setupStepperPins, mainStepper

# Create a VL53L0X object
tof = VL53L0X.VL53L0X()
setupStepperPins()
tts=gTTS(text='Wash you hands, animal', lang='en')
tts.save("wash.mp3")

# Start ranging
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

timing = tof.get_timing()
if (timing < 20000):
    timing = 20000
print("Timing %d ms" % (timing / 1000))

count = 0
while True:
    count = +count
    distance = tof.get_distance()
    if (distance > 0):
        print("%d mm, %d cm, %d" % (distance, (distance / 10), count))
        if (distance < 800):
            mainStepper()
            os.system("mpg321 wash.mp3")

    time.sleep(timing / 1000000.00)


# tof.stop_ranging()

def setupStepperPins():
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


def mainStepper():
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

    StepPins = [17, 22, 23, 24]
    StepCount = len(Seq)
    StepDir = -1  # Set to 1 or 2 for clockwise
    # Set to -1 or -2 for anti-clockwise

    # Read wait time from command line
    if len(sys.argv) > 1:
        WaitTime = int(sys.argv[1]) / float(18000)
    else:
        WaitTime = 10 / float(18000)

    # Initialise variables
    StepCounter = 0

    directionSwitchCounter = 0

    counter = 6

    # Start main loop
    while True:

        print("StepCounter = " + str(StepCounter))
        print("Seq[StepCounter] = " + str(Seq[StepCounter]))

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
        if directionSwitchCounter >= 100:
            directionSwitchCounter = 0
            counter -= 1
            if counter == 0:
                break
            if StepDir == 1:
                StepDir = -1
            else:
                StepDir = 1

        # Wait before moving on
        time.sleep(WaitTime)

# if __name__ == '__main__':
#     setupStepperPins()
#     p1 = Process(target=mainStepper)
#     p2 = Process(target=func2)
#     p1.start()
#     p2.start()

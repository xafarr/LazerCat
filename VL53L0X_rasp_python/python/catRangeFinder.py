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

import os
import random
import sys
import time
from multiprocessing import Process

import RPi.GPIO as GPIO
import VL53L0X

Freq = 100 #Hz
GPIO.setmode(GPIO.BCM)
red = 4
green = 5
blue = 6

redd = 13
greenn = 19
bluee = 26

# Set GPIO to Broadcom system and set RGB Pin numbers
# Set pins to output mode
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

GPIO.setup(redd, GPIO.OUT)
GPIO.setup(greenn, GPIO.OUT)
GPIO.setup(bluee, GPIO.OUT)

# Setup all the LED colors with an initial
# duty cycle of 0 which is off
RED = GPIO.PWM(red, Freq)
RED.start(0)
GREEN = GPIO.PWM(green, Freq)
GREEN.start(0)
BLUE = GPIO.PWM(blue, Freq)
BLUE.start(0)

REDD = GPIO.PWM(redd, Freq)
REDD.start(0)
GREENN = GPIO.PWM(greenn, Freq)
GREENN.start(0)
BLUEE = GPIO.PWM(bluee, Freq)
BLUEE.start(0)

def setupPins():
    # Use BCM GPIO references
    # instead of physical pin numbers
    # GPIO.setmode(GPIO.BCM)

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


def washYourHands():
    washChoices = ['this is the police, wash your hands',
                   'wash your hands you filthy animal',
                   'please wash your hands']
    washChoice = random.choice(washChoices)
    os.system("espeak \"" + washChoice + "\" 2>/dev/null ")

# Define a simple function to turn on the LED colors
def color(R, G, B, on_time):
    # Color brightness range is 0-100%
    RED.ChangeDutyCycle(R)
    GREEN.ChangeDutyCycle(G)
    BLUE.ChangeDutyCycle(B)

    REDD.ChangeDutyCycle(R)
    GREENN.ChangeDutyCycle(G)
    BLUEE.ChangeDutyCycle(B)
    time.sleep(on_time)

    # Turn all LEDs off after on_time seconds
    RED.ChangeDutyCycle(0)
    GREEN.ChangeDutyCycle(0)
    BLUE.ChangeDutyCycle(0)

    REDD.ChangeDutyCycle(0)
    GREENN.ChangeDutyCycle(0)
    BLUEE.ChangeDutyCycle(0)

def lightLoop():
    # Main loop
    try:
        # while RUNNING:
        for x in range(0, 10000):
            for x in range(0, 2):
                for y in range(0, 2):
                    for z in range(0, 2):
                        print(x, y, z)
                        # Slowly ramp up power percentage of each active color
                        for i in range(0, 101):
                            color((x * i), (y * i), (z * i), .002)

    # If CTRL+C is pressed the main loop is broken
    # except KeyboardInterrupt:
    #     RUNNING = False
    #     print("Quitting")

    # Actions under 'finally' will always be called
    # regardless of what stopped the program
    finally:
        # Stop and cleanup so the pins
        # are available to be used again
        GPIO.cleanup()


def runWarning():
    stepper = Process(target=mainStepper)
    voice = Process(target=washYourHands)
    light = Process(target=lightLoop)
    stepper.start()
    voice.start()
    light.start()


if __name__ == '__main__':
    # setupStepperPins()
    # p1 = Process(target=mainStepper)
    # p2 = Process(target=func2)
    # p1.start()
    # p2.start()
    # Create a VL53L0X object
    tof = VL53L0X.VL53L0X()
    setupPins()
    # tts=gTTS(text='Wash you hands, animal', lang='en')
    # tts.save("wash.mp3")

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
                tof.stop_ranging()
                runWarning()
                tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

        time.sleep(timing / 1000000.00)

    # tof.stop_ranging()

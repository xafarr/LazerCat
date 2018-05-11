#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  RGB_LED.py
#
# A short program to control an RGB LED by utilizing
# the PWM functions within the Python GPIO module
#
#  Copyright 2015  Ken Powers
#   
 
# Import the modules used in the script
import random, time
import RPi.GPIO as GPIO
 
# Set GPIO to Broadcom system and set RGB Pin numbers
RUNNING = True
GPIO.setmode(GPIO.BCM)
red = 4
green = 5
blue = 6

redd = 13
greenn = 19
bluee = 26

 
# Set pins to output mode
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

GPIO.setup(redd, GPIO.OUT)
GPIO.setup(greenn, GPIO.OUT)
GPIO.setup(bluee, GPIO.OUT)


Freq = 100 #Hz
 
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

 
print("Light It Up!")
print("Press CTRL + C to quit.\n")
print(" R  G  B\n---------")


if __name__ == '__main__' :
    # Main loop
    try:
        while RUNNING:
            for x in range(0,2):
                for y in range(0,2):
                    for z in range(0,2):
                        print (x,y,z)
                        # Slowly ramp up power percentage of each active color
                        for i in range(0,101):
                            color((x*i),(y*i),(z*i), .002)
     
    # If CTRL+C is pressed the main loop is broken
    except KeyboardInterrupt:
        RUNNING = False
        print("Quitting")
     
    # Actions under 'finally' will always be called
    # regardless of what stopped the program
    finally:
        # Stop and cleanup so the pins
        # are available to be used again
        GPIO.cleanup()



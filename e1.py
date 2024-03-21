# EG2310
# This code is used to control the servo
# Students will be given this code but will need to understand how it works
# Additional h/w exercise is to write a function to turn the servo by an angle
# The servo motor may be chosen to tilt the payload
import RPi.GPIO as GPIO
from time import sleep
# Set pin numbering convention
GPIO.setmode(GPIO.BCM)
# Choose an appropriate pwm channel to be used to control the servo
servo_pin = 21
# Set the pin as an output
GPIO.setup(servo_pin, GPIO.OUT)
# Initialise the servo to be controlled by pwm with 50 Hz frequency
p = GPIO.PWM(servo_pin, 50)
# Set servo to 90 degrees as it's starting position
p.start(7.5)

def rotate_servo(angle):
    dc = 2.5 + angle / 18 
    p.ChangeDutyCycle(dc)

try:
    while True:

        angle = 180
        rotate_servo(angle)
        sleep(0.3)
        angle = 0
        rotate_servo(angle)
        sleep(0.3)


except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
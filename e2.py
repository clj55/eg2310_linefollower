from time import sleep 
import RPi.GPIO as GPIO
# Set pin numbering convention
GPIO.setmode(GPIO.BCM)
# Choose an appropriate pwm channel to be used to control the servo
pin = 21
# Set the pin as an output
GPIO.setup(pin, GPIO.OUT)

try:
    while True:
        GPIO.output(12, 1)
        sleep(0.2)
        GPIO.output(12, 0)
        sleep(1)


except KeyboardInterrupt:
    GPIO.cleanup()
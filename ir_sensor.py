import RPi.GPIO as GPIO
from time import sleep

# Set pin numbering convention
GPIO.setmode(GPIO.BCM)
# Choose an appropriate pwm channel to be used to control the servo
ir1_pin = 19
ir2_pin = 26
# Set the pin as an output
GPIO.setup(ir1_pin, GPIO.IN)
GPIO.setup(ir2_pin, GPIO.IN)


try:
    while True:
        ir1 = GPIO.input(ir1_pin)
        ir2 = GPIO.input(ir2_pin)
        print(f'ir1: {ir1} | ir2: {ir2}')
        sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()


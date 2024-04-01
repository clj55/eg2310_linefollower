import rclpy
from rclpy.node import Node
import geometry_msgs.msg
import RPi.GPIO as GPIO
from time import sleep, time
import requests
import math
from threading import Timer

# setting up all the GPIO for functionality
GPIO.setmode(GPIO.BCM)
ir1_pin = 17
ir2_pin = 27
servo1_pin = 25
servo2_pin = 21

GPIO.setup(ir1_pin, GPIO.IN)
GPIO.setup(ir2_pin, GPIO.IN)
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)

def convert_ang_dc(angle):
    dc = 2.5 + angle / 18 
    return dc

# Function: Request HTTP
esp32_ip = '172.20.10.5'
turtleBot_ID = 43
header = {'Content-Type': 'application/json'}

# Class 1: Functionality of the turtleBot3 Burger
class Func(Node):
    # initialiser
    def __init__():
        super().__init__('mover')
        self.publisher_ = self.create_publisher(geometry_msgs.msg.Twist, 'cmd_vel', 10)

    # Function 1: Line_follower
    def line_follower(self):
        twist = geometry_msgs.msg.Twist()
        rad_per_sec = 0.3
        cent_per_sec = 0.1
        turning_rate = 0.08 
        linear_rate = 0.05
        try:
            while True:
                ir1 = GPIO.input(ir1_pin)
                ir2 = GPIO.input(ir2_pin)
                print(f'ir1: {ir1} | ir2: {ir2}')
                twist.linear.x = cent_per_sec
                self.publisher_.publish(twist)
                
                if ir1 == 1 and ir2 == 1:
                    twist.linear.x = 0.0
                    twist.angular.z = 0.0
  
                elif ir1 == 1 and ir2 == 0:
                    twist.angular.z += rad_per_sec * turning_rate
                    twist.linear.x += cent_per_sec * linear_rate

                elif ir2 == 1 and ir1 == 0:
                    twist.linear.z -= rad_per_sec * turning_rate
                    twist.linear.x += cent_per_sec * linear_rate

                else: 
                    twist.linear.z = 0.0
                    twist.linear.x = cent_per_sec
                
                self.publisher_.publish(twist)
        
        except Exception as e:
            print(e)
        
        # Ctrl-c detected
        finally:
        	# stop moving
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.publisher_.publish(twist)
    
    # Function 2: Ball Dispenser
    def ball_dispenser():
        s1 = GPIO.PWM(servo1_pin, 50)
        s2 = GPIO.PWM(servo2_pin, 50)
        counter = 0

        while counter <= 10:
            s1.ChangeDutyCycle(convert_ang_dc(90))
            s2.ChangeDutyCycle(convert_ang_dc(90))
            counter += 1
        
        s1.ChangeDutyCycle(convert_ang_dc(0))
        s2.ChangeDutyCycle(convert_ang_dc(0))

    # Function 3: HTTP request to ESP32 --> needs to be tested as I didn't test it as a function
    def send_request(self, ip_address, ID):
        header = {'Content-Type': 'application/json'}
        endpoint = "http://" + ip_address + "/openDoor"
        data = "action": "openDoor", "parameters": {"robotId": ID}}
        response = requests.post(url=endpoint, json=data, headers=header)
        return(response.text)

    # Function 4: Specific turns in radians (turning within its own space)
    def turn_specific(self, radian):
        twist = geometry_msgs.msg.Twist()
        if radian < 0:
            rad_per_sec = -0.3
        else:
            rad_per_sec = 0.3
        time_90 = abs(radian / rad_per_sec)
        twist.angular.z = rad_per_sec
        th.Timer(time_90, twist.angular.z = 0.0)

    # Function 5: Marker Detector --> this one needs to be implemented with the Frontier and A* algo?
    def marker_detector(self):
        # twist = geometry_msgs.msg.Twist()
        # ir1 = GPIO.input(ir1_pin)
        # ir2 = GPIO.input(ir2_pin)
        # if ir1 == 1 and ir2 == 1:
        #     twist.linear.x = 0.0
        #     self.publisher_.publish(twist)
        pass
        

def main(args=None):
    rclpy.init(args=args)
    TurtleBot = Func()
    # finds the marker
    TurtleBot.marker_detector()
    # sends HTTP request to determine which door to open
    response = 'no'
    while response == 'no':
        response = TurtleBot.send_request(esp32_ip, turtleBot_ID)
        if response == 'door1':
            TurtleBot.turn_specific(math.pi / 2)
            break
        elif response == 'door2':
            TurtleBot.turn_specific(- math.pi / 2)
            break
        else:
            th.Timer(60, response = 'no')
    # line follows to the bucket
    TurtleBot.line_follower()
    # dispense balls
    TurtleBot.ball_dispenser()
    # turns 180 degrees
    TurtleBot.turn_specific(math.pi)
    # follows line backward
    TurtleBot.line_follower()
    
if __name__ == '__main__':
    main()

import rclpy
from rclpy.node import Node
import geometry_msgs.msg
import RPi.GPIO as GPIO
from time import sleep, time

# Set pin numbering convention
GPIO.setmode(GPIO.BCM)
# Choose an appropriate pwm channel to be used to control the servo
ir1_pin = 17
ir2_pin = 27
servo1 = 25
servo2 = 21
motor = 12
# Set the pin as an output
GPIO.setup(ir1_pin, GPIO.IN)
GPIO.setup(ir2_pin, GPIO.IN)
GPIO.setup(servo1, GPIO.OUT)
GPIO.setup(servo2, GPIO.OUT)
GPIO.setup(motor, GPIO.OUT)


s1 = GPIO.PWM(servo1, 50)
s2 = GPIO.PWM(servo2, 50)
m = GPIO.PWM(motor, 50)
open_angle = 90
close_angle = 0

# constants
rotatechange = 0.3
speedchange = -0.03


def convert_ang_dc(angle):
    dc = 2.5 + angle / 18 
    return dc


class Mover(Node):
    def __init__(self):
        super().__init__('mover')
        self.publisher_ = self.create_publisher(geometry_msgs.msg.Twist,'cmd_vel',10)
    
    def read_ir(self):
        twist = geometry_msgs.msg.Twist()
        try:
            counter = 0
            motor_start = False
            s1open = False
            s2open = False
            open_dc= convert_ang_dc(open_angle)
            close_dc = convert_ang_dc(close_angle)

            while True:
                ir1 = GPIO.input(ir1_pin)
                ir2 = GPIO.input(ir2_pin)
                print(f'ir1: {ir1} | ir2: {ir2}')

                twist.linear.x = speedchange


                #TODO: Control Servos and Motors
                if ir1 == 1 and ir2 == 1:
                    twist.linear.x = 0.0
                    twist.angular.z = 0.0
                    counter += 1
                    last_time = time.time()

                    if motor_start == False:
                         m.start(50)
                    elif s1open == False:
                        s1.ChangeDutyCycle(open_dc)
                        s1open = True
                    elif (last_time - time.time()) > 1:
                        s2.ChangeDutyCycle(open_dc)
                        s2open = True
                    
                elif ir1 == 1:
                    twist.angular.z += rotatechange
                    sleep(0.5)
                elif ir2 == 1:
                    twist.angular.z -= rotatechange
                    sleep(0.5)
                else: 
                    twist.angular.z = 0.0
                
                self.publisher_.publish(twist)
        
        except Exception as e:
            print(e)
        
        # Ctrl-c detected
        finally:
        	# stop moving
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.publisher_.publish(twist)


def main(args=None):
    rclpy.init(args=args)

    mover = Mover()
    mover.read_ir()


    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    mover.destroy_node()
    
    rclpy.shutdown()


if __name__ == '__main__':
    main()

import pygame
import gpiozero
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
drive_motor = GPIO.PWM(17, 100)
steering_motor = gpiozero.AngularServo(18, min_angle=-60, max_angle=60)


pygame.init()

controller = pygame.joystick.Joystick(0)
controller.init()

axis = {}
button = {}

# Accelerometers identifiers
AXIS_X = 6
AXIS_Y = 7

#variables to store rotations in, initialized to zero
rot_x = 0.0
rot_y = 0.0

x_angle = 0

def steer(angle):
    if angle < -60:
        angle = -60
    elif angle > 60:
        angle = 60
    elif angle > -15 and angle < 15:
        angle = 0
    steering_motor.angle = angle
    
def drive(speed):
    if speed < 40:
        speed = 40
    elif speed > 100:
        speed = 100
    drive_motor.ChangeDutyCycle(speed)
        
def translate(value, left_min, left_max, right_min, right_max):
    leftSpan = left_max - left_min
    rightSpan = right_max - right_min
    
    valueScaled = float(value-left_min) / float(leftSpan)
    
    return right_min + (valueScaled * rightSpan)
drive_motor.start(1)
while True:
    axis[AXIS_X] = rot_x
    axis[AXIS_Y] = rot_y
    
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            axis[event.axis] = round(event.value,2)
        elif event.type == pygame.JOYBUTTONDOWN:
            button[event.button] = True
        elif event.type == pygame.JOYBUTTONUP:
            button[event.button] = False

        rot_x = axis[AXIS_X]
        rot_y = axis[AXIS_Y]
        
        print("x: " + str(rot_x) + ", rated: " + str(translate(rot_x, -0.55, 0.55, -45, 45)))
        print("y: " + str(rot_y) + ", rated: " + str(translate(rot_y, -0.55, 0.55, 0, 100)))
        
        steer(translate(rot_x, -0.55, 0.55, -45, 45))
        drive(translate(rot_y, -0.65, 0.65, 40, 100))

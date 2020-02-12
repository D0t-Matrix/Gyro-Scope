import pygame
import gpiozero
import numpy as np

steering = gpiozero.AngularServo(18, min_angle=-60, max_angle=60)
drive = gpiozero.Motor(17, 21, enable=None, pwm=True, pin_factory=None)

pygame.init()
controller = pygame.joystick.Joystick(0)
controller.init()

axis = {}
button = {}
AXIS_X = 6
AXIS_Y = 7

def steer(angle):
    if angle < -60:
        angle = -60
    elif angle > 60:
        angle = 60
    elif angle > -15 and angle < 15:
        angle = 0
    steering.angle = angle

def drive(speed):
    if speed > 0.15:
        drive.forward(speed)
    elif speed < -0.15:
        drive.backward((speed * -1))
    else:
        drive.stop()

while True:
    axis[AXIS_X] = rot_x
    axis[AXIS_Y] = rot_y
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            axis[event.axis] = round(event.value,2)
        rot_x = axis[AXIS_X]
        rot_y = axis[AXIS_Y]
        steer(rot_x * 100)
        drive(np.interp(rot_y, -0.65, 0.65, -1, 1))
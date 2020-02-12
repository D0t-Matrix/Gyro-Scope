import gpiozero
import numpy as np
import cwiid
steering = gpiozero.AngularServo(18, min_angle=-60, max_angle=60)
drive = gpiozero.Motor(17, 21, enable=None, pwm=True, pin_factory=None)
wii = cwiid.Wiimote()
wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
def steer(angle):
    if np.absolute(angle) < 5:
        angle = 0
    steering.angle = angle
def drive(speed):
    if np.absolute(speed) < 0.15:
        drive.stop()
    elif speed < 0:
        drive.backward(abs(speed))
    else:
        drive.forward(speed)
while True:
    steer(np.clip(np.interp(wii.state["acc"][cwiid.X] - 95), 0, 50, -50, 50), -60, 60)
    drive(np.clip(np.interp(wii.state["acc"][cwiid.Y] - 95), 0, 50, -1, 1), -1, 1)
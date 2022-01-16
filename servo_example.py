from servo import Servo
import math
from time import sleep

with Servo(17) as s:
    s.set(math.pi/4)
    sleep(0.5)
    s.set(math.pi/2)
    sleep(0.5)
    s.set(math.pi/4)
    sleep(0.5)
    s.set(0)
    sleep(0.5)
    s.set(-math.pi/4)
    sleep(0.5)
    s.set(-math.pi/2)
    sleep(0.5)
    s.set(-math.pi/4)
    sleep(0.5)
    s.set(0)
    sleep(0.5)

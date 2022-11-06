from digitalio import DigitalInOut, Direction
from board import LED

led = DigitalInOut(LED)
led.direction = Direction.OUTPUT

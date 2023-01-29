from machine import UART

from sen0386 import readSensorValues, UNDEFINED

uart = UART(2, 9600)
uart.init(9600, bits=8, parity=None, stop=1)

while True:
    ax, ay, az, wx, wy, wz, roll, pitch, yaw = readSensorValues(uart)
    if yaw is not UNDEFINED:
        print(yaw)



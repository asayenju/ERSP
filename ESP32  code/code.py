import time
import board
import adafruit_mpu6050
import busio

i2c = busio.I2C(sda=board.IO1,scl=board.IO0)
# i2c = board.I2C()  # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c)

while True:
    ax, ay, az = mpu.acceleration
    gx, gy, gz = mpu.gyro
    print("%.6f, %.6f, %.6f, %.6f, %.6f, %.6f" % (ax, ay, az, gx, gy, gz))
    time.sleep(0.01)
from easytello import tello
import cv2
import time


drone = tello.Tello()
time.sleep(1)

drone.takeoff()
time.sleep(1)
print(drone.tello_ip)

drone.streamon()
for i in range(1000):
	drone.ccw(25)


drone.land()

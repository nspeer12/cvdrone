from tello import *
from stats import *
import cv2
import time
import pandas as pd

cols = ['time', 'battery', 'height', ' acceleration', 'baro', 'attitude', 'tof']

drone = Tello()
print(drone.tello_ip)
#drone.streamon()

for i in range(10):
	log =[drone.get_time(),
		drone.get_battery(),
		drone.get_height(),
		drone.get_acceleration(),
		drone.get_attitude(),
		drone.get_tof(),
		drone.get_baro()]

	print(log)

drone.streamon()
print('streamon')
drone._video_thread()
print('video thread')

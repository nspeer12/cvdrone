# simple example demonstrating how to control a Tello using your keyboard.
# For a more fully featured example see manual-control-pygame.py
# 
# Use W, A, S, D for moving, E, Q for rotating and R, F for going up and down.
# When starting the script the Tello will takeoff, pressing ESC makes it land
#  and the script exit.

from djitellopy import Tello
import cv2, math, time
import numpy as np

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture(0)



tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

#tello.takeoff()

while True:
	# In reality you want to display frames in a seperate thread. Otherwise
	#  they will freeze while the drone moves.
	frame = frame_read.frame

	frame = cv2.resize(frame, (640, 480))
	# using a greyscale picture, also for faster detection
	gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

	# detect people in the image
	# returns the bounding boxes for the detected objects
	boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )

	boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

	for (xA, yA, xB, yB) in boxes:
		# display the detected boxes in the colour picture
		cv2.rectangle(frame, (xA, yA), (xB, yB),  (0, 255, 0), 2)
	
	# Write the output video 
	#out.write(frame.astype('uint8'))
	# Display the resulting frame
	cv2.imshow('frame',frame)

	key = cv2.waitKey(1) & 0xff
	if key == 27: # ESC
		break
	elif key == ord('w'):
		tello.move_forward(30)
	elif key == ord('s'):
		tello.move_back(30)
	elif key == ord('a'):
		tello.move_left(30)
	elif key == ord('d'):
		tello.move_right(30)
	elif key == ord('e'):
		tello.rotate_clockwise(30)
	elif key == ord('q'):
		tello.rotate_counter_clockwise(30)
	elif key == ord('r'):
		tello.move_up(30)
	elif key == ord('f'):
		tello.move_down(30)

tello.land()

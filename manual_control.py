from easytello import tello
import cv2
import pynput



def on_press(key):
	try:
		if key.char == 'w':
			print('forward')
			drone.forward(25)

		elif key.char == 'a':
			print('right')
			drone.right(25)

		elif key.char == 's':
			print('back')
			drone.back(25)

		elif key.char == 'd':
			print('right')
			drone.right(25)

		elif key.char == 'q':
			print('land')
			drone.land()

		elif key.char == 't':
			print('takeoff')
			drone.takeoff()

		elif key.char == 'r':
			print('up')
			drone.up(25)

		elif key.char == 'f':
			print('down')
			drone.down(25)

		elif key.char == 'z':
			print('clockwise 90 degrees')
			drone.cw(90)
		elif key.char == 'x':
			print('counter clockwise 90 degrees')
			drone.ccw(90)

	except AttributeError:
		return


def on_release(key):
	print('{0} released'.format(
		key))
	if key == pynput.keyboard.Key.esc:
		drone.land()
		# Stop listener
		return False

def on_move(x, y):
	alpha = 0.01

	dx = x - posx
	dy = y - posy

	dx *= alpha
	dy *= alpha
	print(dx, dy)


def on_click(x, y, button, pressed):
	drone.land()
	return


def on_scroll(x, y, dx, dy):
	if dy > 0:
		print('up')
	elif dy < 0:
		drone.up(25)
		print('down')
		drone.down(25)

def main():
	# create keyboard listener
	listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
	listener.start()

	fly = True
	while fly:
		log =[drone.get_time(),
			drone.get_battery(),
			drone.get_height(),
			drone.get_acceleration(),
			drone.get_attitude(),
			drone.get_tof(),
			drone.get_baro()]
		print(log)

if __name__=='__main__':
	# initialize drone
	drone = tello.Tello()
	print(drone.tello_ip)
	print(drone.tello_port)
	#drone.takeoff()
	drone.streamon()
	main()

from djitellopy import Tello
import time
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits import mplot3d
import cv2
import numpy as np
import io
from matplotlib.animation import FuncAnimation

def data_collection(data_file='data.csv'):
	tello = Tello()
	tello.connect()
	#tello.takeoff()

	start = time.time()
	posx=[]
	posy=[]
	posz=[]
	pitch=[]
	roll=[]
	yaw=[]
	while time.time() - start < 10:
		state = tello.get_current_state()
		print(state)
		posx.append(float(state['agx']))
		posy.append(float(state['agy']))
		posz.append(float(state['agz']))
		pitch.append(float(state['pitch']))
		roll.append(float(state['roll']))
		yaw.append(float(state['yaw']))


	#tello.land()
	d = {'x': posx, 'y': posy, 'z': posz, 'pitch': pitch, 'roll': roll, 'yaw': yaw}
	df = pd.DataFrame(data=d)
	df.dropna(inplace=True)
	df.to_csv('data.csv')

def fig_to_np(fig, dpi=180):
	buf = io.BytesIO()
	fig.savefig(buf, format="png", dpi=dpi)
	buf.seek(0)
	img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
	buf.close()
	img = cv2.imdecode(img_arr, 1)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

	return img

def graph_animation():
	data = pd.read_csv('data.csv')
	# sample every 100th row
	data = data[::5000]	
	
	xmin = min(data['x']) 
	xmax = max(data['x'])
	ymin = min(data['y'])
	ymax = max(data['y'])
	zmin = min(data['z'])
	zmax = max(data['z'])
	
	for i in range(len(data)):
		fig, ax = plt.subplots(subplot_kw=dict(projection='3d'), figsize=(20,20))
		df = data.iloc[:i, :]
		ax.view_init(30, int(i/100))	
		ax.set_xlim(xmin, xmax)
		ax.set_ylim(ymin, ymax)
		ax.set_zlim(zmin, zmax)

		ax.plot(df['x'], df['y'], df['z'])
		plt.savefig('frames/frame' + str(i) + '.png')
		plt.close()

if __name__=='__main__':
	graph_animation()








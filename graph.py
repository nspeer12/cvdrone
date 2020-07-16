from djitellopy import Tello
import time
import matplotlib.pyplot as plt
import pandas as pd

tello = Tello()
tello.connect()
#tello.takeoff()

start = time.time()
history = [None]
posx=[]
posy=[]
posz=[]
i = 0
while time.time() - start < 5:
	state = tello.get_current_state()
	posx.append(float(state['agx']))
	posy.append(float(state['agy']))
	posz.append(float(state['agz']))
	#history.append(pos)
	print(state['agx'])
	i+=1

#tello.land()
d = {'x': posx, 'y': posy, 'z': posz}
df = pd.DataFrame(data=d)
df.dropna(inplace=True)

fig, axs = plt.subplots(3, figsize=(30,10))
axs[0].plot(df['x'])
axs[1].plot(df['y'])
axs[2].plot(df['z'])
plt.savefig('tello.png')

import socket
import time

tello_ip = '192.168.10.1'
tello_port = 8889
tello_network = (tello_ip, tello_port)

drone = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
drone.connect(tello_network)

drone.send('command'.encode(), 0)
print('connected')

drone.send('takeoff'.encode(), 0)
print('takeoff')


drone.send('land'.encode(), 0)
print('land')

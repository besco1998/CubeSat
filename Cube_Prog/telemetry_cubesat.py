#!/usr/bin/env python
import time
import serial
import socket
#import pygame
#import pygame.camera
# Serial Setup #
ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate = 9600,#must be configured to stm baudrate to read from serial
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
#################

# UDP Send fn #
def send(data, port=50000, addr='239.192.1.100'):
    # Create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Make the socket multicast-aware, and set TTL.
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
    # Change TTL (=20) to suit
    # Send the data
    s.sendto(data, (addr, port))
#################

while 1:
    #cmd received from serial sent to ground station via udp
        
    #cmd, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #cmd="$c,1,16,15,20,2" #for test only
    #cmd="$s,30.21,10.255,35,80,50,10,35,25.54,33,98.55,13:25:30,650" #for test only telemetry
    
    cmd=ser.readline()
    print(cmd)
    cmd_split=cmd.split(',')
    print(cmd_split)
    if cmd_split[0] == "$S":
        send(cmd,19019,'192.168.169.4')
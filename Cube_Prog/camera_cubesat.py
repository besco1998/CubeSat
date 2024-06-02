#!/usr/bin/env python
import time
import serial
import socket
import pygame
import pygame.camera
import sys
import os
from time import gmtime, strftime
from picamera import PiCamera
from time import sleep

# Camera Setup #
pygame.camera.init()
pygame.camera.list_cameras() #Camera detected or not
cam = pygame.camera.Camera("/dev/video0",(640,480))


cam = PiCamera()

#################


# UDP Initialization
UDP_IP = "0.0.0.0"
UDP_PORT = 19020
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
#################
#cam.start()

def get_image_path_uniform():
    x= strftime("%Y-%m-%d", gmtime())
    if (os.path.isdir(x)!= 1):
        os.makedirs(x)
        return str(x + "/" + strftime("%Y-%m-%d@%H#%M#%S", gmtime()))
    else:
        return str(x + "/" + strftime("%Y-%m-%d@%H#%M#%S", gmtime()))

def get_image_path_shots(yaw1,yaw2,no):
    x= strftime("%Y-%m-%d", gmtime())
    if (os.path.isdir(x)!= 1):
        os.makedirs(x)
    #format need to be changed
    return str(x + "/" + strftime("%Y-%m-%d@%H#%M#%S", gmtime()))
    #return str(x + "/" + strftime("%Y-%m-%d", gmtime())+"-"+str(yaw1)+"-"+str(yaw2)+"-"+str(no))

def capture_uniform():
    #cam.start()
    img = cam.get_image()
    pygame.image.save(img,get_image_path_uniform()+".jpg")

    cam.start_preview()
    cam.rotation = 180
    cam.capture(get_image_path_uniform()+".jpg")
    cam.stop_preview()

    #need to insert delay fn

def capture_number(yawi,yawf,num):
    cam.start_preview()
    cam.rotation = 180
    for i in range(0,int(num)):
        #cam.start()
        print(i)
        #img = cam.get_image()
        #pygame.image.save(img,get_image_path_shots(yawi,yawf,i)+".jpg")
        sleep(1)
        cam.capture(get_image_path_shots(yawi,yawf,i)+".jpg")
        #need to insert delay fn
    cam.stop_preview()

def camera_ctrl (cmd):
    if int(cmd[1])==1: #open camera
        #if int(cmd[2])>=int(cmd[3]) and int(cmd[2])<=int(cmd[4]) : # current yaw is inside the boundary
        if int(cmd[5]) == 0: # for 0 it capture photos in uniform time interval
            capture_uniform()
        else: #for any other number i capture that no of pictures
            capture_number(int(cmd[3]),int(cmd[4]),int(cmd[5]))
                

while 1:
    cmd, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #cmd="$c,1,16,15,20,5" #for test only for camera
    #cmd="$s,30.21,10.255,35,80,50,10,35,25.54,33,98.55,13:25:30,650" #for test only
    cmd_split=cmd.split(',')
    #print(cmd_split)
    if cmd_split[0] == "$c":
        camera_ctrl(cmd_split)
     
        
        







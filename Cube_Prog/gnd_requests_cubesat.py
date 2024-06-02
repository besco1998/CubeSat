# GND_CMD Client on (cube sat)
# 

#!/usr/bin/env python
import time
import socket
import sys
import os
from time import gmtime, strftime

from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove


# UDP Initialization for recieving commands
UDP_IP = ""
UDP_PORT = 19021
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
#################

current_path=os.path.dirname(os.path.abspath(__file__)) # global variable have this python file path

##### these functions for tcp sending  ######
def send_file(file):
    s = socket.socket()
    s.connect(('192.168.169.4',8001)) # Distenation ip and port
    path=os.path.join(current_path,file)
    print('Sending file: %s') %file
    s.sendall(file.encode() + b'\n')
    filesize = os.path.getsize(path)
    s.sendall(str(filesize).encode() + b'\n')
    with open(path,'rb') as f:
        s.sendall(f.read())
##############################################

#under construction
def debug_info(rw):
    path =os.path.join(current_path,'debug/') #get the current file directory
    if rw == 'r':
        f= open(strftime(path+"%Y-%m-%d", gmtime())+".txt","w+") # create or open text file
        for line in reversed(open("filename").readlines()):
            print (line.rstrip())

    for root, dirs, files in os.walk(path):
    	for file in files:
    		if(file.endswith(".jpg")): #searching for jpg files only
    			file_path=str(os.path.join(root,file))
    			newfile_path=file_path.replace(path,'') #delete the home directory leaving just image folders
    			f.write(file_path.replace(path,'')+"\n") #write to the file
    			print(newfile_path)
    f.close()
#############################################################3

# lists the files and folders in a ls.txt file
def get_dir_list():
	path =current_path #get the current file directory
	f= open("ls.txt","w+") # create or open text file
	f2=open("ls2.txt","w+")
	for root, dirs, files in os.walk(path):
		for file in files:
			if(file.endswith(".jpg")): #searching for jpg files only
				file_path=str(os.path.join(root,file))
				newfile_path=file_path.replace(path,'') #delete the home directory leaving just image folders
				x=file_path.replace(path,'')
				f.write(x+"\r\n") #write to the file
				y=x.replace("/",'\\')
				f2.write(y+"\r\n") #write to the file
				print(y)
	f.close()
	f2.close()

def get_set_last_update(rw):
	current_path=os.path.dirname(os.path.abspath(__file__)) # global variable have this python file path
	path =os.path.join(current_path,'debug/') #get the current file directory
	daily_debug= path+strftime("%Y-%m-%d", gmtime())+".txt" # path for daily debug file
	status_debug= path+"status.txt"
	if rw =="r":
		if (os.path.isfile(daily_debug) != 1): #if there is no daily debug file , create one and add the last data to it	
			l_gs_u=""
            #read reverse
			textfile = open(status_debug)
			lines = textfile.readlines()
			for line in reversed(lines):
				if (line.partition("-Last groundstation update request:")[1] == "-Last groundstation update request:"):
					l_gs_u=line.partition("-Last groundstation update request:")[2]
					break
			textfile.close()
			f= open(strftime(path+"%Y-%m-%d", gmtime())+".txt","w+") # create or open text file
			f.write("#"+strftime("%H#%M#%S", gmtime())+"#-Last groundstation update request:"+l_gs_u) # write the last data from status file
			f.close()
			return l_gs_u
    	
		else: #if the daily file exists, search it and get l gs u
			l_gs_u=""
			textfile = open(daily_debug)
			lines = textfile.readlines()
			for line in reversed(lines):
				if line.partition("-Last groundstation update request:")[1] == "-Last groundstation update request:":
					l_gs_u=line.partition("-Last groundstation update request:")[2]
					break
			textfile.close()
			return l_gs_u
	
	elif rw=="w":#update the status file
		fh, abs_path = mkstemp()
		with fdopen(fh,'w') as new_file:
			with open(status_debug) as old_file:
				for line in old_file:
					if (line.partition("-Last groundstation update request:")[1] == "-Last groundstation update request:"):
						line="-Last groundstation update request:"+strftime("%Y-%m-%d@%H#%M#%S", gmtime())+"\n"
					new_file.write(line)
		copymode(status_debug, abs_path)#copy the file permissions
		remove(status_debug)#remove original file
		move(abs_path, status_debug)#move it to its new place
		f= open(strftime(path+"%Y-%m-%d", gmtime())+".txt","a") # open daily debug file and append it
		f.write("#"+strftime("%H#%M#%S", gmtime())+"#-Last groundstation update request:"+strftime("%Y-%m-%d@%H#%M#%S", gmtime())+"\n") # write the last data from status file
		f.close()
		return "#"+strftime("%H#%M#%S", gmtime())+"#-Last groundstation update request:"+strftime("%Y-%m-%d@%H#%M#%S", gmtime())

def send_string(sock,string):
    sock.sendall(string.encode() + b'\n')

def send_int(sock,integer):
    sock.sendall(str(integer).encode() + b'\n')

def transmit(sock,file_path,file_name):
    path = file_path
    filesize = os.path.getsize(path)
    print('Sending file:'+ str(file_name) +'('+ str(filesize) +' bytes)')
    send_string(sock,str(file_name))
    send_int(sock,filesize)
    with open(path,'rb') as f:
        sock.sendall(f.read())

def get_update_list():
	current_path=os.path.dirname(os.path.abspath(__file__)) # global variable have this python file path
	path =os.path.join(current_path,'debug/') #get the current file directory
	status_debug= path+"status.txt"
	l_gs_u = get_set_last_update("r")
	l_u_stamp = time.strptime(l_gs_u, "%Y-%m-%d@%H#%M#%S\n")
	l_u_date = time.strptime(l_gs_u.split("@")[0], "%Y-%m-%d")
    #compare it with the text file
	textfile = open(current_path+"/ls.txt")
	lines = textfile.readlines()
	dir_list=[]
	for line in lines:
		if time.strptime(line.split("/")[1], "%Y-%m-%d") >= l_u_date :
			if time.strptime(line.split("/")[2], "%Y-%m-%d@%H#%M#%S.jpg\n") >= l_u_stamp :
				dir_list.append(str(line.split("\r\n")[0])) #add the path to the buffer to send this files
	return dir_list


def send_last_update():
	update_list=get_update_list()
	s = socket.socket()
	s.connect(('192.168.169.4',8001))
	for i in range(len(update_list)):
		transmit(s,os.path.dirname(os.path.abspath(__file__))+update_list[i],update_list[i])

while 1:
	cmd, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #cmd="$u" #for test only # 0/1 for list of directories transfere,# 0/1 to download last update,#0  or file name to be downloaded
    #cmd="$s,30.21,10.255,35,80,50,10,35,25.54,33,98.55,13:25:30,650" #for test only
	#cmd=b'$u'
	print(cmd)
	if cmd == b'$l':
		get_dir_list()# this will wright a ls.txt file of all the directories have .jpg files
		send_file("ls2.txt")
	elif cmd == b'$u':
		send_last_update()
		get_set_last_update("w")
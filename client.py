#!/usr/lib/python
import sys
import pygame
from pygame.locals import *
import threading
from socket import *
HOST,PORT="localhost",8080
def listen(sock,others):
    while 1:
        data=sock.recv(1024)
        print data             
        l=data.split(",")
        for i in l:
            if i=="":
                continue
            t=i.split("@")
            others[t[0]]=tuple([int(i) for i in t[1].split(":")])

pygame.init()
s=socket(AF_INET, SOCK_STREAM)
s.connect((HOST,PORT))
sc=pygame.display.set_mode((600,600))
self=pygame.image.load("c1/c1.png")
self_location=[0,0]
other=pygame.image.load("c2/c2.png")
others={}
listen_thread=threading.Thread(target=listen,args=(s,others))
listen_thread.start()
while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
           s.close()
           sys.exit(1)
        elif event.type == KEYDOWN:
            if event.key == K_DOWN:
                self_location[1]+=100
            if event.key == K_UP:
                self_location[1]-=100
            if event.key == K_LEFT:
                self_location[0]-=100
            if event.key == K_RIGHT:
                self_location[0]+=100
            s.send("127.0.0.1"+"@"+":".join([str(i) for i in self_location]))
            
    sc.fill((255,255,255))
    sc.blit(self,tuple(self_location))
    print others
    for k,v in others.items():
        sc.blit(other,v)
    pygame.display.update()


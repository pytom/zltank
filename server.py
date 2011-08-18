#!/usr/bin/python
from socket import *
import threading
HOST,PORT="localhost",8080
connl=[]
def cthread_do(add,conn,status=[0,0]):   
   global connl
   citem=[add,[conn,status]]
   print threading.currentThread().getName() 
   print connl,citem
   data=""
   for d in connl:
       t=d[0]+"@"+":".join([str(i) for i in d[1][1]])+","
       data+=t
   if data != "": 
       conn.send(data)       
   for other in connl: 
       sdata=add+"@"+":".join([str(i) for i in status])          
       other[1][0].send(sdata)             
   connl.append(citem)    
   while 1:
       rdata=conn.recv(1024)
       t=rdata.split("@")
       newstatus=[int(i) for i in t[1].split(":")]
       for i in connl:
           if i[0]==add:
               i[1][1]=newstatus
               break 
       for other in connl:
          if other[1][0].fileno()==conn.fileno():
              continue         
          other[1][0].send(rdata)
                    
def main():
    server=socket(AF_INET,SOCK_STREAM)
    server.bind((HOST,PORT))
    while 1:
        server.listen(5)
        conn, add=server.accept()
        print "connected",add
        c=threading.Thread(target=cthread_do,args=(add[0],conn))
        c.start()

main()

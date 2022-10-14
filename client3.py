from http import server
import socket
import threading
import tkinter
from tkinter import *
from turtle import down, onclick
global port


# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Listening to Server and Sending Nickname


#initializing object 
top= tkinter.Tk(className='Instant LAN messenger client')
top.geometry("400x300")

#display port number and ip 
L1 = Label(top, text="Enter IP and Port:")
L1.place(x=0,y=0)

#def of click
def myclick():
    receive_thread = threading.Thread(target=receive)

    str= E1.get()
    print(str)
    index1=str.find(":")
    ip_address=str[0:index1]
    print("ip address is:",ip_address)
    #ip_address=re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",str)
    #print(ip_address)
    index=str.find(":")
    port=int(str[index+1:])
    if((client.connect(('127.0.0.2', port))== None)):
        var.set('Connected')
    #port=re.match(":(?P<port>[0-9]+)",str2)
    print("port number is:",port)
    receive_thread.start()
    
#display button start listening
B = tkinter.Button(top, text ="Connection",command=myclick,width=20,height=1,bg="light blue")
B.place(x=200,y=15)

#display entry box on top
E1 = Entry(top, bd =5,width=30)
E1.place(x=0,y=20)

#display text box for connection
msg1 = Text(top,height=1,width="23")
var = StringVar()
label = Label( msg1, textvariable=var, relief=RAISED,height=1,width="23" )
var.set("not connected")
label.pack()
msg1.config(state=DISABLED)
msg1.place(x=2, y=50)
msg1.tag_add("here", "1.0", "1.4")
msg1.tag_add("start", "1.8", "1.13")
msg1.tag_config("here", background="yellow", foreground="blue")
msg1.tag_config("start", background="black", foreground="green")

#display text box for reply
msg1 = Text(top,height=5,width="43",bg='light grey')
msg1.config(state=DISABLED)
msg1.place(x=0, y=80)
msg1.tag_add("here", "1.0", "1.4")
msg1.tag_add("start", "1.8", "1.13")
msg1.tag_config("here", background="yellow", foreground="blue")
msg1.tag_config("start", background="black", foreground="green")

#display text box 
msg = Text(top,height=5,width="43")
msg.insert(INSERT, "")
msg.insert(END, "")
msg.place(x=0, y=160)
msg.tag_add("here", "1.0", "1.4")
msg.tag_add("start", "1.8", "1.13")
msg.tag_config("here", background="yellow", foreground="blue")
msg.tag_config("start", background="black", foreground="green")

def send():
    write_thread = threading.Thread(target=write)

    #str1=E1.get(0,9);
    #print(str1)
    data = msg.get("0.0", END)
    msg1.config(state=NORMAL)
    msg1.insert(END, data)
    msg1.config(state=DISABLED)
    client.send(data.encode('ascii'))
    write_thread.start()

#display send button
B1=tkinter.Button(top, text="SEND",command=send,width=20,height=1,bg="light blue")
B1.place(x=200,y=250)




def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'Misbah':
                client.send(nickname.encode('ascii'))
            else:
                msg1.config(state=NORMAL)
                msg1.insert(END, message)
                msg1.config(state=DISABLED)
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break


# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        server.send(message.encode('ascii'))
        
# Starting Threads For Listening And Writing



top.mainloop()
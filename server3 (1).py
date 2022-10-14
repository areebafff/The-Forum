import socket
import threading
import tkinter
from tkinter import *
from turtle import down, onclick
host = '127.0.0.2'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#port = 5545
global port
#client = None

#initializing object 
top= tkinter.Tk(className='Instant LAN messenger server')
top.geometry("450x250")

#display port number text
L1 = Label(top, text="Port Number:")
L1.place(x=0,y=0)

#def of click
def myclick():
    thread1 = threading.Thread(target=rec, args=())
    port= int(E1.get())
    print(port)
    
    server.bind((host, port))
    server.listen()
    #threading.Thread(target=lambda: self._thread_function(arg1, arg2=arg2, arg3=arg3)).start()

    
    thread1.start()

#def of send
def send():
    global msg
    global client
    data = msg.get("0.0", END)
    msg1.config(state=NORMAL)
    msg1.insert(END, data)
    msg1.config(state=DISABLED)
    client.send(data.encode('ascii'))
    
    
#display button start listening
B = tkinter.Button(top, text ="Start listening",command=myclick,width=20,height=1,bg="light blue")
B.place(x=300,y=0)

#display entry box on top
E1 = Entry(top, bd =5)
E1.place(x=100,y=0)



#display text box for reply
msg1 = Text(top,height=5,width="55")
msg1.config(state=DISABLED)
msg1.place(x=0, y=30)
msg1.tag_add("here", "1.0", "1.4")
msg1.tag_add("start", "1.8", "1.13")
msg1.tag_config("here", background="yellow", foreground="blue")
msg1.tag_config("start", background="black", foreground="green")

#display text box 
msg = Text(top,height=5,width="55")
msg.insert(INSERT, "")
msg.insert(END, "")
msg.place(x=0, y=100)
msg.tag_add("here", "1.0", "1.4")
msg.tag_add("start", "1.8", "1.13")
msg.tag_config("here", background="yellow", foreground="blue")
msg.tag_config("start", background="black", foreground="green")


#display send button
B1=tkinter.Button(top, text="SEND",command=send,width=20,height=1,bg="light blue")
B1.place(x=300,y=200)

# Starting Server


# Lists For Clients and Their Nicknames
clients = []
nicknames = []
# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)
        

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            msg1.config(state=NORMAL)
            msg1.insert(END, message)
            msg1.config(state=DISABLED)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


# Receiving / Listening Function
def rec():
    #global server
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('Misbah'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
    return

top.mainloop()

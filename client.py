import socket
import sys
import threading
import tkinter

def logmessage(msg):
    print(f"[LOG] {msg}")

HOST = "127.0.0.1"
PORT = 65456

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)



def listen():
    while True:
        msg = server.recv(1024).decode()
        text_box.insert(tkinter.END, msg)
        logmessage("Message recieved: "+msg)

def sendMessage(event=None):
    msg = input_text.get()
    if len(msg) == 0:
        logmessage("Attempt of sending an empty message.")
        return
    input_text.set("")
    server.sendall( msg.encode() )
    text_box.insert(tkinter.END, f"<me> {msg}")
    logmessage("Message "+msg+" has been sent.")

def setupMessages():
    text_box.insert( tkinter.END, "Welcome to the chat!")
    text_box.insert( tkinter.END, "Here are available commands:")
    text_box.insert( tkinter.END, "/chnick <newnick>")




# GUI related 
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 350
window = tkinter.Tk()
window.geometry('350x500')
window.title("Simple messages")

input_text = tkinter.StringVar()
# input_text.set("Your message...")

chat_title = tkinter.Label(
    window,
    text="Chat messages",
    font="60"
)

scrollbar = tkinter.Scrollbar(
    window
)

text_box = tkinter.Listbox( 
    window,
    yscrollcommand=scrollbar.set,
    height="25",
    width="50"
)

send_button = tkinter.Button( 
    window, 
    text="Send",
    command=sendMessage
)

text_field = tkinter.Entry( 
    window,
    textvariable=input_text,
    width="40",
)
text_field.bind("<Return>", sendMessage)

chat_title.pack( side=tkinter.TOP, anchor="center" )
text_box.pack( side=tkinter.TOP, anchor="center")
send_button.place( x=300, y=450)
text_field.place( x=20, y=450 )

setupMessages()


# connecting to the server
logmessage(f"Connecting to {HOST} {PORT}")
server.connect( (HOST, PORT) )
logmessage(f"Connection established.")

# background message recieving thread
background = threading.Thread(target=listen)
background.daemon = True
background.start()


window.mainloop()

server.close()

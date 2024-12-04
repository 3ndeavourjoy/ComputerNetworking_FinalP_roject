from tkinter import *
from socket import *
import threading
from tkinter import scrolledtext
from tkinter import messagebox
from client import ChatClient


clients = []
nameX = []
cname = ""

def GUI():
    global chatlog, textbox, gui, cnamebox, hostbox, portbox

    gui = Tk()
    gui.title("Server")
    gui.geometry("400x750")
    gui.configure(bg="#2c3e50")


    FONT = ("Helvetica", 12)
    USER_COLOR = "#1abc9c"
    BOT_COLOR = "#3498db"
    TEXT_COLOR = "#ecf0f1"

    header = Label(
        gui,
        text="Welcome to Chat",
        bg="#34495e",
        fg=TEXT_COLOR,
        font=("Helvetica", 14, "bold"),
        pady=10
    )
    header.place(relx=0, rely=0, relwidth=1, height=40)
    
    control_frame = Frame(gui, bg="#2c3e50")
    control_frame.place(relx=0, rely=0.07, relwidth=1, height=80)

    
    Button(
        control_frame,
        text="Start Server",
        font=FONT,
        bg=USER_COLOR,
        fg=TEXT_COLOR,
        command=start_server
    ).place(relx=0.1, rely=0.1, relwidth=0.35, height=30)

    Button(
        control_frame,
        text="Stop Server",
        font=FONT,
        bg="#e74c3c",
        fg=TEXT_COLOR,
        command=stop_server
    ).place(relx=0.55, rely=0.1, relwidth=0.35, height=30)
    


    chatlog = scrolledtext.ScrolledText(
        gui,
        wrap=WORD,
        state="disabled",
        bg="#34495e",
        fg=TEXT_COLOR,
        font=FONT,
        padx=10,
        pady=10,
    )
    chatlog.tag_configure("user_message", foreground=USER_COLOR)
    chatlog.tag_configure("bot_message", foreground=BOT_COLOR)
    chatlog.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.7)

 
    input_frame = Frame(gui, bg="#2c3e50")
    input_frame.place(relx=0, rely=0.8, relwidth=1, height=350)


    textbox = Text(
        input_frame,
        font=FONT,
        bg="#ecf0f1",
        fg="#2c3e50",
        bd=0,
        relief="solid",
        highlightbackground="#2c3e50",
        highlightthickness=1,
    )
    textbox.place(relx=0.05, rely=0.03, relwidth=0.7, relheight=0.09)

    send_button = Button(
        input_frame,
        text="Send",
        font=FONT,
        bg=USER_COLOR,
        fg=TEXT_COLOR,
        bd=0,
        activebackground="#16a085",
        activeforeground=TEXT_COLOR,
        relief="flat",
        command=send ,
    )
    send_button.place(relx=0.8, rely=0.03, relwidth=0.15, relheight=0.09)
    
    
    hostname = Label(
        input_frame,
        text="Host :",
        bg="#34495e",
        fg=TEXT_COLOR,
        font=("Helvetica", 12, "bold"),
        pady=10
    )
    hostname.place(relx=0.05, rely=0.165, relwidth=0.15, relheight=0.09)
    
    
    hostbox = Text(
        input_frame,
        font=FONT,
        bg="#ecf0f1",
        fg="#2c3e50",
        bd=0,
        relief="solid",
        highlightbackground="#2c3e50",
        highlightthickness=1,
    )
    hostbox.place(relx=0.20, rely=0.165, relwidth=0.4, relheight=0.09)
    
    
    portname = Label(
        input_frame,
        text="Port :",
        bg="#34495e",
        fg=TEXT_COLOR,
        font=("Helvetica", 12, "bold"),
        pady=10
    )
    portname.place(relx=.65, rely=0.165, relwidth=0.15, relheight=0.09)
    
    
    portbox = Text(
        input_frame,
        font=FONT,
        bg="#ecf0f1",
        fg="#2c3e50",
        bd=0,
        relief="solid",
        highlightbackground="#2c3e50",
        highlightthickness=1,
    )
    portbox.place(relx=0.80, rely=0.165, relwidth=0.15, relheight=0.09)
    
    
    cname = Label(
        input_frame,
        text="Name :",
        bg="#34495e",
        fg=TEXT_COLOR,
        font=("Helvetica", 12, "bold"),
        pady=10
    )
    cname.place(relx=0.05, rely=0.3, relwidth=0.15, relheight=0.09)
    
    cnamebox = Text(
        input_frame,
        font=FONT,
        bg="#ecf0f1",
        fg="#2c3e50",
        bd=0,
        relief="solid",
        highlightbackground="#2c3e50",
        highlightthickness=1,
    )
    cnamebox.place(relx=0.20, rely=0.3, relwidth=0.46, relheight=0.09)
    
    
    clientbutton = Button(
        input_frame,
        text="Add Client",
        font=FONT,        bg=USER_COLOR,
        fg=TEXT_COLOR,
        bd=0,
        activebackground="#16a085",
        activeforeground=TEXT_COLOR,
        relief="flat",
        command=getClient,
    )
    clientbutton.place(relx=0.7, rely=0.3, relwidth=0.25, relheight=0.09)

    textbox.focus()
    
    gui.mainloop()
    
    
def getClient():
    global cnamebox, portbox, hostbox
    cname = cnamebox.get("1.0", END).strip()
    port = portbox.get("1.0", END).strip()
    host = hostbox.get("1.0", END).strip()
    
    if "127.0.0.1" in host and "5678" in port and  len(cname) > 1 and str(cname) not in nameX:
        nameX.append(cname)
        Toplevel(ChatClient(cname))
    

def broadcast(message, sender_conn=None):
    """Send a message to all connected clients."""
    global chatlog
    for client in clients:
        conn, _, _ = client
        # print(client[2])
        
        if conn != sender_conn: 
            try:
                first_word = message.split()[0]
                second_word = message.split()[1]
   
                if "All" in first_word:
                    result = " ".join(message.split()[2:])
                    msg = f"{second_word} : {result}"
                    conn.send(msg.encode('ascii'))
                    
                elif first_word in client[2] and second_word in client[2]:
                    result = " ".join(message.split()[2:])
                    msg = f"{second_word} : {result}"
                    conn.send(msg.encode('ascii'))
                    
                elif first_word in client[2]:
                    result = " ".join(message.split()[2:])
                    msg = f"{second_word} : {result}"
                    conn.send(msg.encode('ascii'))
                    
                    
                elif "list" in first_word:
                    conn.send(message.encode('ascii'))
                else:
                   pass
                    
            except:
                conn.close()
                clients.remove(client)
 
 
    first_wordx = message.split()[0]
    second_wordx = message.split()[1]

    if "list ::" not in str(message) and first_wordx not in second_wordx: 
        resultx = " ".join(message.split()[2:])   
        msgx = f"{second_wordx} : {resultx}"    
    # if "list ::" not in str(message):    
        chatlog.config(state=NORMAL)
        chatlog.insert(END, f"{message}\n")
        chatlog.config(state=DISABLED)
        chatlog.yview(END)
        

def handle_client(conn, addr, name):
    # print(f"New connection from {addr}")
    global cname
    cname = cnamebox.get("1.0", END).strip()
    clients.append((conn, addr, cname))
    broadcast(f"list :: {nameX}")

    while True:
        try:
            message = conn.recv(1024).decode('ascii')
            if not message:
                break
            # print(f"Message from {addr}: {message}")
            # broadcast(f"Client {addr}: {message}", conn)
            broadcast(f"{message}", conn)
        except:
            break

    # print(f"Connection closed from {addr}")
    conn.close()
    clients.remove((conn, addr, cname))

def initialize_server():
    try:
        global cnamebox
        server = socket(AF_INET, SOCK_STREAM)
        host = "127.0.0.1"
        port = 5678
        server.bind((host, port))
        server.listen(5)

        # print(f"Server listening on {host}:{port}")
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr, cname), daemon=True).start()
    
    except OSError as e:
        if e.errno == 10048:
            messagebox.showwarning("Warning", f"Error: Address {host}:{port} is already in use.\n")
        else:
            messagebox.showwarning("Warning", f"Unexpected error: {e}\n")
    except ValueError:
        messagebox.showwarning("Warning", "Error: Port must be a valid integer.\n")
    except Exception as e:
        messagebox.showwarning("Warning", f"Unexpected error: {e}\n")

def start_server():
    initialize_server()

def stop_server():

    try:
            gui.destroy()
            GU()
    except Exception as e:
        messagebox.showwarning("Warning", f"Error stopping server: {e}\n")


def send():
    
    global textbox
    message = textbox.get("1.0", END).strip()
    if message:  
        broadcast(f"Server: {message}")
    textbox.delete("1.0", END)

if __name__ == "__main__":
    chatlog = textbox = None

    
    threading.Thread(target=initialize_server, daemon=True).start()
    GUI()

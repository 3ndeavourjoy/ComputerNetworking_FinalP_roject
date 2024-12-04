from tkinter import *
from tkinter import scrolledtext
from socket import *
import threading
import queue
from tkinter import ttk


class ChatClient:
    
    def __init__(self,name):
        self.s = self.initialize_client()
        self.msg_queue = queue.Queue()
        self.namelist = []
        self.name = name

        self.gui = Tk()
        self.gui.title("Client")
        self.gui.geometry("400x600")
        self.gui.configure(bg="#2c3e50")


        FONT = ("Helvetica", 12)
        USER_COLOR = "#1abc9c"
        BOT_COLOR = "#3498db"
        TEXT_COLOR = "#ecf0f1"


        self.header = Label(
            self.gui,
            text=f"Welcome to Chat : {name}",
            bg="#34495e",
            fg=TEXT_COLOR,
            font=("Helvetica", 14, "bold"),
            pady=10
        )
        self.header.place(relx=0, rely=0, relwidth=1, height=40)


        self.chatlog = scrolledtext.ScrolledText(
            self.gui,
            wrap=WORD,
            state="disabled",
            bg="#34495e",
            fg=TEXT_COLOR,
            font=FONT,
            padx=10,
            pady=10,
        )
        self.chatlog.tag_configure("user_message", foreground=USER_COLOR)
        self.chatlog.tag_configure("bot_message", foreground=BOT_COLOR)
        self.chatlog.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.7)


        self.input_frame = Frame(self.gui, bg="#2c3e50")
        self.input_frame.place(relx=0, rely=0.85, relwidth=1, height=60)
        
        self.combobox = ttk.Combobox(
            self.input_frame,
            values=self.namelist,
            font=FONT,
            state="readonly" 
        )
        self.combobox.place(relx=0.05, rely=0.3, relwidth=0.2, relheight=0.6)
        self.combobox.set("All")
        

   
        self.textbox = Text(
            self.input_frame,
            font=FONT,
            bg="#ecf0f1",
            fg="#2c3e50",
            bd=0,
            relief="solid",
            highlightbackground="#2c3e50",
            highlightthickness=1,
        )
        self.textbox.place(relx=0.3, rely=0.3, relwidth=0.45, relheight=0.6)

  
        self.send_button = Button(
            self.input_frame,
            text="Send",
            font=FONT,
            bg=USER_COLOR,
            fg=TEXT_COLOR,
            bd=0,
            activebackground="#16a085",
            activeforeground=TEXT_COLOR,
            relief="flat",
            command=self.send ,
        )
        self.send_button.place(relx=0.8, rely=0.3, relwidth=0.15, relheight=0.6)

   
        self.textbox.focus()


        threading.Thread(target=self.receive, daemon=True).start()

        self.gui.after(100, self.process_messages)

        self.gui.mainloop()


    def initialize_client(self):
        
        s = socket(AF_INET, SOCK_STREAM)
        host = '127.0.0.1'
        port = 5678

        try:
            s.connect((host, port))
            print("Connected to the server.")
        except Exception as e:
            print(f"Error connecting to the server: {e}")
            exit(1)

        return s


    def send(self):
        
        msg = self.textbox.get("1.0", END).strip()
        if msg:  # Avoid sending empty messages
            self.update_chat(f"YOU: {msg}\n", 0)
            try:
                msg1 = f"{self.combobox.get()} {self.name} {msg}"
                self.s.send(msg1.encode('ascii'))
                self.textbox.delete("1.0", END)
            except Exception as e:
                print(f"Error sending message: {e}")
        

    def receive(self):
        while True:
            try:
                data = self.s.recv(1024)
                if data:
                    msg = data.decode('ascii')
                    if "list ::" not in str(msg):
                        self.msg_queue.put(msg)
                    else:
                        self.namelist.clear()
                        x = 'All'
                        inside_brackets = msg.split("[")[1].split("]")[0]
                        self.namelist = [name.strip(" '") for name in inside_brackets.split(",")]
                        self.namelist.append(x)
                        self.combobox.config(values=self.namelist)
                        
            except Exception as e:
                print(f"Error receiving message: {e}")
                break


    def process_messages(self):
        while not self.msg_queue.empty():
            msg = self.msg_queue.get()
            self.update_chat(f"{msg}\n", 1)
        self.gui.after(100, self.process_messages)


    def update_chat(self, msg, state):
        self.chatlog.config(state=NORMAL)
        self.chatlog.insert(END, msg)
        self.chatlog.config(state=DISABLED)
        self.chatlog.yview(END)


if __name__ == "__main__":
    ChatClient()

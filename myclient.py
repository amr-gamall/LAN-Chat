import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = ""
        self.running = True

    def handle_sending(self):
        msg = self.msg_var.get()
        if msg:
            self.msg_var.set('')
            if msg == "exit":
                self.client.close()
                self.running = False
                self.window.quit()
                return
            self.client.sendall(f'{self.name}: {msg}'.encode())

    def handle_reading(self):
        while self.running:
            try:
                msg_in = self.client.recv(1024)
                if msg_in:
                    msg_in = msg_in.decode('utf-8')
                    self.chat_box.config(state=tk.NORMAL)
                    self.chat_box.insert(tk.END, msg_in + '\n')
                    self.chat_box.config(state=tk.DISABLED)
                    self.chat_box.yview(tk.END)
            except OSError:
                break

    def start_client(self):
        try:
            self.client.connect(('localhost', 42))
        except ConnectionRefusedError:
            messagebox.showerror("Connection Error", "Unable to connect to server")
            return

        self.name = simpledialog.askstring("Nickname", "Please choose a nickname", parent=self.window)
        if not self.name:
            self.running = False
            self.window.quit()
            return

        send_th = threading.Thread(target=self.handle_reading)
        send_th.start()

    def run_gui(self):
        self.window = tk.Tk()
        self.window.title("Chat Client")

        self.chat_box = scrolledtext.ScrolledText(self.window)
        self.chat_box.pack(padx=20, pady=5)
        self.chat_box.config(state=tk.DISABLED)

        self.msg_var = tk.StringVar()
        self.msg_entry = tk.Entry(self.window, textvariable=self.msg_var)
        self.msg_entry.pack(padx=20, pady=5)
        self.msg_entry.bind("<Return>", lambda event: self.handle_sending())

        self.send_button = tk.Button(self.window, text="Send", command=self.handle_sending)
        self.send_button.pack(padx=20, pady=5)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.start_client()
        
        self.window.mainloop()

    def on_closing(self):
        self.running = False
        self.client.close()
        self.window.quit()

if __name__ == '__main__':
    client = Client()
    client.run_gui()

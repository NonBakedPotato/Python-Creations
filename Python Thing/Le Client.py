import socket
import threading
import tkinter as tk
from tkinter import messagebox

# Client settings
HOST = '192.168.209.242' #Change this to the Local IP host
PORT = 12345  # Ensure this matches the server's port

def receive_messages(client_socket, text_area):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                text_area.config(state=tk.NORMAL)
                text_area.insert(tk.END, f"Other: {message}\n")
                text_area.config(state=tk.DISABLED)
                text_area.yview(tk.END)
        except:
            messagebox.showerror("An error occurred!", "The Thingy broke and it's your fault >:(")
            client_socket.close()
            break



def send_message(client_socket, entry_field, text_area):
    message = f"{username}: "
    message += entry_field.get()
    client_socket.send(message.encode('utf-8'))
    entry_field.delete(0, tk.END)
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, f"{message}\n")
    text_area.config(state=tk.DISABLED)
    text_area.yview(tk.END)

def main_interface(client_socket, root):
    login_frame.destroy()
    
    frame = tk.Frame(root)
    scrollbar = tk.Scrollbar(frame)
    text_area = tk.Text(frame, height=20, width=50, yscrollcommand=scrollbar.set, state=tk.DISABLED, wrap=tk.WORD)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar.config(command=text_area.yview)
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    frame.pack()

    entry_field = tk.Entry(root, width=50)
    entry_field.pack()
    entry_field.bind("<Return>", lambda event: send_message(client_socket, entry_field, text_area))

    send_button = tk.Button(root, text="Send", command=lambda: send_message(client_socket, entry_field, text_area))
    send_button.pack()

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, text_area))
    receive_thread.start()

def limit_size(*args):
    value = name_entry.get()
    if len(value) > max_length:
        name_var.set(value[:max_length])

def Login_Screen(root):
    global login_frame, name_entry, max_length, name_var
    
    login_frame = tk.Frame(root)
    label = tk.Label(login_frame, text="Welcome Screen")
    label.pack(pady=15)

    max_length = 12
    name_var = tk.StringVar()
    name_var.trace("w", limit_size)

    name_entry = tk.Entry(login_frame, textvariable=name_var, width=25)
    name_entry.pack(pady=5)


    connect_button = tk.Button(login_frame, text="Connect", bg='green', command=lambda: server_connection(name_var))
    connect_button.pack(pady=5)

    login_frame.pack(expand=True)

def server_connection(name_var):
    global username
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    username = name_var.get()
    print("name entered:", username)
    main_interface(client_socket, root)

def main():
    global root
    root = tk.Tk()
    root.title("Software Dev Room")
    Login_Screen(root)
    root.mainloop()

if __name__ == "__main__":
    main()


import socket
import threading
import tkinter as tk

# Client settings
HOST = '192.168.209.242'  # Change this to the server's IP address if needed
PORT = 12345  # Ensure this matches the server's port

def receive_messages(client_socket, text_area):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                text_area.config(state=tk.NORMAL)
                text_area.insert(tk.END, message + "\n")
                text_area.config(state=tk.DISABLED)
                text_area.yview(tk.END)
        except:
            print("An error occurred!")
            client_socket.close()
            break

def send_message(client_socket, entry_field, text_area):
    message = entry_field.get()
    client_socket.send(message.encode('utf-8'))
    entry_field.delete(0, tk.END)
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, f"You: {message}\n")
    text_area.config(state=tk.DISABLED)
    text_area.yview(tk.END)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    root = tk.Tk()
    root.title("Software Dev Room")

    frame = tk.Frame(root)
    scrollbar = tk.Scrollbar(frame)
    text_area = tk.Text(frame, height=20, width=50, yscrollcommand=scrollbar.set, state=tk.DISABLED)
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

    root.mainloop()

if __name__ == "__main__":
    main()


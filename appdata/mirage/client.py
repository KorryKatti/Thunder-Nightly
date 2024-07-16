import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import requests
import json
import os
import random

# Load user info from JSON file
with open('../userdata/userinfo.json', 'r') as file:
    user_info = json.load(file)

username = user_info['username']
email = user_info['email']

# Set base URL for server
with open('../userdata/settings.json', 'r') as f:
    settings = json.load(f)
    server_url = settings['server']

current_room = None
last_message_id = -1

# Create messages directory if it doesn't exist
os.makedirs('messages', exist_ok=True)

# Function to save a message to a room file
def save_message_to_file(room_name, message):
    with open(f'messages/{room_name}.txt', 'a') as file:
        file.write(f'{message}\n')

# Function to generate a color based on the username
def generate_user_color(username):
    random.seed(username)
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def send_chat_message():
    global current_room
    message = chat_message_entry.get()
    if current_room and message:
        response = requests.post(f'{server_url}/send_message', json={
            'username': username,
            'room_name': current_room,
            'message': message
        })
        if response.status_code == 200:
            chat_message_entry.delete(0, tk.END)
        else:
            print(f"Error sending message: {response.json().get('message', 'Unknown error')}")
    elif message:
        print("Select a room first.")

# Function to load rooms from server
def load_rooms():
    for widget in rooms_canvas_frame.winfo_children():
        widget.destroy()
    response = requests.get(f'{server_url}/get_rooms')
    if response.status_code == 200:
        rooms = response.json()
        for room in rooms:
            room_button = tk.Button(rooms_canvas_frame, text=room, command=lambda r=room: select_room(r), bg='#444', fg='white', relief='flat', bd=0)
            room_button.pack(fill=tk.X, pady=2, padx=5)

# Function to select a room
def select_room(room_name):
    global current_room, last_message_id
    current_room = room_name
    last_message_id = -1
    room_label.config(text=f'Current Room: {room_name}')
    response = requests.post(f'{server_url}/join_room', json={
        'username': username,
        'room_name': room_name
    })
    if response.status_code == 200:
        load_users_in_room(room_name)
        load_chat_history(room_name)
        check_for_new_messages()
    else:
        print(f"Error joining room: {response.json().get('message', 'Unknown error')}")

# Function to leave a room
def leave_room():
    global current_room, last_message_id
    if current_room:
        response = requests.post(f'{server_url}/leave_room', json={
            'username': username,
            'room_name': current_room
        })
        if response.status_code == 200:
            current_room = None
            last_message_id = -1
            room_label.config(text="Select a room or talk to yourself")
            chat_text.config(state=tk.NORMAL)
            chat_text.delete(1.0, tk.END)
            chat_text.config(state=tk.DISABLED)
            user_list.delete(0, tk.END)
        else:
            print(f"Error leaving room: {response.json().get('message', 'Unknown error')}")

# Function to load users in a room
def load_users_in_room(room_name):
    response = requests.get(f'{server_url}/get_users_in_room', params={'room_name': room_name})
    if response.status_code == 200:
        users = response.json()
        user_list.delete(0, tk.END)
        for user in users:
            user_button = tk.Button(user_list, text=user, bg='#222', fg='white', relief='flat', bd=0,
                                    command=lambda u=user: show_user_info_popup(u))
            user_button.pack(fill=tk.X, padx=5, pady=2)

# Function to show user information popup
def show_user_info_popup(username):
    popup = tk.Toplevel()
    popup.title(f"User Info: {username}")
    popup.geometry("300x150")
    popup.configure(bg='#2a2a2a')

    # Display username
    username_label = tk.Label(popup, text=f"Username: {username}", bg='#2a2a2a', fg='white', font=('Arial', 12))
    username_label.pack(pady=10)

    # Display random quote
    quotes = [
        "1 is not equal to 1",
        "The future belongs to those who believe in the beauty of their dreams.",
        "In the middle of difficulty lies opportunity.",
        "It does not matter how slowly you go as long as you do not stop."
    ]
    random_quote = random.choice(quotes)
    quote_label = tk.Label(popup, text=random_quote, bg='#2a2a2a', fg='white', font=('Arial', 10))
    quote_label.pack(pady=5)

# Function to load chat history from a room file
def load_chat_history(room_name):
    chat_text.config(state=tk.NORMAL)
    chat_text.delete(1.0, tk.END)
    try:
        with open(f'messages/{room_name}.txt', 'r') as file:
            chat_history = file.read()
            chat_text.insert(tk.END, chat_history)
    except FileNotFoundError:
        pass
    chat_text.config(state=tk.DISABLED)

# Function to check for new messages
def check_for_new_messages():
    global last_message_id
    if current_room:
        response = requests.get(f'{server_url}/get_new_messages', params={
            'room_name': current_room,
            'last_message_id': last_message_id
        })
        if response.status_code == 200:
            new_messages = response.json()
            if new_messages:
                chat_text.config(state=tk.NORMAL)
                for msg in new_messages:
                    formatted_message = f"{msg['username']}: {msg['message']}"
                    save_message_to_file(current_room, formatted_message)
                    user_color = generate_user_color(msg['username'])
                    chat_text.insert(tk.END, f'{formatted_message}\n', ('username',))
                    chat_text.tag_config('username', foreground=user_color)
                    last_message_id = msg['id']
                chat_text.config(state=tk.DISABLED)
                chat_text.see(tk.END)
        root.after(1700, check_for_new_messages)

# Function to periodically refresh the user list
def refresh_user_list():
    if current_room:
        load_users_in_room(current_room)
    root.after(2000, refresh_user_list)

# Function to create a new room
def create_new_room():
    new_room_name = simpledialog.askstring("Create New Room", "Enter the name for the new room:")
    if new_room_name:
        response = requests.post(f'{server_url}/create_room', json={
            'username': username,
            'room_name': new_room_name
        })
        if response.status_code == 200:
            room_button = tk.Button(rooms_canvas_frame, text=new_room_name, command=lambda r=new_room_name: select_room(r), bg='#444', fg='white', relief='flat', bd=0)
            room_button.pack(fill=tk.X, pady=2, padx=5)
            load_rooms()
        else:
            print(f"Error creating room '{new_room_name}': {response.json().get('message', 'Unknown error')}")
            load_rooms()

# Initialize main Tkinter window
root = tk.Tk()
root.title("Chat App")
root.geometry("800x600")
root.configure(bg='#2a2a2a')

# Main container frame
main_frame = tk.Frame(root, bg='#2a2a2a')
main_frame.pack(fill=tk.BOTH, expand=True)

# Left frame (chat area)
left_frame = tk.Frame(main_frame, bg='#2a2a2a')
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Room label
room_label = tk.Label(left_frame, text="Select a room or talk to yourself", bg='#444', fg='white', font=('Arial', 12))
room_label.pack(fill=tk.X)

# Chat display
chat_text = scrolledtext.ScrolledText(left_frame, state=tk.DISABLED, bg='#222', fg='white', wrap=tk.WORD, font=('Arial', 12), relief='flat', borderwidth=0)
chat_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Chat message entry
chat_message_frame = tk.Frame(left_frame, bg='#2a2a2a')
chat_message_frame.pack(fill=tk.X, padx=10, pady=10)
chat_message_entry = tk.Entry(chat_message_frame, bg='#444', fg='white', font=('Arial', 12), relief='flat')
chat_message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
send_button = tk.Button(chat_message_frame, text="Send", command=send_chat_message, bg='#444', fg='white', relief='flat', font=('Arial', 12))
send_button.pack(side=tk.RIGHT)

# Right frame (rooms and users)
right_frame = tk.Frame(main_frame, bg='#333')
right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# Rooms list
rooms_label = tk.Label(right_frame, text="Rooms", bg='#333', fg='white', font=('Arial', 12))
rooms_label.pack(fill=tk.X, pady=(10, 5))

rooms_canvas = tk.Canvas(right_frame, bg='#222', borderwidth=0, highlightthickness=0)
rooms_canvas.pack(side=tk.LEFT, fill=tk.Y, expand=True)
rooms_scrollbar = tk.Scrollbar(right_frame, orient='vertical', command=rooms_canvas.yview)
rooms_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
rooms_canvas_frame = tk.Frame(rooms_canvas, bg='#222')
rooms_canvas.create_window((0, 0), window=rooms_canvas_frame, anchor='nw')
rooms_canvas.config(yscrollcommand=rooms_scrollbar.set)
rooms_canvas.bind('<Configure>', lambda e: rooms_canvas.configure(scrollregion=rooms_canvas.bbox("all")))

# Users list
users_label = tk.Label(right_frame, text="Users", bg='#333', fg='white', font=('Arial', 12))
users_label.pack(fill=tk.X, pady=(20, 5))
user_list = tk.Listbox(right_frame, bg='#222', fg='white', font=('Arial', 12), relief='flat', borderwidth=0)
user_list.pack(fill=tk.Y, expand=True)

# Create new room button
create_room_button = tk.Button(root, text="Create New Room", command=create_new_room, bg='#444', fg='white', relief='flat', font=('Arial', 12))
create_room_button.pack(side=tk.BOTTOM, padx=10, pady=10)

# Create leave room button
leave_room_button = tk.Button(root, text="Leave Room", command=leave_room, bg='#444', fg='white', relief='flat', font=('Arial', 12))
leave_room_button.pack(side=tk.BOTTOM, padx=10, pady=10)

# Load rooms initially
load_rooms()

# Start periodic refreshes
refresh_user_list()
check_for_new_messages()

root.mainloop()

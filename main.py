#!/usr/bin/env python3
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
import tkinter as tk
from functools import partial
from playsound import playsound
import json

Config = {}
Config['X'] = 0
Config['Y'] = 0
Config['X_MAX'] = 5
Config['Y_MAX'] = 5
Config['buttons'] = {}


def checkOS():
    pass  # C:\


root = tk.Tk()


def playSound(filename):
    playsound(filename)


def on_closing():
    print(json.dumps(Config))
    root.destroy()


def genButton():
    global Config
    root.filename = fd.askopenfilename(initialdir="~/Musik", title="Select file",
                                       filetypes=(("audio files", "*.mp3"), ("audio files", "*.wav")))
    if(len(root.filename) > 0):
        root.result = sd.askstring('Name', 'Enter a name for the button')
        if(root.result is not None):
            button = tk.Button(root, text=root.result, command=partial(playSound, root.filename))
            button.grid(row=Config['X'], column=Config['Y'], padx=1)
            Config['buttons'][root.result] = {}
            Config['buttons'][root.result]['X'] = Config['X']
            Config['buttons'][root.result]['Y'] = Config['Y']
            Config['buttons'][root.result]['file'] = root.filename
            if Config['Y'] > Config['Y_MAX']-2:
                Config['Y'] = 0
                Config['X'] += 1
            else:
                Config['Y'] += 1


def main():
    menu = tk.Menu(root)
    root.config(menu=menu)
    menu.add_command(label="New", command=genButton)
    root.geometry('600x400')
    root.wm_title("Soundboard")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == '__main__':
    main()

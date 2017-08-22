#!/usr/bin/env python3
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
import tkinter as tk
from functools import partial
from playsound import playsound
import pygame
import json

Config = {}
Config['X'] = 0
Config['Y'] = 0
Config['ID'] = 0
Config['X_MAX'] = 5
Config['Y_MAX'] = 5
Config['buttons'] = {}


def checkOS():
    pass  # C:\


root = tk.Tk()


def playSound(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()


def on_opening():
    global Config
    try:
        Config = json.load(open("config.json", 'r'))
        for buttonID in Config['buttons']:
            print()
            button = tk.Button(root, text=Config['buttons'][buttonID]['name'], command=partial(playSound, Config['buttons'][buttonID]['file']))
            button.grid(row=Config['buttons'][buttonID]['X'], column=Config['buttons'][buttonID]['Y'], padx=1)
    except FileNotFoundError as e:
        print("No Config")


def on_closing():
    print(json.dumps(Config))
    f = open("config.json", 'w')
    f.write(json.dumps(Config, indent=4))
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
            Config['buttons'][Config['ID']] = {}
            Config['buttons'][Config['ID']]['name'] = root.result
            Config['buttons'][Config['ID']]['X'] = Config['X']
            Config['buttons'][Config['ID']]['Y'] = Config['Y']
            Config['buttons'][Config['ID']]['file'] = root.filename
            Config['ID'] += 1
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
    on_opening()
    root.mainloop()


if __name__ == '__main__':
    main()

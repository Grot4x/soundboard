#!/usr/bin/env python3
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
import tkinter as tk
from functools import partial
from playsound import playsound


def checkOS():
    pass  # C:\


root = tk.Tk()


def playSound(filename):
    playsound(filename)


def genButton():
    root.filename = fd.askopenfilename(initialdir="~/Musik", title="Select file",
                                       filetypes=(("audio files", "*.mp3"), ("audio files", "*.wav")))
    root.result = sd.askstring('Name', 'Enter a name for the button')
    if(len(root.filename) > 0):
        button = tk.Button(root, text=root.result, command=partial(playSound, root.filename))
        button.grid()


def main():
    menu = tk.Menu(root)
    root.config(menu=menu)
    menu.add_command(label="New", command=genButton)
    w = tk.Label(root, text="Hello World")
    w.grid()
    root.geometry('400x400')
    root.mainloop()


if __name__ == '__main__':
    main()

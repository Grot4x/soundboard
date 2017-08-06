#!/usr/bin/env python3
from tkinter import filedialog as fd
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
    button = tk.Button(root, text="lol", command=partial(playSound, root.filename))
    button.pack()


def main():
    menu = tk.Menu(root)
    root.config(menu=menu)
    menu.add_command(label="New", command=genButton)
    w = tk.Label(root, text="Hello World")
    w.pack()
    root.mainloop()


if __name__ == '__main__':
    main()

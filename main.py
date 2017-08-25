#!/usr/bin/env python3
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
from tkinter import messagebox as mb
import tkinter as tk
from functools import partial
from threading import Thread, Event
import os
import pyaudio
import wave
import sys
import json
import time

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
threads = []


class AudioFile(Thread):
    def __init__(self, filename):
        Thread.__init__(self)
        self._halt = Event()
        self.filename = filename
        self.p = pyaudio.PyAudio()
        self.CHUNK = 1024
        if os.path.isfile(self.filename):
            self.wf = wave.open(self.filename, 'rb')
            self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                      channels=self.wf.getnchannels(),
                                      rate=self.wf.getframerate(),
                                      output=True)
        else:
            mb.showerror("Error", "File not found: %s" % (self.filename))
            # print("file not found")

    def run(self):
        data = self.wf.readframes(self.CHUNK)
        while data != b"" and not self._halt.is_set():
            self.stream.write(data)
            data = self.wf.readframes(self.CHUNK)
        self.halt()

    def halt(self):
        self._halt.set()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.wf.close()


def playSound(filename):
    global threads
    for t in threads:
        if not t.isAlive():
            t.handled = True
        else:
            print("stopping old one")
            t.halt()
            t.join()
            t.handled = True
    threads = [t for t in threads if not t.handled]
    print("Starting new one")
    t = AudioFile(filename)
    threads.append(t)
    t.start()


def on_opening():
    global Config
    try:
        Config = json.load(open("config.json", 'r'))
        for buttonID in Config['buttons']:
            button = tk.Button(root, text=Config['buttons'][buttonID]['name'], command=partial(
                playSound, Config['buttons'][buttonID]['file']))
            button.grid(row=Config['buttons'][buttonID]['X'],
                        column=Config['buttons'][buttonID]['Y'], padx=1)
    except FileNotFoundError as e:
        mb.showinfo("Info", "No config file was found")
        # print("No Config")


def on_closing():
    f = open("config.json", 'w')
    f.write(json.dumps(Config, indent=4))
    root.destroy()


def genButton():
    global Config
    root.filename = fd.askopenfilename(initialdir="~/Musik", title="Select file",
                                       filetypes=(("audio files", "*.mp3"), ("audio files", "*.wav")))
    if(len(root.filename) > 0):
        root.result = sd.askstring('Name', 'Enter a name for the button')
        if(root.result is not None and len(root.result) > 0):
            button = tk.Button(root, text=root.result,
                               command=partial(playSound, root.filename))
            button.grid(row=Config['X'], column=Config['Y'], padx=1)
            Config['buttons'][Config['ID']] = {}
            Config['buttons'][Config['ID']]['name'] = root.result
            Config['buttons'][Config['ID']]['X'] = Config['X']
            Config['buttons'][Config['ID']]['Y'] = Config['Y']
            Config['buttons'][Config['ID']]['file'] = root.filename
            Config['ID'] += 1
            if Config['Y'] > Config['Y_MAX'] - 2:
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

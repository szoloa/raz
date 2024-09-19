from .custom import custom, listener_v
import tkinter as tk
from tkinter import ttk
from pynput import keyboard
import random

# 实验性功能
class BetaT(tk.Frame):
    def __init__(self, master = None, bro = None):
        super().__init__(master)
        self.master = master
        self.bro = bro
        self.pack()
        self.createFrame()

    def createFrame(self):
        self.button_right = ttk.Button(self, text='开始', command=self.quickStart)

        global listener_v
        if listener_v and listener_v.running:
            self.button_right['text'] = '结束'
            self.button_right['command'] = self.quickStop
            
        self.button_right.pack()

    def quickStart(self):
        global listener_v
        def press(key):
            if key.char == "j":
                chioce = random.choice(custom.get_theme())
                custom.openWeb(chioce)
                self.bro.saveResult(chioce)

        if listener_v is None or not listener_v.running:
            listener_v = keyboard.Listener(on_press=press)
            listener_v.start()
            self.button_right['text'] = '结束'
            self.button_right['command'] = self.quickStop

    def quickStop(self):
        global listener_v
        if listener_v and listener_v.running:
            listener_v.stop()
            self.button_right['text'] = '开始'
            self.button_right['command'] = self.quickStart
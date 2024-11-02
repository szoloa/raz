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
        pass
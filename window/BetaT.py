from .custom import custom
import tkinter as tk
from tkinter import ttk

# 实验性功能
class BetaT(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createFrame()

    def createFrame(self):
        self.button_right = ttk.Button(self, text='开始',) # command=self.quickStart)
        self.button_right.pack()
        global isKilled
        isKilled = True

    # def quickStart(self):
    #     global isKilled
    #     if not isKilled:
    #         isKilled = True
    #     def runKey():
    #         def press(key):
    #             if key.char == "j":
    #                 chioce = random.choice(theme)
    #                 openWeb(chioce)
    #             return isKilled
    #         with keyboard.Listener(on_press = press) as listener:
    #             listener.join()
    #     self.thread_01 = Process(target=runKey)
    #     self.thread_01.start()
    #     self.button_right['text'] = '结束'
    #     self.button_right['command'] = self.quickStop

    # def quickStop(self):
    #     if self.thread_01.is_alive:
    #         global isKilled
    #         isKilled = False
    #         if not self.thread_01.is_alive:
    #             self.button_right['text'] = '开始'
    #             self.button_right['command'] = self.quickStart
        

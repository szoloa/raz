import random
import webbrowser
from tkinter import *
import tkinter as tk

class appliction(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createFrame()

    def createFrame(self):
        self.button_goto = Button(self)
        self.button_goto['text'] = '选择'
        self.button_goto['command'] = self.chioceTheme
        self.button_goto.pack()

        # 历史记录
        
    def chioceTheme(self):
        f = open(r'raz\data.txt', encoding='utf-8')
        theme = f.readlines()
        chioce = random.choice(theme)
        webbrowser.open('https://search.bilibili.com/all?keyword=%s' % (chioce))

root = Tk()
root.geometry("500x300+100+200")
appliction(master=root)

root.mainloop()
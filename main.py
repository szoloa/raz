import random
import webbrowser
from tkinter import *
import tkinter as tk

f = open(r'.\data.txt', encoding='utf-8')
theme = f.readlines()

def openWeb(theme):
    webbrowser.open('https://search.bilibili.com/all?keyword=%s' % (theme))

class appliction(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createFrame()

    def createFrame(self):

        self.button_rand = Button(self)
        self.button_rand['text'] = '随机'
        self.button_rand['command'] = self.chioceTheme

        self.button_goto = Button(self)
        self.button_goto['text'] = '选择'
        self.button_goto['command'] = self.openHistoryPage
        
        self.button_muti = Button(self)
        self.button_muti['text'] = '随机多个'
        self.button_muti['command'] = self.openMuti

        # 历史记录
        self.lsb = Listbox(self) 
        
        self.button_rand.pack()
        self.button_goto.pack()
        self.button_muti.pack()
        self.lsb.pack()

    def chioceTheme(self):
        chioce = random.choice(theme)
        self.lsb.insert(0, chioce)
        openWeb(chioce)
    
    def openHistoryPage(self):
        openWeb(self.lsb.get(self.lsb.curselection()))
    
    def openMuti(self, time=5):
        for i in range(time):
            chioce = random.choice(theme)
            self.lsb.insert(0, chioce)

root = Tk()
root.geometry("500x300+100+200")
root.title("开启随机主题")

appliction(master=root)

root.mainloop()
import random
import webbrowser
from tkinter import *
import tkinter as tk
import tkinter.filedialog

f = open(r'.\data.txt', encoding='utf-8')
global theme
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

        self.button_front = Button(self)
        self.button_front['text'] = '置于最前'
        self.button_front['command'] = self.windFront

        self.button_userDo = Button(self)
        self.button_userDo['text'] = '自定义随机文件'
        self.button_userDo['command'] = self.userDo
        # 历史记录
        self.lsb = Listbox(self) 
        
        self.button_rand.pack()
        self.button_goto.pack()
        #self.button_muti.pack()
        self.button_front.pack()
        self.button_userDo.pack()
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

    def windFront(self):
        if self.button_front['text'] == '置于最前':
            self.master.attributes('-topmost', 1)
            self.button_front['text'] = '取消置于最前'
        else:
            self.master.attributes('-topmost', 0)
            self.button_front['text'] = '置于最前'
    
    def userDo(self):
        path_ = tkinter.filedialog.askopenfilename()
        path_=path_.replace("/","\\\\")
        f = open(path_, encoding='utf-8')
        global theme
        theme = f.readlines()

root = Tk()
root.geometry("500x300+100+200")
root.title("开启随机主题")

root.lift()
root.attributes('-topmost',True)
root.after_idle(root.attributes,'-topmost',False)

appliction(master=root)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

root.mainloop()
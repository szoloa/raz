from .custom import custom
from .BetaT import BetaT
from .InputW import inputW
from .UserItem import UserItem
from .AppSetting import Appset
import random
from tkinter import Listbox
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import clipboard

# 主程序窗口
class appliction(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createFrame()
        self.child_windows = []
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def createFrame(self):
        style = ttk.Style()
        style.configure('TButton', font=("黑体", 11))
        self.button_rand = ttk.Button(self)
        self.button_rand['text'] = '> 随机开启一个主题 <'
        self.button_rand['width'] = 64
        self.button_rand['command'] = self.chioceTheme
        
        self.button_rand_n = ttk.Button(self)
        self.button_rand_n['text'] = '仅随机而不跳转'
        self.button_rand_n['width'] = 16
        self.button_rand_n['command'] = self.chioceThemeNotGo

        self.button_goto = ttk.Button(self)
        self.button_goto['text'] = '选择跳转此主题'
        self.button_goto['width'] = 64
        self.button_goto['command'] = self.openHistoryPage
        
        self.button_muti = ttk.Button(self)
        self.button_muti['text'] = '随机多个'
        self.button_muti['width'] = 6
        self.button_muti['command'] = self.openMuti

        self.button_front = ttk.Button(self)
        self.button_front['text'] = '置于最前'
        self.button_front['width'] = 16
        self.button_front['command'] = self.windFront

        self.button_userDo = ttk.Button(self)
        self.button_userDo['text'] = '自定义随机文件'
        self.button_userDo['width'] = 16
        self.button_userDo['command'] = self.userDo

        self.buttoon_changeWeb = ttk.Button(self, text='更改搜索引擎', command=self.changeWeb, width=16)

        self.buttoon_beta = ttk.Button(self, text='实验性功能', command=self.betaT, width=16)
        self.buttoon_setting = ttk.Button(self, text='设置', command=self.Appsetting, width=16)
        
        self.label_web = ttk.Label(self, text='当前搜索引擎: %s' %(custom.get_web()), font=('黑体', 12))

        if custom.get_search_type_s() == 'url':
            self.label_web['text'] = '当前搜索引擎: %s' %(custom.get_search_type_s())
        else:
            if custom.get_search_type() == 'random':
                self.label_web['text'] = '当前搜索引擎: %s' %(custom.get_search_type())
            elif custom.get_search_type() == 'single':
                self.label_web['text'] = '当前搜索引擎: %s' %(custom.get_web_name())

        # 历史记录
        self.lsb = Listbox(self, width=56, font=("黑体", 12)) 

        self.lsb.bind('<Return>', self.openHistoryPage)
        self.lsb.bind('<Up>', lambda :self.lsb.activate(self.lsb.curselection()-1))
        self.lsb.bind('<Down>', lambda :self.lsb.activate(self.lsb.curselection()-1))

        self.master.bind_all('<f>', self.chioceTheme)
        
        self.button_rand.grid(row=4, column=0, padx=4, pady=4, columnspan=4)
        self.button_rand_n.grid(row=0, column=0, padx=4, pady=4)
        self.button_goto.grid(row=3, column=0, padx=4, pady=4, columnspan=4)
        #self.button_muti.pack()
        self.button_front.grid(row=0, column=1, padx=4, pady=4)
        self.button_userDo.grid(row =0, column=2, padx=4, pady=4)
        self.buttoon_changeWeb.grid(row=0, column=3, padx=4, pady=4)
        self.lsb.grid(row=2, column=0, columnspan=4)
        self.buttoon_beta.grid(row=5, column=0, padx=4, pady=4, columnspan=2)
        self.buttoon_setting.grid(row=5, column=2, padx=4, pady=4, columnspan=2)
        self.label_web.grid(row=6, column=0, padx=4, pady=4, columnspan=4)

    def upUiGoto(self):
        self.button_rand['text'] = '> 随机开启一个主题 <'
        self.button_goto['text'] = '选择跳转此主题'
        self.update_idletasks()

    def chioceTheme(self, *args):
        if self.button_rand['text'] == '> 跳转中 <':
            return 

        if custom.get_language() != 0:
            self.button_rand['text'] = '> 跳转中 <'
            self.update_idletasks()
            chioce = custom.get_theme()
            custom.openWeb(chioce.url, self)
            self.saveResult(chioce)
        else:    
            chioce = custom.get_theme()
            custom.openWeb(chioce.url)
            self.saveResult(chioce)

    
    def openHistoryPage(self, *args):
        temp = self.lsb.get(self.lsb.curselection())
        if temp == '':
            return
        if self.button_goto['text'] == '跳转中':
            return
        if custom.get_language() != 0:
            self.button_goto['text'] = '跳转中'
            self.update_idletasks()
            custom.openWeb(temp, self)
        else:
            custom.openWeb(temp)

    def openMuti(self, time=5):
        for i in range(time):
            chioce = random.choice(custom.get_theme())
            self.lsb.insert(0, chioce)

    def windFront(self):
        if self.button_front['text'] == '置于最前':
            self.master.attributes('-topmost', 1)
            self.button_front['text'] = '取消置于最前'
        else:
            self.master.attributes('-topmost', 0)
            self.button_front['text'] = '置于最前'
    
    # 跳转
    def userDo(self):
        root_web = Toplevel()

        root_x = self.master.winfo_x()
        root_y = self.master.winfo_y()
        root_width = self.master.winfo_width()
        root_height = self.master.winfo_height()

        child_x = root_x - 500 - 20 # -    # 主窗口右侧 20 像素
        child_y = root_y  - root_height // 2  # 垂直居中于主窗口

        root_web.geometry(f"500x720+{child_x}+{child_y}")
        root_web.title("更改随机条目")
        # root_web.iconphoto(True, PhotoImage(file='logo.png'))
        UserItem(master=root_web) 
        self.child_windows.append(root_web)
    # 跳转
    def changeWeb(self):
        root_web = Toplevel()
    
        # 获取主窗口的位置和大小
        root_x = self.master.winfo_x()
        root_y = self.master.winfo_y()
        root_width = self.master.winfo_width()
        root_height = self.master.winfo_height()

        # 计算子窗口的位置（相对于主窗口的右下角）
        child_x = root_x + root_width + 20  # 主窗口右侧 20 像素
        child_y = root_y  - root_height // 2  # 垂直居中于主窗口

        root_web.geometry(f"500x720+{child_x}+{child_y}")
        root_web.title("更改搜索引擎")
        # root_web.iconphoto(True, PhotoImage(file='logo.png'))
        inputW(master=root_web, bro=self)   
    
    def chioceThemeNotGo(self):
        chioce = custom.get_theme()
        self.saveResult(chioce)
        msg = messagebox.askokcancel("确定或取消", f"随机结果为：{chioce.text}是否复制到剪切板？")
        if msg:
            clipboard.copy(chioce.text)
        
    def saveResult(self, chioce):
        self.lsb.insert(0, chioce.text)
        with open(r'./hostory.txt', 'a+', encoding='utf-8') as f:
            f.writelines(f'{str(chioce)}\n')

    def betaT(self):
        root_web = Toplevel()

        # 获取主窗口的位置和大小
        root_x = self.master.winfo_x()
        root_y = self.master.winfo_y()
        root_width = self.master.winfo_width()
        root_height = self.master.winfo_height()

        # 计算子窗口的位置（相对于主窗口的右下角）
        child_x = root_x + 70 # + root_width // 2 # 20  # 主窗口右侧 20 像素
        child_y = root_y  - 200 - 20 # root_height // 2  # 垂直居中于主窗口

        root_web.geometry(f"500x160+{child_x}+{child_y}")
        root_web.title("实验性功能")
        # root_web.iconphoto(True, PhotoImage(file='logo.png'))
        BetaT(master=root_web, bro=self) 
        self.child_windows.append(root_web)
    
    def Appsetting(self):
        root_set = Toplevel()
        root_set.geometry("500x400+200+300")
        root_set.title("设置")
        # root_web.iconphoto(True, PhotoImage(file='logo.png'))
        Appset(master=root_set) 
        self.child_windows.append(root_set)

    def on_closing(self):
        """当主窗口关闭时，关闭所有子窗口"""
        for window in self.child_windows:
            window.destroy()  # 关闭所有子窗口
        self.master.destroy()  # 最后关闭主窗口
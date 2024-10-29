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

        style = ttk.Style()
        style.configure('TButton', font=("黑体", 11))

        style_r = ttk.Style()
        style_r.configure('TRadiobutton', font=("黑体", 11))
        self.button_right = ttk.Button(self, text='开启按J跳转', command=self.quickStart)
        self.button_u = ttk.Button(self, text='关闭搜索引擎', command=self.NoneUrl)

        global listener_v
        if listener_v and listener_v.running:
            self.button_right['text'] = '关闭按J跳转'
            self.button_right['command'] = self.quickStop
        
        if custom.get_search_type_s() == 'url':
            self.button_u['text'] = '使用搜索引擎'
            self.button_u['command'] = self.UnNoneUrl

        self.label_language = ttk.Label(self, text='将随机内容翻译至', font=("黑体", 11))
        self.radiobutton_language_var = tk.IntVar()
        self.radiobutton_language_var.set(custom.get_language())

        # 创建四个单选按钮，使用同一个 IntVar 来绑定其值
        self.radiobutton_language_origin = ttk.Radiobutton(self, text='不翻译词条', value=0, variable=self.radiobutton_language_var, command=self.changeLanguage)
        self.radiobutton_language_chinese = ttk.Radiobutton(self, text='中文转英文', value=1, variable=self.radiobutton_language_var, command=self.changeLanguage)
        self.radiobutton_language_english = ttk.Radiobutton(self, text='英文转中文', value=2, variable=self.radiobutton_language_var, command=self.changeLanguage)
        self.radiobutton_language_janpanese = ttk.Radiobutton(self, text='中文转日文', value=3, variable=self.radiobutton_language_var, command=self.changeLanguage)


        self.button_right.pack(pady=4)
        self.button_u.pack(pady=4)

        self.label_language.pack(side='top', pady=4)
        self.radiobutton_language_origin.pack(side='left')
        self.radiobutton_language_chinese.pack(side='left')
        self.radiobutton_language_english.pack(side='left')
        self.radiobutton_language_janpanese.pack(side='left')

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
    
    def NoneUrl(self):
        custom.set_search_type_s('url')
        self.button_u['text'] = '使用搜索引擎'
        self.button_u['command'] = self.UnNoneUrl
    
    def UnNoneUrl(self):
        custom.set_search_type_s('theme')
        self.button_u['text'] = '关闭搜索引擎'
        self.button_u['command'] = self.NoneUrl

    def changeLanguage(self):
        custom.set_language(self.radiobutton_language_var.get())
import tkinter as tk
from .custom import custom, listener_v
from tkinter import ttk, messagebox
from pynput import keyboard
import random

class Appset(tk.Frame):
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

        frame_radiobutton = ttk.Frame(self)

        self.label_language = ttk.Label(frame_radiobutton, text='将随机内容翻译至', font=("黑体", 11))
        self.radiobutton_language_var = tk.IntVar()
        self.radiobutton_language_var.set(custom.get_language())

        
        # 创建四个单选按钮，使用同一个 IntVar 来绑定其值
        self.radiobutton_language_origin = ttk.Radiobutton(frame_radiobutton, text='不翻译词条', value=0, variable=self.radiobutton_language_var, command=self.changeLanguage)
        self.radiobutton_language_chinese = ttk.Radiobutton(frame_radiobutton, text='中文转英文', value=1, variable=self.radiobutton_language_var, command=self.changeLanguage)
        self.radiobutton_language_english = ttk.Radiobutton(frame_radiobutton, text='英文转中文', value=2, variable=self.radiobutton_language_var, command=self.changeLanguage)
        self.radiobutton_language_janpanese = ttk.Radiobutton(frame_radiobutton, text='中文转日文', value=3, variable=self.radiobutton_language_var, command=self.changeLanguage)


        self.button_right.pack(pady=4)
        self.button_u.pack(pady=4)
        frame_radiobutton.pack()

        self.label_language.pack(side='top', pady=4)
        self.radiobutton_language_origin.pack(side='left')
        self.radiobutton_language_chinese.pack(side='left')
        self.radiobutton_language_english.pack(side='left')
        self.radiobutton_language_janpanese.pack(side='left')

        frame_button = ttk.Frame(self)
        frame_button.pack(pady=4)

        self.button_save = ttk.Button(frame_button, text='保存设置', command=self.__save_setting)

        self.button_save.pack(side='right')

    def __save_setting(self):
        custom.save_setting()
        messagebox.showinfo('成功', '保存成功！')

    def quickStart(self):
        global listener_v
        def press(key):
            try:
                if key.char == "j":
                    chioce = custom.get_theme()
                    custom.openWeb(chioce.url)
                    self.bro.saveResult(chioce)
            except Exception as e:
                pass

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
        self.bro.label_web['text'] = '当前搜索引擎: %s' %(custom.get_search_type_s())
        self.button_u['command'] = self.UnNoneUrl
    
    def UnNoneUrl(self):
        custom.set_search_type_s('theme')
        self.button_u['text'] = '关闭搜索引擎'
        if custom.get_search_type() == 'random':
            self.bro.label_web['text'] = '当前搜索引擎: %s' %(custom.get_search_type())
        elif custom.get_search_type() == 'single':
            self.bro.label_web['text'] = '当前搜索引擎: %s' %(custom.get_web_name())
        self.button_u['command'] = self.NoneUrl

    def changeLanguage(self):
        custom.set_language(self.radiobutton_language_var.get())
import tkinter as tk
from .custom import custom
from tkinter import ttk, messagebox

class Appset(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createFrame()

    def createFrame(self):
        self.button_save = ttk.Button(self, text='保存设置', command=self.__save_setting)

        self.button_save.pack()

    def __save_setting(self):
        custom.save_setting()
        messagebox.showinfo('成功', '保存成功！')
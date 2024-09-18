from .custom import custom
from tkinter import Listbox
from tkinter import *
import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
from os import listdir as os_listdir

# 修改随机配置文件
class UserItem(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createFrame()

    def createFrame(self):
        style01 = ttk.Style()
        style01.configure('TButton01', font=("黑体", 16))

        self.button_userFile = ttk.Button(self, text='导入配置文件', command=self.userDo, style='TButton')
        self.lsb = Listbox(self, font=("黑体", 12), width=36) 

        self.label_tiem = ttk.Label(self, text='当前随机内容\n仅显示前40项', font=('黑体', 12))
        self.entry_item = ttk.Entry(self, width=45)
        for i in custom.get_theme()[:40]:
            self.lsb.insert(0, i)


        self.button_add = ttk.Button(self, text='添加', command=self.addItem)
        self.button_del = ttk.Button(self, text='删除', command=self.delItem)
        self.button_delall = ttk.Button(self, text='清空', command=self.delAllItem)

        self.lsb_ls = Listbox(self, font=("黑体", 12), width=36) 
        for i in custom.get_Item():
            self.lsb_ls.insert(0, i)
        self.button_ls_right = ttk.Button(self, text='确定', command=self.ls_right)

        self.button_userFile.pack()
        self.label_tiem.pack()
        self.lsb.pack()
        
        self.entry_item.pack()
        self.button_add.pack()
        self.button_del.pack()
        self.button_delall.pack()

        self.lsb_ls.pack()
        self.button_ls_right.pack()

    def userDo(self):
        path_ = tkinter.filedialog.askopenfilename(
            title='请选择文件',
        filetypes=[('文本', '.txt .TXT')])

        if path_ == '':
            return
        path_ = path_.replace("/","\\\\")
        f = open(path_, encoding='utf-8')
        theme = custom.get_theme()
        custom.set_theme(f.readlines())
        for i in theme[:20]:
            self.lsb.insert(0, i)

        self.lsb_ls.insert(0, path_)
        item = custom.get_Item()
        item.append(path_)
        custom.set_Item(item)
        f.close()

    def addItem(self):
        item = self.entry_item.get()
        if item == '':
            return
        theme = custom.get_theme()
        custom.set_theme(theme.append(item))
        self.lsb.insert(0, item)
        self.entry_item.delete(0, END)

    def delItem(self):
        theme = custom.get_theme()
        item = self.lsb.curselection()
        if self.lsb.get(item) in theme:
            theme.remove(self.lsb.get(item))
        self.lsb.delete(item)

    def delAllItem(self):
        theme = custom.get_theme()
        self.lsb.delete(0, END)
        custom.set_theme(theme.clear())

    def ls_right(self):
        item = self.lsb_ls.get(self.lsb_ls.curselection())
        if item == '':
            return
        f = open(item, encoding='utf-8')
        theme = custom.get_theme()
        custom.set_theme(f.readlines())
        f.close()
        self.lsb.delete(0, END)
        for i in custom.get_theme()[:40]:
            self.lsb.insert(0, i)
        

from .custom import custom
from tkinter import Listbox, messagebox
from tkinter import *
import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
import requests

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

        # 配置文件导入按钮
        self.button_userFile = ttk.Button(self, text='导入配置文件', command=self.userDo, style='TButton', width=16)

        # 随机内容列表
        self.lsb = Listbox(self, font=("黑体", 12), width=36, height=10)

        for i in custom.get_theme_list()[:40]:
            self.lsb.insert(0, i)


        # 显示前40项的标签
        self.label_tiem = ttk.Label(self, text='当前随机内容\n仅显示前40项', font=('黑体', 12))

        # 随机条目输入框和按钮
        self.entry_item = ttk.Entry(self, width=30)
        self.button_add = ttk.Button(self, text='添加', command=self.addItem, style='TButton', width=10)
        self.button_del = ttk.Button(self, text='删除', command=self.delItem, style='TButton', width=10)
        self.button_delall = ttk.Button(self, text='清空', command=self.delAllItem, style='TButton', width=10)

        # 加载主题列表
        self.lsb_ls = Listbox(self, font=("黑体", 12), width=36, height=10)
        for i in custom.get_Item():
            self.lsb_ls.insert(0, i)

        # 应用随机条目按钮
        self.button_ls_right = ttk.Button(self, text='应用随机条目文件', command=self.ls_right, style='TButton', width=16)

        # 网络文件导入部分
        self.entry_internet_item = ttk.Entry(self, width=30)
        self.button_internet = ttk.Button(self, text='导入网络文件', command=self.internet_catch, style='TButton', width=16)

        # 使用网格布局进行布局调整
        self.label_tiem.grid(row=0, column=0, columnspan=4, pady=4, padx=4)
        self.lsb.grid(row=1, column=0, columnspan=4, pady=4, padx=4)

        self.entry_item.grid(row=2, column=0, columnspan=2, pady=4, padx=4)
        self.button_add.grid(row=2, column=2, pady=4, padx=4)
        self.button_del.grid(row=2, column=3, pady=4, padx=4)
        self.button_delall.grid(row=3, column=0, columnspan=4, pady=4, padx=4)

        self.lsb_ls.grid(row=4, column=0, columnspan=4, pady=4, padx=4)
        self.button_ls_right.grid(row=5, column=0, columnspan=4, pady=4, padx=4)

        self.entry_internet_item.grid(row=6, column=0, columnspan=2, pady=4, padx=4)
        self.button_internet.grid(row=6, column=2, columnspan=2, pady=4, padx=4)

        self.button_userFile.grid(row=7, column=0, columnspan=4, pady=4, padx=4)


    def userDo(self):
        path_ = tkinter.filedialog.askopenfilename(
            title='请选择文件',
        filetypes=[('文本', '.txt .TXT')])

        if path_ == '':
            return
        path_ = path_.replace("/","////")
        # f = open(path_, encoding='utf-8')
        # theme = custom.get_theme()
        # custom.set_theme(f.readlines())
        # for i in theme[:20]:
        #     self.lsb.insert(0, i)

        self.lsb_ls.insert(0, path_)
        item = custom.get_Item()
        item.append(path_)
        custom.set_Item(item)
        # f.close()

    def addItem(self):
        item = self.entry_item.get()
        if item == '':
            return
        theme = custom.get_theme_list()
        theme.append(item)
        custom.set_theme(theme)
        self.lsb.insert(0, item)
        self.entry_item.delete(0, END)

    def delItem(self):
        theme = custom.get_theme_list()
        item = self.lsb.curselection()
        if self.lsb.get(item) in theme:
            theme.remove(self.lsb.get(item))
            custom.set_theme(theme)
        self.lsb.delete(item)

    def delAllItem(self):
        theme = custom.get_theme_list()
        self.lsb.delete(0, END)
        theme.clear()
        custom.set_theme(theme)

    def ls_right(self):
        item = self.lsb_ls.get(self.lsb_ls.curselection())
        if item == '':
            return
        f = open(item, encoding='utf-8')
        theme = custom.get_theme_list()
        custom.set_theme([i.replace('\n','').replace('\r','') for i in f.readlines()])
        f.close()
        self.lsb.delete(0, END)
        for i in custom.get_theme_list()[:40]:
            self.lsb.insert(0, i)
    
    def internet_catch(self):
        url = self.entry_internet_item.get()
        if url == '':
            return
        try:
            r = requests.get(url)
            theme = r.text.splitlines()
            custom.set_theme(theme)
            for i in theme[:20]:
                self.lsb.insert(0, i)
            custom.set_theme(theme)
            self.lsb.delete(0, END)
            for i in theme[:40]:
                self.lsb.insert(0, i)
        except:
            messagebox.showinfo('失败', '导入失败')

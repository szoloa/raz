from .custom import custom
from tkinter import Listbox
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import requests
from tkinter import ttk
import json
import tkinter.filedialog

# 修改搜索引擎
class inputW(tk.Frame):
    def __init__(self, master = None, bro = None):
        super().__init__(master)
        self.master = master
        self.bro = bro
        self.pack()
        self.createFrame()

    def createFrame(self):
        style = ttk.Style()
        style.configure('TButton', font=("黑体", 11))
        self.label_web = ttk.Label(self, text='此处输入链接\n内容用%s代替', font=('黑体', 12))

        self.v1 = StringVar()
        self.entry_web = ttk.Entry(self, textvariable=self.v1, width=45)
        
        self.label_list = ttk.Label(self, text=r'预设搜索引擎', font=('黑体', 12))
        self.lsb = Listbox(self, font=("黑体", 12), width=36) 

        for item in reversed(custom.get_web_dict()):
            self.lsb.insert(0, item)
             
        search_type = custom.get_search_type()
        if search_type == 'single':
            self.button_write = ttk.Button(self, text='填入', command=self.list_write)
            self.button_random_web = ttk.Button(self, text='开启随机搜索引擎', command=self.random_web)
            self.button_right = ttk.Button(self, text='确定', command=self.changeWeb)
        elif search_type == 'random':
            self.button_write = ttk.Button(self, text='删除', command=self.list_write_del)
            self.button_random_web = ttk.Button(self, text='关闭随机搜索引擎', command=self.random_web_stop)
            self.button_right = ttk.Button(self, text='添加', command=self.addWeb)

        self.button_save = ttk.Button(self, text='保存配置文件', command=self.save_change_dict)
        self.button_load = ttk.Button(self, text='导入配置文件', command=self.load_change_dict)

        self.label_web.pack()
        self.entry_web.pack()
        self.button_right.pack()
        self.label_list.pack()
        self.lsb.pack()
        self.button_write.pack()

        self.button_random_web.pack()
        self.button_save.pack()
        self.button_load.pack()

    def changeWeb(self):
        ipt = self.entry_web.get()
        if ipt != '':
            if self.checkUrl(ipt):
                msg = messagebox.askokcancel("确认修改", "将搜索链接修改为%s" % (ipt), parent=self)
            else:
                msg = messagebox.askokcancel("确认修改", "将搜索链接修改为%s，链接好像不可用" % (ipt), parent=self)
            if msg:
                custom.set_web(ipt)
                self.bro.label_web['text'] = '当前搜索引擎: %s' %(custom.get_web_name())
                self.master.destroy()
            else:
                self.master.lift()
                self.master.attributes('-topmost',True)
                self.master.after_idle(self.master.attributes,'-topmost',False)

    def addWeb(self):
        web_dict = custom.get_web_dict()
        ipt = self.entry_web.get()
        if self.checkUrl(ipt):
            msg = messagebox.askokcancel("确认添加", "将搜索链接添加%s" % (ipt), parent=self)
        else:
            msg = messagebox.askokcancel("确认添加", "将搜索链接添加%s，链接好像不可用" % (ipt), parent=self)
        if msg:
            web_dict[ipt] = ipt
            custom.set_web_dict(web_dict)
            self.lsb.insert(0,ipt)
        
    def list_write(self):
        item = self.lsb.get(self.lsb.curselection())
        if item == '':
            return
        msg = messagebox.askokcancel("确认修改", "将搜索链接修改为%s" % (item), parent=self)
        if msg:
            custom.set_web(custom.get_web_dict()[item])
            self.bro.label_web['text'] = '当前搜索引擎: %s' %(custom.get_web_name())
            self.master.destroy()
        else:
            self.master.lift()
            self.master.attributes('-topmost',True)
            self.master.after_idle(self.master.attributes,'-topmost',False)

    def list_write_del(self):
        item = self.lsb.get(self.lsb.curselection())
        if item == '':
            return
        web_dict = custom.get_web_dict()
        msg = messagebox.askokcancel("确认删除", "将从搜索链接列表删除%s" % (item), parent=self)
        if msg:
            del web_dict[item]
            custom.set_web_dict(web_dict)
            self.lsb.delete(self.lsb.curselection())
        else:
            self.master.lift()
            self.master.attributes('-topmost',True)
            self.master.after_idle(self.master.attributes,'-topmost',False)
        

    def checkUrl(self, url, word='当你'):
        if '%s' not in url:
            return False
        r = requests.get(url % (word))
        result = r.status_code
        if (result == 200):
            return True
        else:
            return False
    
    def random_web(self):
        custom.set_search_type('random')
        self.button_right['command'] = self.addWeb
        self.button_random_web['text'] = '关闭随机搜索引擎'
        self.button_random_web['command'] = self.random_web_stop
        self.button_write['text'] = '删除'
        self.button_write['command'] = self.list_write_del

        self.bro.label_web['text'] = '当前搜索引擎: %s' %(custom.get_search_type())
    
    def random_web_stop(self):
        custom.set_search_type('single')
        self.button_write['text'] = '填入'
        self.button_write['command'] = self.list_write
        self.button_right['command'] = self.changeWeb
        self.button_random_web['text'] = '开启随机搜索引擎'
        self.button_random_web['command'] = self.random_web

        self.bro.label_web['text'] = '当前搜索引擎: %s' %(custom.get_web_name())

    def save_change_dict(self):
        j = json.dumps(custom.get_web_dict())
        f = open('./web.json', 'w')
        f.write(j)
        f.close()
        messagebox.showinfo(title='保存成功', message='搜索引擎配置文件保存成功')
    
    def load_change_dict(self):
        path_ = tkinter.filedialog.askopenfilename(
            title='请选择文件',
        filetypes=[('文本', '.json')])

        if path_ == '':
            return
        path_ = path_.replace("/","\\\\")
        f = open(path_, 'r')
        j = json.loads(f.read())
        for item in reversed(j):
            self.lsb.insert(0, item)
        d = {}
        d.update(j)      
        d.update(custom.get_web_dict())
        custom.set_web_dict(d)
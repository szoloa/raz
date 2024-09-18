from .custom import *

# 修改搜索引擎
class inputW(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
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
        for item in reversed(web_dict):
            self.lsb.insert(0, item)
             
        global search_type
        if search_type == 'single':
            self.button_write = ttk.Button(self, text='填入', command=self.list_write)
            self.button_random_web = ttk.Button(self, text='开启随机搜索引擎', command=self.random_web)
            self.button_right = ttk.Button(self, text='确定', command=self.changeWeb)
        elif search_type == 'random':
            self.button_write = ttk.Button(self, text='删除', command=self.list_write_del)
            self.button_random_web = ttk.Button(self, text='关闭随机搜索引擎', command=self.random_web_stop)
            self.button_right = ttk.Button(self, text='确定', command=self.addWeb)

        self.label_web.pack()
        self.entry_web.pack()
        self.button_right.pack()
        self.label_list.pack()
        self.lsb.pack()
        self.button_write.pack()

        self.button_random_web.pack()

    def changeWeb(self):
        global web
        ipt = self.entry_web.get()
        if self.checkUrl(ipt):
            msg = messagebox.askokcancel("确认修改", "将搜索链接修改为%s" % (ipt), parent=self)
        else:
            msg = messagebox.askokcancel("确认修改", "将搜索链接修改为%s，链接好像不可用" % (ipt), parent=self)
        if msg:
            web = ipt
            self.master.destroy()
        else:
            self.master.lift()
            self.master.attributes('-topmost',True)
            self.master.after_idle(self.master.attributes,'-topmost',False)

    def addWeb(self):
        global web
        ipt = self.entry_web.get()
        if self.checkUrl(ipt):
            msg = messagebox.askokcancel("确认添加", "将搜索链接添加%s" % (ipt), parent=self)
        else:
            msg = messagebox.askokcancel("确认添加", "将搜索链接添加%s，链接好像不可用" % (ipt), parent=self)
        if msg:
            web_dict[ipt] = ipt
            self.lsb.insert(0,ipt)
        
    def list_write(self):
        item = self.lsb.get(self.lsb.curselection())
        if item == '':
            return
        global web
        msg = messagebox.askokcancel("确认修改", "将搜索链接修改为%s" % (item), parent=self)
        if msg:
            web = web_dict[item]
            self.master.destroy()
        else:
            self.master.lift()
            self.master.attributes('-topmost',True)
            self.master.after_idle(self.master.attributes,'-topmost',False)

    def list_write_del(self):
        item = self.lsb.get(self.lsb.curselection())
        if item == '':
            return
        global web_dict
        msg = messagebox.askokcancel("确认删除", "将从搜索链接列表删除%s" % (item), parent=self)
        if msg:
            del web_dict[item]
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
        global search_type
        search_type = 'random'
        self.button_right['command'] = self.addWeb
        self.button_random_web['text'] = '关闭随机搜索引擎'
        self.button_random_web['command'] = self.random_web_stop
        self.button_write['text'] = '删除'
        self.button_write['command'] = self.list_write_del
    
    def random_web_stop(self):
        global search_type
        search_type = 'single'
        self.button_write['text'] = '填入'
        self.button_write['command'] = self.list_write
        self.button_right['command'] = self.changeWeb
        self.button_random_web['text'] = '开启随机搜索引擎'
        self.button_random_web['command'] = self.random_web

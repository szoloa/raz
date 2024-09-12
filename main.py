import random
import webbrowser
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import tkinter.filedialog
import requests

f = open(r'.\data.txt', encoding='utf-8')
global theme
theme = f.readlines()

global web
web = 'https://search.bilibili.com/all?keyword=%s'

web_dict = {
    'bilibili': 'https://search.bilibili.com/all?keyword=%s',
    'Bing_CN' : 'https://cn.bing.com/search?q=%s',
    '抖音' : 'https://www.douyin.com/search/%s', 
    '百度' : 'https://www.baidu.com/s?wd=%s',
    '网易云音乐' : 'https://music.163.com/#/search/m/?s=%s',
    'X(twitter)' : 'https://x.com/search?q=%s',
    'PronHub' : 'https://pornhub.com/video/search?search=%s',
    'Yandex' : 'https://yandex.com/search/?text=%s',
}

def openWeb(theme):
    webbrowser.open(web % (theme))


# 更新搜索引擎
class inputW(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createFrame()

    def createFrame(self):
        self.v1 = StringVar()
        self.entry_web = Entry(self, textvariable=self.v1)
        
        self.button_right = Button(self, text='确定', command=self.changeWeb)
        
        self.lsb = Listbox(self) 
        for item in reversed(web_dict):
            self.lsb.insert(0,item)
        self.button_write = Button(self, text='填入', command=self.list_write)

        self.entry_web.pack()
        self.button_right.pack()
        self.lsb.pack()
        self.button_write.pack()

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
            self.master.after_idle(root.attributes,'-topmost',False)

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
            self.master.after_idle(root.attributes,'-topmost',False)
    
    def checkUrl(self, url, word='当你'):
        if '%s' not in url:
            return False
        r = requests.get(url % (word))
        result = r.status_code
        if (result == 200):
            return True
        else:
            return False

# 更新配置文件
class UserItem(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createFrame()

    def createFrame(self):
        self.button_userFile = Button(self, text='选择配置文件', command=self.userDo)
        self.lsb = Listbox(self) 

        self.entry_item = Entry(self)
        for i in theme[:20]:
            self.lsb.insert(0, i)

        self.button_add = Button(self, text='添加', command=self.addItem)
        self.button_del = Button(self, text='删除', command=self.delItem)
        self.button_delall = Button(self, text='清空', command=self.delAllItem)

        self.lsb.pack()
        self.button_userFile.pack()


        self.entry_item.pack()
        self.button_add.pack()
        self.button_del.pack()
        self.button_delall.pack()

    def userDo(self):
        path_ = tkinter.filedialog.askopenfilename()
        if path_ == '':
            return
        path_=path_.replace("/","\\\\")
        f = open(path_, encoding='utf-8')
        global theme
        theme = f.readlines()

        for i in theme[:20]:
            self.lsb.insert(0, i)

    def addItem(self):
        item = self.entry_item.get()
        if item == '':
            return
        theme.append(item)
        self.lsb.insert(0, item)
        self.entry_item.delete(0, END)

    def delItem(self):
        item = self.lsb.curselection()
        if self.lsb.get(item) in theme:
            theme.remove(self.lsb.get(item))
        self.lsb.delete(item)

    def delAllItem(self):
        global theme
        self.lsb.delete(0, END)
        theme.clear()

        
# 主程序
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

        self.button_rand_n = Button(self)
        self.button_rand_n['text'] = '仅随机而不跳转'
        self.button_rand_n['command'] = self.chioceThemeNotGo

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

        self.buttoon_changeWeb = Button(self, text='更改搜索引擎', command=self.changeWeb)

        # 历史记录
        self.lsb = Listbox(self) 
        
        self.button_rand.pack()
        self.button_rand_n.pack()
        self.button_goto.pack()
        #self.button_muti.pack()
        self.button_front.pack()
        self.button_userDo.pack()
        self.buttoon_changeWeb.pack()
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
    
    # 跳转
    def userDo(self):
        root_web = Tk()
        root_web.geometry("500x300+200+300")
        root_web.title("更改随机条目")
        # root_web.iconphoto(True, PhotoImage(file='logo.png'))
        UserItem(master=root_web) 
    
    # 跳转
    def changeWeb(self):
        root_web = Tk()
        root_web.geometry("500x300+200+300")
        root_web.title("更改搜索引擎")
        # root_web.iconphoto(True, PhotoImage(file='logo.png'))
        inputW(master=root_web)   
    
    def chioceThemeNotGo(self):
        chioce = random.choice(theme)
        messagebox.showinfo('结果', chioce)
        self.lsb.insert(0, chioce)

root = Tk()
root.geometry("500x300+100+200")
root.title("开启随机主题")
root.iconphoto(True, PhotoImage(file='logo.png'))

root.lift()
root.attributes('-topmost',True)
root.after_idle(root.attributes,'-topmost',False)

appliction(master=root)

root.mainloop()
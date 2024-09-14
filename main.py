import random
import webbrowser
from tkinter import Listbox
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import tkinter.filedialog
import requests
from tkinter import ttk
import sv_ttk
import darkdetect

f = open(r'.\data.txt', encoding='utf-8')
global theme
theme = f.readlines()
f.close()

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

global search_type
search_type = 'single'

def openWeb(theme):
    if search_type == 'random':
        rweb = random.choice(list(web_dict.values()))
    elif search_type == 'single':
        rweb = web
    webbrowser.open(rweb % (theme))

class BetaT(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createFrame()

    def createFrame(self):
        self.button_right = ttk.Button(self, text='开始',) # command=self.quickStart)
        self.button_right.pack()
        global isKilled
        isKilled = True

    # def quickStart(self):
    #     global isKilled
    #     if not isKilled:
    #         isKilled = True
    #     def runKey():
    #         def press(key):
    #             if key.char == "j":
    #                 chioce = random.choice(theme)
    #                 openWeb(chioce)
    #             return isKilled
    #         with keyboard.Listener(on_press = press) as listener:
    #             listener.join()
    #     self.thread_01 = Process(target=runKey)
    #     self.thread_01.start()
    #     self.button_right['text'] = '结束'
    #     self.button_right['command'] = self.quickStop

    # def quickStop(self):
    #     if self.thread_01.is_alive:
    #         global isKilled
    #         isKilled = False
    #         if not self.thread_01.is_alive:
    #             self.button_right['text'] = '开始'
    #             self.button_right['command'] = self.quickStart
        
# 更新搜索引擎
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
        self.button_write = ttk.Button(self, text='填入', command=self.list_write)
        
        global search_type
        if search_type == 'single':
            self.button_random_web = ttk.Button(self, text='开启随机搜索引擎', command=self.random_web)
            self.button_right = ttk.Button(self, text='确定', command=self.changeWeb)
        elif search_type == 'random':
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
            self.master.after_idle(root.attributes,'-topmost',False)

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
    
    def random_web(self):
        global search_type
        search_type = 'random'
        self.button_right['command'] = self.addWeb
        self.button_random_web['text'] = '关闭随机搜索引擎'
        self.button_random_web['command'] = self.random_web_stop
    
    def random_web_stop(self):
        global search_type
        search_type = 'single'
        self.button_right['command'] = self.changeWeb
        self.button_random_web['text'] = '开启随机搜索引擎'
        self.button_random_web['command'] = self.random_web


# 更新配置文件
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
        for i in theme[:40]:
            self.lsb.insert(0, i)


        self.button_add = ttk.Button(self, text='添加', command=self.addItem)
        self.button_del = ttk.Button(self, text='删除', command=self.delItem)
        self.button_delall = ttk.Button(self, text='清空', command=self.delAllItem)

        self.button_userFile.pack()
        self.label_tiem.pack()
        self.lsb.pack()
        
        self.entry_item.pack()
        self.button_add.pack()
        self.button_del.pack()
        self.button_delall.pack()

    def userDo(self):
        path_ = tkinter.filedialog.askopenfilename(
            title='请选择文件',
        filetypes=[('文本', '.txt .TXT')])

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
        style = ttk.Style()
        style.configure('TButton', font=("黑体", 11))
        self.button_rand = ttk.Button(self)
        self.button_rand['text'] = '随机'
        self.button_rand['width'] = 64
        self.button_rand['command'] = self.chioceTheme
        
        self.button_rand_n = ttk.Button(self)
        self.button_rand_n['text'] = '仅随机而不跳转'
        self.button_rand_n['width'] = 16
        self.button_rand_n['command'] = self.chioceThemeNotGo

        self.button_goto = ttk.Button(self)
        self.button_goto['text'] = '选择'
        self.button_goto['width'] = 64
        self.button_goto['command'] = self.openHistoryPage
        
        self.button_muti = ttk.Button(self)
        self.button_muti['text'] = '随机多个'
        self.button_muti['width'] = 6
        self.button_muti['command'] = self.openMuti

        self.button_front = ttk.Button(self)
        self.button_front['text'] = '置于最前'
        self.button_front['width'] = 10
        self.button_front['command'] = self.windFront

        self.button_userDo = ttk.Button(self)
        self.button_userDo['text'] = '自定义随机文件'
        self.button_userDo['width'] = 20
        self.button_userDo['command'] = self.userDo

        self.buttoon_changeWeb = ttk.Button(self, text='更改搜索引擎', command=self.changeWeb, width=16)

        self.buttoon_beta = ttk.Button(self, text='实验性功能', command=self.betaT, width=16)

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
        self.buttoon_beta.grid(row=5, column=0, padx=4, pady=4, columnspan=4)

    def chioceTheme(self, *args):
        chioce = random.choice(theme)
        openWeb(chioce)
        self.__saveResult(chioce)

    
    def openHistoryPage(self, *args):
        temp = self.lsb.get(self.lsb.curselection())
        if temp == '':
            return
        openWeb(temp)
    
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
        root_web.geometry("500x400+200+300")
        root_web.title("更改随机条目")
        # root_web.iconphoto(True, PhotoImage(file='logo.png'))
        UserItem(master=root_web) 
    
    # 跳转
    def changeWeb(self):
        root_web = Tk()
        root_web.geometry("500x400+200+300")
        root_web.title("更改搜索引擎")
        # root_web.iconphoto(True, PhotoImage(file='logo.png'))
        inputW(master=root_web)   
    
    def chioceThemeNotGo(self):
        chioce = random.choice(theme)
        messagebox.showinfo('结果', chioce)
        self.__saveResult(chioce)
        
    def __saveResult(self, chioce):
        self.lsb.insert(0, chioce)
        with open(r'./hostory.txt', 'a+', encoding='utf-8') as f:
            f.writelines(chioce)

    def betaT(self):
        root_web = Tk()
        root_web.geometry("500x400+200+300")
        root_web.title("实验性功能")
        # root_web.iconphoto(True, PhotoImage(file='logo.png'))
        BetaT(master=root_web) 

root = tk.Tk()

sv_ttk.set_theme(darkdetect.theme())

root.resizable(False, False)
root.geometry("640x350+200+200")
root.title("开启随机主题")
root.iconphoto(True, PhotoImage(file='logo.png'))

root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)

appliction(master=root)

def on_closing():
    if messagebox.askokcancel("退出", "是否要退出程序？"):
        root.quit()
        root.destroy()
        quit()

root.protocol('WM_DELETE_WINDOW', on_closing)

root.mainloop()
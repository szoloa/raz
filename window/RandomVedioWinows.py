import tkinter
import threading
from tkinter import messagebox
from .randomVedio import vedioSpider
from .custom import custom
import os

class RandomVedioWinows(tkinter.Frame):
    def __init__(self, theme, master=None, bro=None):
        super().__init__(master)
        self.master = master
        self.bro = bro
        self.pack()
        self.createFrame()
        self.Theme = theme
        
        # 创建一个事件来检测 vedioSpider 的完成状态
        self.finished_event = threading.Event()

        # 启动 vedioSpider 的新线程
        self.start_vedio_spider(theme)

    def createFrame(self):
        # 创建一个 Text 小部件用于显示内容
        self.text = tkinter.Text(self, wrap="word", height=160, width=500)
        self.text.pack()

    def start_vedio_spider(self, theme):
        # 创建一个新线程来运行 vedioSpider
        thread = threading.Thread(target=self.run_vedio_spider, args=(theme,))
        thread.daemon = True  # 设置为守护线程，在主程序退出时自动结束
        thread.start()

        # 使用 after 定时检查任务是否完成
        self.check_if_finished()

    def run_vedio_spider(self, theme):
        # 启动 vedioSpider 并传递 self.update 作为回调函数
        vedioSpider(theme, handle=self.update)
        # 任务完成后设置事件
        self.finished_event.set()

    def update(self, text):
        self.text.after(0, self._update_text, text)

    def _update_text(self, text):
        # 插入新文本
        self.text.insert(tkinter.END, text)
        self.text.see(tkinter.END)  # 自动滚动到底部

        # 限制文本行数
        max_lines = 40  # 最大行数限制
        current_lines = int(self.text.index('end-1c').split('.')[0])  # 获取当前行数

        if current_lines > max_lines:
            self.text.delete("1.0", f"{current_lines - max_lines}.0")  # 删除多余行


    def check_if_finished(self):
        # 检查 vedioSpider 是否完成
        if self.finished_event.is_set():
            # 弹出消息框并关闭窗口
            messagebox.showinfo("完成", "深入探索 已完成任务")
            custom.set_Item(['./data/%s' %(i) for i in os.listdir('./data')])
            custom.set_search_type_s('url')
            self.bro.label_web['text'] = '当前搜索引擎: %s' %(custom.get_search_type_s())
            f = open('./data/%s.txt' %(self.Theme))
            custom.set_theme([i.replace('\n','').replace('\r','') for i in f.readlines()])
            f.close()
            self.master.destroy()  # 关闭主窗口
        else:
            # 如果未完成，继续检查
            self.after(500, self.check_if_finished)


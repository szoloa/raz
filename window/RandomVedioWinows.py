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
        self.finished_event = threading.Event()
        self.start_vedio_spider(theme)

    def createFrame(self):
        self.text = tkinter.Text(self, wrap="word", height=160, width=500)
        self.text.pack()

    def start_vedio_spider(self, theme):
        thread = threading.Thread(target=self.run_vedio_spider, args=(theme,))
        thread.daemon = True
        thread.start()
        self.check_if_finished()

    def run_vedio_spider(self, theme):
        vedioSpider(theme, handle=self.update)
        self.finished_event.set()

    def update(self, text):
        self.text.after(0, self._update_text, text)

    def _update_text(self, text):
        self.text.delete('0.0', tkinter.END)
        self.text.insert(tkinter.END, text)
        self.text.see(tkinter.END)  # 自动滚动到底部


    def check_if_finished(self):
        if self.finished_event.is_set():
            messagebox.showinfo("完成", "深入探索 已完成任务")
            custom.set_Item(['./data/%s' %(i) for i in os.listdir('./data')])
            custom.set_search_type_s('url')
            self.bro.label_web['text'] = '当前搜索引擎: %s' %(custom.get_search_type_s())
            f = open('./data/%s.txt' %(self.Theme))
            custom.set_theme([i.replace('\n','').replace('\r','') for i in f.readlines()])
            f.close()
            self.master.destroy()
        else:
            self.after(500, self.check_if_finished)


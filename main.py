from window.custom import *
from window.Appliction import appliction
import tkinter as tk
import sv_ttk
import darkdetect
from tkinter import messagebox, PhotoImage

# 主程序
root = tk.Tk()

w = custom.get_width()
h = custom.get_height()

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
# 计算 x, y 位置
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

sv_ttk.set_theme(darkdetect.theme())

root.resizable(False, False)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.title("开启随机主题")
root.iconphoto(True, PhotoImage(file='logo.png'))

root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)

appliction(master=root)

def on_closing():
    if messagebox.askokcancel("退出", "是否要退出程序？"):
        root.lift()
        root.attributes('-topmost', True)
        root.quit()
        root.destroy()
root.protocol('WM_DELETE_WINDOW', on_closing)

if __name__ == '__main__':
    root.mainloop()
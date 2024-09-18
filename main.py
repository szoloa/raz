from window.custom import *
from window.Appliction import appliction
import tkinter as tk
import sv_ttk
import darkdetect
from tkinter import messagebox, PhotoImage

# 主程序
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
        root.lift()
        root.attributes('-topmost', True)
        root.quit()
        root.destroy()
        quit()
root.protocol('WM_DELETE_WINDOW', on_closing)

root.mainloop()
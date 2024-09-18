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
from os import listdir as os_listdir
import json

f = open(r'.\data\data.txt', encoding='utf-8')
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
    'YouTuBe':'https://www.youtube.com/results?search_query=%s',
}

global search_type
search_type = 'single'

def openWeb(theme):
    if search_type == 'random':
        rweb = random.choice(list(web_dict.values()))
    elif search_type == 'single':
        rweb = web
    webbrowser.open(rweb % (theme))

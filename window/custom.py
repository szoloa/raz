import random
import webbrowser
import os
import json
from translate import Translator
import threading


opti = False
if opti:
    from .optional import Translator
else:
    from translate import Translator


# 作为全局变量
class Custom():
    def __init__(self) -> None:
        f = open(r'./data/data.txt', encoding='utf-8')
        self.__theme = f.readlines()
        f.close()

        self.__item_user = ['./data/%s' %(i) for i in os.listdir('./data')]

        self.__web = 'https://search.bilibili.com/all?keyword=%s'

        self.__language = 0

        if os.path.exists('./web.json'):
            with open('./web.json', 'r') as f:
                self.__web_dict = json.loads(f.read())
        else:
            self.__web_dict = {
                'bilibili': 'https://search.bilibili.com/all?keyword=%s',
                'Bing_CN' : 'https://cn.bing.com/search?q=%s',
                '抖音' : 'https://www.douyin.com/search/%s', 
                '百度' : 'https://www.baidu.com/s?wd=%s',
                '网易云音乐' : 'https://music.163.com/#/search/m/?s=%s',
                'X(twitter)' : 'https://x.com/search?q=%s',
                'PronHub' : 'https://pornhub.com/video/search?search=%s',
                'Yandex' : 'https://yandex.com/search/?text=%s',
                'YouTuBe' : 'https://www.youtube.com/results?search_query=%s',
                'Google' : 'https://www.google.com.hk/search?q=%s',
                '淘宝' : 'https://ai.taobao.com/search/index.htm?key=%s',
            }
        self.__search_type = 'single'
        self.__search_type_s = 'theme'

    def handle_theme(self, theme_ipt, callback, obj):
        if self.__language == 0:
                theme = theme_ipt
                callback(theme)
        def Translate():       
            try:
                
                if self.__language == 1:
                    theme = Translator(from_lang="Chinese", to_lang="English").translate(theme_ipt)
                elif self.__language == 2:
                    theme = Translator(from_lang="English", to_lang="Chinese").translate(theme_ipt)
                elif self.__language == 3:
                    theme = Translator(from_lang="Chinese", to_lang="Japanese").translate(theme_ipt)
            except Exception as e:
                theme = theme_ipt
                print(f"Translation error: {e}")
            callback(theme)
            obj.after(0, obj.upUiGoto())
        thread_trans = threading.Thread(target=Translate)
        thread_trans.start()

    def __openWeb(self, theme_ipt):
        
        theme = theme_ipt

        if self.__search_type == 'random':
            rweb = random.choice(list(self.__web_dict.values()))
            webbrowser.open(rweb % (theme))
        elif self.__search_type == 'single':
            if self.__search_type_s == 'theme':
                rweb = self.__web
                webbrowser.open(rweb % (theme))
            elif self.__search_type_s == 'url':
                webbrowser.open(theme)

    def openWeb(self, theme_ipt, obj = None):
        self.handle_theme(theme_ipt, self.__openWeb, obj)

    def get_Item(self):
        return self.__item_user
    def set_Item(self, item):
        self.__item_user = item

    def get_theme(self):
        return self.__theme
    def set_theme(self, theme_s):
        self.__theme = theme_s

    def get_web(self):
        return self.__web
    def set_web(self, web_s):
        self.__web = web_s
    def get_web_name(self):
        if self.__web in self.__web_dict.values():
            return [k for k, v in self.__web_dict.items() if v == self.__web][0]
        return self.__web

    def get_search_type(self):
        return self.__search_type
    def set_search_type(self, search_typle_s):
        self.__search_type = search_typle_s

    def get_web_dict(self):
        return self.__web_dict
    def set_web_dict(self, web_dict_s):
        self.__web_dict = web_dict_s

    def get_search_type_s(self):
        return self.__search_type_s
    def set_search_type_s(self, search_typle_s_t):
        self.__search_type_s = search_typle_s_t

    def get_language(self):
        return self.__language
    def set_language(self, language_t):
        self.__language = language_t

global listener_v
listener_v = None

custom = Custom()
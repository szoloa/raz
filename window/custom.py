import random
import webbrowser
import os
import json

# 作为全局变量
class Custom():
    def __init__(self) -> None:
        f = open(r'./data/data.txt', encoding='utf-8')
        self.__theme = f.readlines()
        f.close()

        self.__item_user = ['./data/%s' %(i) for i in os.listdir('./data')]

        self.__web = 'https://search.bilibili.com/all?keyword=%s'

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
                'YouTuBe':'https://www.youtube.com/results?search_query=%s',
            }
        self.__search_type = 'single'

    def openWeb(self, theme):
        if self.__search_type == 'random':
            rweb = random.choice(list(self.__web_dict.values()))
        elif self.__search_type == 'single':
            rweb = self.__web
        webbrowser.open(rweb % (theme))

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

global listener_v
listener_v = None

custom = Custom()
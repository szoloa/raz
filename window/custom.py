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

class chioce:
    def __init__(self, content, type='theme'):
        self.content = content
        if content[:5] == 'JSON:':
            temj = json.loads(content[6:])
            self.text = temj['text']
            if type == 'url':
                self.url = temj['url']
            else:
                self.url = temj['text']
        else:
            self.text = content
            self.url = content
    def __str__(self):
        return self.content

# 作为全局变量
class Custom():
    def __init__(self) -> None:
        f = open(r'./data/data.txt', encoding='utf-8')
        self.__theme = [i.replace('\n','').replace('\r','') for i in f.readlines()]
        f.close()
        
        self.__item_user = ['./data/%s' %(i) for i in os.listdir('./data')]

        self.__web = 'https://search.bilibili.com/all?keyword=%s'

        self.__language = 0

        self.__search_type = 'single'
        self.__search_type_s = 'theme'

        self.__width = 840
        self.__height = 500

        fs = open('setting.json', 'a')
        try:
            setting_user = json.loads(fs.read())
        except:
            setting_user = {
            'item_user' : self.__item_user, 
            'web': self.__web, 
            'language' : self.__language,
            'search_type' : self.__search_type,
            'search_type_s' : self.__search_type_s,
            'width' : self.__width,
            'height' : self.__height,
            'theme' : self.__theme
        }
        fs.close()

        if 'item_user' in setting_user.keys(): 
            self.__item_user = setting_user['item_user']
        if 'web' in setting_user.keys(): 
            self.__web = setting_user['web']
        if 'language' in setting_user.keys(): 
            self.__language = setting_user['language']
        if 'search_type' in setting_user.keys(): 
            self.__search_type = setting_user['search_type']
        if 'search_type_s' in setting_user.keys(): 
            self.__search_type_s = setting_user['search_type_s']
        if 'width' in setting_user.keys(): 
            self.__width = setting_user['width']
        if 'height' in setting_user.keys():
            self.__height = setting_user['height']
        if 'theme' in setting_user.keys():
            self.__theme = setting_user['theme']

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
                '小红书' : 'https://www.xiaohongshu.com/search_result?keyword=%s',
                '微博' : 'https://s.weibo.com/weibo?q=%s',
                '知乎' : 'https://www.zhihu.com/search?type=content&q=%s',
                '百度百科' : 'https://baike.baidu.com/item/%s',
                'Wikipedia' : 'https://zh.wikipedia.org/wiki/%s',
            }
        
    def handle_theme(self, theme_ipt, obj):
        if self.__language == 0:
                theme = theme_ipt
                self.__openWeb(theme)
        else:
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
                self.__openWeb(theme)
                obj.after(0, obj.upUiGoto())
            thread_trans = threading.Thread(target=Translate)
            thread_trans.start()

    def __openWeb(self, theme):
        if self.__search_type_s == 'url':
                webbrowser.open(theme)
        elif self.__search_type == 'random':
            rweb = random.choice(list(self.__web_dict.values()))
            webbrowser.open(rweb % (theme))
        elif self.__search_type == 'single':
            if self.__search_type_s == 'theme':
                rweb = self.__web
                webbrowser.open(rweb % (theme))
            

    def openWeb(self, theme_ipt, obj = None):
        self.handle_theme(theme_ipt, obj)

    def save_setting(self):
        f = open('setting.json', 'w')

        setting_user = {
            'item_user' : self.__item_user, 
            'web': self.__web, 
            'language' : self.__language,
            'search_type' : self.__search_type,
            'search_type_s' : self.__search_type_s,
            'width' : self.__width,
            'height' : self.__height,
            'theme' : self.__theme
        }

        f.write(json.dumps(setting_user))
        f.close()
        
    def get_Item(self):
        return self.__item_user
    def set_Item(self, item):
        self.__item_user = item

    def get_theme(self):
        chi = random.choice(self.__theme)
        tempchi = chioce(chi, self.__search_type_s)
        return tempchi
    def get_theme_list(self):
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

    def get_width(self):
        return self.__width
    def set_width(self, w):
        self.__width = w
    def get_height(self):
        return self.__height
    def set_height(self, h):
        self.__height = h

global listener_v
listener_v = None

custom = Custom()

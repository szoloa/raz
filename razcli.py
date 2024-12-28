from window.custom import custom
import sys 
import getopt

custom.set_web(custom.get_web_dict()['小红书'])

custom.set_search_type_s('theme')

f = open(r'./data/默认.txt', encoding='utf-8')
custom.set_theme([i.replace('\n','').replace('\r','') for i in f.readlines()])
f.close()

chioce = custom.get_theme()
print(chioce)

custom.openWeb(chioce.url)

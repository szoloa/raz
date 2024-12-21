import json

class chioce:
    def __init__(self, content, type='theme'):
        self.content = content
        temj = json.loads(content)
        self.text = temj['text']
        self.url = temj['url']
    def __str__(self):
        return self.content

f = open(r'单曲循环_2023_2020.txt', encoding='utf-8')
line = [i.replace('\n','').replace('\r','')[5:] for i in f.readlines()]
f.close()

f = open('rurl_2023.txt','a+',encoding='utf-8')

for i in line:
    try:
        tempchi = chioce(i)
    except Exception as e:
        print(e, i)
        continue
    print(tempchi.url)
    f.writelines(tempchi.url+'\n')
f.close()
import jieba.analyse

#jieba.enable_paddle()

filepath = './outputfile.txt'
f = open(filepath, 'a+', encoding='utf-8')
themeList = f.readlines()

ipt = input()

ipt = jieba.analyse.extract_tags(ipt, allowPOS=('ns', 'n', 'vn', 'v'))
for i in ipt:
    if i in themeList:
        pass
    elif i == '':
        pass
    elif i in r'''。？！，%；：,./?';:-=+&*@#        \n''' :
        pass
    elif i == '\n':
        pass
    else:
        print(i)
        f.writelines(i+'\n')
f.close()
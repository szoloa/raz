import jieba.analyse

#jieba.enable_paddle()

filepath = './outputfile.txt'
f = open(filepath, 'a+', encoding='utf-8')
themeList = f.readlines()

ipt = '''每一个早晨都是一个愉快的邀请，使得我的生活跟大自然自己同样地简单，也许我可以说，同样地纯洁无暇。我向曙光顶礼，忠诚如同希腊人。我起身很早，在湖中洗澡；这是个宗教意味的运动，我所做到的最好的一件事。据说在成汤王的浴盆上就刻着这样的字：“苟日新，日日新，又日新。”我懂得这个道理。黎明带国来了英雄时代。在最早的黎明中，我坐着，门窗大开，一只看不到也想象不到的蚊虫在我的房中飞，它那微弱的吟声都能感动我，就像我听到了宣扬美名的金属喇叭声一样。这是荷马的一首安魂曲，空中的《伊利亚特》和《奥德赛》，歌唱着它的愤怒与漂泊。此中大有宇宙本体之感；宣告着世界的无穷精力与生生不息，直到它被禁。黎明啊，一天之中最值得纪念的时节，是觉醒的时辰。那时候，我们的昏沉欲睡的感觉是最少的了；至少可有一小时之久，整日夜昏昏沉沉的官能大都要清醒起来。但是，如果我们并不是给我们自己的禀赋所唤醒，而是给什么仆人机械地用肘子推醒的；如果并不是由我们内心的新生力量和内心的要求来唤醒我们，既没有那空中的芬香，也没有回荡的天籁的音乐，而是工厂的汽笛唤醒了我们的，――如果我们醒时，并没有比睡前有了更崇高的生命，那末这样的白天，即便能称之为白天，也不会有什么希望可言；要知道，黑暗可以产生这样的好果子，黑暗是可以证明它自己的功能并不下于白昼的。一个人如果不能相信每一天都有一个比他亵读过的更早、更神圣的曙光时辰，他一定是已经对于生命失望的了，正在摸索着一条降入黑暗去的道路。感官的生活在休息了一夜之后，人的灵魂，或者就说是人的官能吧，每天都重新精力弥漫一次，而他的禀赋又可以去试探他能完成何等崇高的生活了。
        
        '''

for ij in ipt.split('。'):
    print(ij)
    ij = jieba.analyse.extract_tags(ij, allowPOS=('n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng',))
    for j in ij:
        if j in themeList:
            pass
        elif j == '':
            pass
        elif j in r'''。？！，%；：,./?';:-=+&*@#        \n''' :
            pass
        elif j == '\n':
            pass
        else:
            print(j)
            f.writelines(j+'\n')
f.close()
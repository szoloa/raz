#!/usr/bin/python

import random

f = open(r'/home/szoloa/temp/raz/data/默认.txt', encoding='utf-8')
theme = [i.replace('\n','').replace('\r','') for i in f.readlines()]
f.close()

print(random.choice(theme))

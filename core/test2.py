# -*- coding: utf-8 -*-
import os
import time

t = os.path.getmtime('C:\\Users\\Drock\\Desktop\\aa\\test1.fbx')
print(t)
print(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(t)))

a = u'aa中文'
# b = a.decode("utf-8").encode("utf-8")
print(a)

aa = ['cc', 'dd', 'ee']
bb = aa.index('dd')
print(bb)

cc = range(10)
print(cc)

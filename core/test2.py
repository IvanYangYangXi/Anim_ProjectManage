# -*- coding: utf-8 -*-
a = 'aa中文'
b = a.decode("utf-8").encode("utf-8")
print(b)

aa = ['cc','dd','ee']
bb = aa.index('dd')
print(bb)
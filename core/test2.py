# -*- coding: utf-8 -*-
import os

dire = {
            u"'模型','贴图'":'SM_',
            'SK_':[u'绑定', u'融合变形']
        }
print(dire.keys())


a = 'aa中文'
b = a.decode("utf-8").encode("utf-8")
print(b)

aa = ['cc', 'dd', 'ee']
bb = aa.index('dd')
print(bb)

cc = range(10)
print(cc)

# -*- coding: utf-8 -*-
a = '0, 1, 2, 3'
b = a.split(',')
c = []
for i in b:
    # if str.isdigit(i):  # 判断是否为正整数
    c.append(int(i))
print('"%s"'%str(c)[1:-1])

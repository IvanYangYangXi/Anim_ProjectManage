# -*- coding: utf-8 -*-


str1='\u5927\u592b'
str2 = str1.encode('utf-8').decode('unicode-escape')

print(str2)
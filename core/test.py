#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test.py
# @Author :  ()
# @Link   : 
# @Date   : 7/11/2019, 11:08:15 AM




#QLineEdit控件使用
import sys
from  PyQt5.QtWidgets import QPushButton,QApplication,QMainWindow,QLineEdit,QFormLayout,QWidget,QLabel
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QRegExpValidator
from PyQt5.QtCore import  QRegExp
class QLineEditDemo(QWidget):
    def __init__(self,parent=None):
        super(QLineEditDemo,self).__init__(parent)

        self.setWindowTitle("QLineEdit控件使用格式校验")
        self.resize(500,600)
        self.formLayout=QFormLayout()

        edit_int=QLineEdit()
        edit_int.setPlaceholderText("请输入整数！")
        #设置获取焦点
        edit_int.setFocus()

        edit_float=QLineEdit()
        edit_float.setPlaceholderText("请输入浮点数！")

        edit_chars= QLineEdit()
        edit_chars.setPlaceholderText("请输入指定格式字符！")


        self.formLayout.addRow("整数",edit_int)
        self.formLayout.addRow("浮点型",edit_float)
        self.formLayout.addRow("指定格式字符串", edit_chars)
        #格式校验
        intValidator=QIntValidator(self)
        intValidator.setRange(1,200)

        doubleValidator=QDoubleValidator(self)
        doubleValidator.setRange(-300,300)
        doubleValidator.setNotation(QDoubleValidator.StandardNotation)
        doubleValidator.setDecimals(2)

        reg=QRegExp("[a-zA-Z]{6,8}")
        cValidator=QRegExpValidator(self)
        cValidator.setRegExp(reg)

        edit_int.setValidator(intValidator)
        edit_float.setValidator(doubleValidator)
        edit_chars.setValidator(cValidator)

        self.setLayout(self.formLayout)



if __name__=="__main__":
    app=QApplication(sys.argv)
    win=QLineEditDemo()
    win.show()
    sys.exit(app.exec_())
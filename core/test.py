#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test.py
# @Author :  ()
# @Link   : 
# @Date   : 7/11/2019, 11:08:15 AM




import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt


class Demo(QWidget):

    def __init__(self):
        super(Demo, self).__init__()
        self.label = QLabel('Hello World', self)
        self.label1 = QLabel('喂  世界', self)
        self.label1.move(0, 30)
        self.label2 = QLabel('鼠标位置', self)
        self.resize(500, 300)
        self.label.resize(200, 20)
        self.label1.resize(200, 20)
        self.label2.resize(400, 20)
        self.label2.move(0, 60)
        self.label3 = QLabel('鼠标位置', self)
        self.label3.resize(400, 20)
        self.label3.move(0, 90)

        self.setMouseTracking(True)  # 设置鼠标移动跟踪是否有效
        '''
        设置为True时，只要鼠标在窗口内移动时mouseMoveEvent事件就能捕获
        设置为False时（默认），只有鼠标键按下并在窗口内移动时mouseMoveEvent事件才能捕获
        注意只能是QWidget，如果是QMainwindow，则无效
        self.hasMouseTracking()返回设置的状态
        '''

    def mousePressEvent(self, event):  # 鼠标键按下时调用(任意一个键,按一下调一次)，这些方法是许多控件自带的，这里来自于QWidget。
        self.label.setText('鼠标键按下了')
        n = event.button()  # 用来判断是哪个鼠标健触发了事件【返回值：0  1  2  4】
        '''
        QtCore.Qt.NoButton - 0 - 没有按下鼠标键
        QtCore.Qt.LeftButton -1 -按下鼠标左键
        QtCore.Qt.RightButton -2 -按下鼠标右键
        QtCore.Qt.Mion 或 QtCore.Qt.MiddleButton -4 -按下鼠标中键
        '''
        nn = event.buttons()  # 返回前面所列枚举值的组合，用于判断同时按下了哪些键【不知怎么判断】  <PyQt5.QtCore.Qt.MouseButtons object at 0x0000003326982F98>

    def mouseReleaseEvent(self, event):  #鼠标键释放时调用  
        #参数1：鼠标的作用对象；参数2：鼠标事件对象，用来保存鼠标数据
        self.label.setText('鼠标键放开了')

    def mouseMoveEvent(self, event):  # 鼠标移动事件
        ret = self.hasMouseTracking()  #返回鼠标MouseTracking的状态
        self.label1.setText('鼠标移动了:%s' % ret)
        x = event.x()  # 返回鼠标相对于窗口的x轴坐标
        y = event.y()  # 返回鼠标相对于窗口的y轴坐标
        self.label2.setText('鼠标x坐标：%s  ,鼠标y坐标：%s' % (x, y))
        xy = event.pos()  #返回鼠标坐标 ，QPoint(463, 0) 相对于控件  【用xy.x()  xy.y()提取值】
        s=event.localPos()  #返回鼠标坐标  相对于控件   QPointF(2.0, 2.0)

        s = self.mapToGlobal(xy)  # 将窗口坐标转换成屏幕坐标.属于QWidget类的方法；参数类型QPoint
        self.label3.setText('鼠标x坐标：%s  ,鼠标y坐标：%s' % (xy.x(), xy.y()))
        xy1 = event.globalPos()  # 返回鼠标相对于屏幕的坐标。PyQt5.QtCore.QPoint(1096, 37)【用xy1.x()  xy1.y()提取值】
        s1 = self.mapFromGlobal(xy1)  #将屏幕坐标转换成窗口坐标.属于QWidget类的方法；参数类型QPoint
        # mapToParent(QPoint) - 将窗口坐标转换成父窗口坐标。如果没有父窗口，则相当于mapToGlobal (QPoint)
        # mapFromParent(QPoint) - 将父窗口坐标转换成窗口坐标。如果没有父窗口，则相当于mapFromGlobal(QPoint)
        # mapTo (QWidget, QPoint) - 将窗口坐标转换成 QWidget父窗口坐标
        px = event.globalX()  # 返回相对于屏幕的x坐标
        py = event.globalY()  # 返回相对于屏幕的y坐标
        s = event.windowPos()  # 相对于窗口的坐标(保留一位小数)，PyQt5.QtCore.QPointF(481.0, 1.0)【用s.x()  s.y()提取值】
        p = event.screenPos()  # 相对于屏幕的坐标(保留一位小数).PyQt5.QtCore.QPointF(476.0, 49.0)【用p.x()  p.y()提取值】
        t = event.timestamp()  # 返回事件发生的时间。【以程序运行开始计时，以毫秒为单位】

    def mouseDoubleClickEvent(self, event):  # 鼠标双击时调用
        self.label1.setText('双击了鼠标')
        '''双击时的事件顺序如下:
            MouseButtonPress
            MouseButtonRelease
            MouseButtonDblClick
            MouseButtonPress
            MouseButtonRelease
            QApplicaption类的setDoubleClickInterval( )方法可设置双击的时间间隔；doubleClickInterval( )方法返回双击的时间间隔。'''

    def enterEvent(self, event):  # 鼠标移进时调用
        print('鼠标移进窗口了')
        self.setCursor(Qt.CrossCursor)  # 设置鼠标形状。
        # 需要from PyQt5.QtGui import QCursor,from PyQt5.QtCore import Qt
        # #鼠标形状对照图见下方
        # self.unsetCursor()   #鼠标恢复系统默认

    def leaveEvent(self, event):  # 鼠标移出时调用
        print('鼠标移出窗口了')

    def wheelEvent(self, event):  # 滚轮滚动时调用。event是一个QWheelEvent对象
        angle = event.angleDelta()  # 返回滚轮转过的数值，单位为1/8度.PyQt5.QtCore.QPoint(0, 120)
        angle = angle / 8  # 除以8之后单位为度。PyQt5.QtCore.QPoint(0, 15)   【向前滚是正数，向后滚是负数  用angle.y()取值】
        ang = event.pixelDelta()  # 返回滚轮转过的像素值  【不知为何  没有值】
        # print(event.x(),event.y())    #返回鼠标相对于窗口的坐标
        w = event.pos()  # 返回相对于控件的当前鼠标位置.PyQt5.QtCore.QPoint(260, 173)
        w1 = event.posF()  # 返回相对于控件的当前鼠标位置.PyQt5.QtCore.QPointF(302.0, 108.0)
        # 坐标函数与上面相同


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec())
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# treeModels.py
# @Author :  ()
# @Link   : 
# @Date   : 7/10/2019, 2:58:31 PM


import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class TreeItemBase(object):
    def __init__(self, data, parent=None):
        super(TreeItemBase, self).__init__()
        
        self._parentItem = parent
        self._childItems = []
        self._itemData = data

        if parent:
            parent.appendChild(self)
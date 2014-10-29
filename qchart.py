#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from PyQt4 import QtGui, QtCore

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
# #######1#########2#########3#########4#########5#########6#########7#########


class Canvas(FigureCanvasQTAgg):
    def __init__(self, parent, *args):
        super(self.__class__, self).__init__(matplotlib.figure.Figure())
        self.setParent(parent)
        self.figure.patch.set_facecolor("#FFFFFF")
#        self.figure.patch.set_alpha(0.1)
#        self.figure.hold(False)
        self.axes = self.figure.add_subplot(1, 1, 1)
#        self.axes.patch.set_alpha(0.1)
#        self.axes.hold(True)
#        self.axes.get_xaxis().set_visible(False)
#        self.axes.get_yaxis().set_visible(False)
        self.setParent(parent)
        self.setMinimumSize(150, 160)
#        self.setMaximumSize(200, 240)

    def clear_(self):
        self.axes.clear()
        self.draw()

    def save(self, file_, *args, **kwargs):
        return self.print_png(file_, *args, **kwargs)

    def plot_(self, x, y):
        self.axes.plot(x, y, color="#000000")

    def set_xlim(self, duration):
        self.axes.set_autoscalex_on(False)
        self.axes.set_xlim(1, duration)
        self.draw()
        return


class Chart(QtGui.QWidget):
    def __init__(self, parent):
        super(self.__class__, self).__init__(None)
        self.main = QtGui.QLabel('Chart.title')
        self.main.setAlignment(QtCore.Qt.AlignHCenter)
        self._summary = Summary(None)
        self._canvas = Canvas(parent)
        self.xlab = QtGui.QLabel('Chart.xlab')
        self.xlab.setAlignment(QtCore.Qt.AlignHCenter)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.main)
        layout.addWidget(self._summary)
        layout.addWidget(self._canvas)
        layout.addWidget(self.xlab)
        layout.setSpacing(0)
        layout.setMargin(0)
#        self.setMaximumHeight(180)

    @property
    def canvas(self):
        return self._canvas

    @property
    def summary(self):
        return self._summary


class LabeledLCD(QtGui.QWidget):
    def __init__(self, num_digits):
        super(self.__class__, self).__init__(None)
        layout = QtGui.QVBoxLayout(self)

        self.label = QtGui.QLabel('LabeldLCD', self)
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        layout.addWidget(self.label)
#        self._lcd = QtGui.QLCDNumber(num_digits, self)
#        self.display = self._lcd.display
#        layout.addWidget(self._lcd)

        value = QtGui.QLabel("0", self)
        value.setAlignment(QtCore.Qt.AlignHCenter)
        layout.addWidget(value)
        self.display = value.setNum


class Summary(QtGui.QWidget):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        layout = QtGui.QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self._min = LabeledLCD(2)
        self._mean = LabeledLCD(4)
        self._max = LabeledLCD(2)
        layout.addWidget(self._min)
        layout.addWidget(self._mean)
        layout.addWidget(self._max)

    def display(self, mean_, min_, max_):
        self._min.display(round(min_, 1))
        self._mean.display(round(mean_, 1))
        self._max.display(round(max_, 1))

    def retr(self):
        self._min.label.setText(self.tr("Min"))
        self._mean.label.setText(self.tr("Mean"))
        self._max.label.setText(self.tr("Max"))

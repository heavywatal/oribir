#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from PyQt4 import QtGui, QtCore


class LineEdit(QtGui.QLineEdit):
    def __init__(self, arg=None, parent=None):
        if not arg or isinstance(arg, QtGui.QWidget):
            super(LineEdit, self).__init__(arg or parent)
        else:
            self._class = arg.__class__
            super(LineEdit, self).__init__(str(arg), parent)
        self.setMinimumWidth(60)
        self.setMaximumWidth(80)

    def get(self):
        return self._class(self.text())  # TODO exception


class SliderLayout(QtGui.QHBoxLayout):
    def __init__(self, master, min_, max_, step, value=None):
        super(self.__class__, self).__init__(master)

        self.value_class = value.__class__
        self.value = QtGui.QLabel(str(value), master)
        self.value.setMinimumWidth(40)

        slider = QtGui.QSlider(QtCore.Qt.Horizontal, master)
        slider.setRange(min_, max_)
        slider.setSingleStep(step)
        slider.setTickInterval(step)
        slider.setValue(value)
        slider.valueChanged.connect(self.value.setNum)

        self.addWidget(slider)
        self.addWidget(self.value)

    def get(self):
        return self.value_class(self.value.text())


class SpinBox(QtGui.QSpinBox):
    def __init__(self, master, min_, max_, step, value):
        super(self.__class__, self).__init__(master)
        self.setRange(min_, max_)
        self.setSingleStep(step)
        self.setValue(value)
        self.setMinimumWidth(80)


class ComboBox(QtGui.QComboBox):
    def __init__(self, master, idx=1):
        super(self.__class__, self).__init__(master)
        for i in range(3):
            self.addItem('')
        self.setCurrentIndex(idx)
        self.retr()

    def setReadOnly(self, read_only=True):
        return self.setDisabled(read_only)

    def retr(self):
        self.setItemText(0, self.tr("Rich"))
        self.setItemText(1, self.tr("Medium"))
        self.setItemText(2, self.tr("Poor"))


class DoubleSpinBox(QtGui.QDoubleSpinBox):
    def __init__(self, master, min_, max_, step, value):
        super(self.__class__, self).__init__(master)
        self.setRange(min_, max_)
        self.setSingleStep(step)
        self.setValue(value)
        self.setMinimumWidth(80)
        self.setDecimals(3)


def ParamsGroupBox_env_gen_func():
    yield 2
    yield 0


class ParamsGroupBox(QtGui.QGroupBox, object):
    unlocked = QtCore.pyqtSignal(bool)
    locked = QtCore.pyqtSignal(bool)
    initial_env_gen = ParamsGroupBox_env_gen_func()

    def __init__(self, master=None):
        QtGui.QGroupBox.__init__(self, master)

        self._params = dict()
        self._params["environment"] = ComboBox(
            master, next(self.__class__.initial_env_gen))
        self._params["mutation_rate"] = DoubleSpinBox(
            master, 1e-3, 1e-1, 1e-3, 1e-2)
        self._params["pop_size"] = SpinBox(master, 10, 200, 10, 30)
        self._params["duration"] = SpinBox(master, 10, 200, 10, 30)

        forml = QtGui.QFormLayout(self)
        self.labels = [QtGui.QLabel('', self) for i in range(4)]
        forml.addRow(self.labels[0], self._params["environment"])
        forml.addRow(self.labels[1], self._params["mutation_rate"])
        forml.addRow(self.labels[2], self._params["pop_size"])
        forml.addRow(self.labels[3], self._params["duration"])
        self.duration_changed = self._params["duration"].valueChanged

        self.retr()

    @property
    def environment(self):
        return self._params["environment"]

    @property
    def mutation_rate(self):
        return self._params["mutation_rate"].value()

    @property
    def pop_size(self):
        return self._params["pop_size"].value()

    @property
    def duration(self):
        return self._params["duration"].value()

    def retr(self):
        self.setTitle(self.tr("Parameters"))
        self.labels[0].setText(self.tr("Oasis"))
        self.labels[1].setText(self.tr("Mutation Rate"))
        self.labels[2].setText(self.tr("Population Size"))
        self.labels[3].setText(self.tr("Duration"))
        self._params["environment"].retr()
        return

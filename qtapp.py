#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

import random
import os
import sys
sys.path.append("/usr/local/lib/python{0}/site-packages".format(sys.version[:3]))

#import sip
#sip.setapi('QString', 2)

from PyQt4 import QtGui, QtCore
#from PySide import QtGui, QtCore
# resource converted from qrc by pyrcc4

QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName("utf-8"))
QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("utf-8"))
import translations

if sys.platform.startswith("darwin"):
    sys.path.append("/System/Library/Frameworks/Python.framework/\
Versions/2.7/Extras/lib/python/PyObjc")
    import Foundation

import numpy

import simulation
from qgraphics import *
from qchart import *
from qparams import *
from qaction import *

#########1#########2#########3#########4#########5#########6#########7#########


class Thread(QtCore.QThread):
    stats_signal = QtCore.pyqtSignal(numpy.ndarray)
    pop_signal = QtCore.pyqtSignal(simulation.Population)

    def __init__(self, parent, population):
        super(self.__class__, self).__init__(parent)
        self._is_killed = False
        self._plot_done = True
        self._draw_done = True
        self._population = population

    def run(self):
        if sys.platform.startswith("darwin"):
            pool = Foundation.NSAutoreleasePool.alloc().init()

        while not self._is_killed:
            while not (self._plot_done and self._draw_done):
                self.msleep(64)

            self._population.reproduce()
            self._population.survive()
            pheno_list = [ind.phenotype for ind in self._population]
            pheno_array = numpy.array(pheno_list)

            self._plot_done = False
            self._draw_done = False

            self.stats_signal.emit(pheno_array)
            self.pop_signal.emit(self._population)
        return

    def emit_population(self):
        self.pop_signal.emit(self._population)

    def plot_done(self):
        self._plot_done = True

    def draw_done(self):
        self._draw_done = True

    def kill(self):
        self._is_killed = True

    def revive(self):
        self._is_killed = False


#########1#########2#########3#########4#########5#########6#########7#########
## Tabs

class PlayPauseButton(QtGui.QPushButton):
    def __init__(self, master):
        super(self.__class__, self).__init__(master)
        self.set_text_play()
        self.setCheckable(True)
        self.setDisabled(True)

    def set_text_pause(self):
        self._is_playing = True
        self.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPause))
        return self.setText(self.tr("Pause"))

    def set_text_play(self):
        self._is_playing = False
        self.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay))
        #self.setIcon(QtGui.QIcon(":media-playback-start"))
        return self.setText(self.tr("Start"))

    def retr(self):
        if self._is_playing:
            self.set_text_pause()
        else:
            self.set_text_play()
        return


class LockButton(QtGui.QPushButton):
    def __init__(self, master):
        super(self.__class__, self).__init__(master)
        self.set_text_lock()

    def set_text_lock(self):
        self._is_locled = False
        qs = QtGui.QStyle.SP_DialogYesButton
        self.setIcon(self.style().standardIcon(qs))
        return self.setText(self.tr("Lock"))

    def set_text_unlock(self):
        self._is_locled = True
        qs = QtGui.QStyle.SP_DialogResetButton
        self.setIcon(self.style().standardIcon(qs))
        return self.setText(self.tr("Reset"))

    def retr(self):
        if self._is_locled:
            self.set_text_unlock()
        else:
            self.set_text_lock()
        return


class EvolutionWidget(QtGui.QWidget):
    plot_done = QtCore.pyqtSignal()
    selected = QtCore.pyqtSignal(simulation.Individual)

    def __init__(self, master):
        super(EvolutionWidget, self).__init__(master)

        self.params = ParamsGroupBox()
        self.params.locked.connect(self.init_thread)
        self.params.unlocked.connect(self.clear_)

        self.lock_button = LockButton(self)
        self.lock_button.clicked.connect(self.toggle_lock)
        self.params.locked.connect(self.lock_button.set_text_unlock)
        self.params.unlocked.connect(self.lock_button.set_text_lock)

        self.play_pause_button = PlayPauseButton(self)
        self.play_pause_button.clicked.connect(self.play_pause)
        self.params.unlocked.connect(self.play_pause_button.setDisabled)

        lhs = QtGui.QVBoxLayout()
        lhs.addWidget(self.params)
        lhs.addWidget(self.lock_button)
        lhs.addWidget(self.play_pause_button)
        lhs.addStretch(1)

        self._charts = [Chart(self) for i in range(3)]

        hbox = QtGui.QHBoxLayout()

        for chart in self._charts:
            hbox.addWidget(chart)
        self.view = GraphicsView(self, [640, 320], self.params.environment.currentIndex())
        self.view.fit_scene()
        self.params.environment.currentIndexChanged.connect(self.view.scene().set_oasis)
        self.view.scene().selected.connect(self.selected_emit)
        self.view.scene().is_clickable = True

        rhs = QtGui.QVBoxLayout()
        rhs.addLayout(hbox)

        notes = QtGui.QHBoxLayout()
        strong_font = self.font()
        strong_font.setBold(True)
        strong_font.setPointSize(strong_font.pointSize() + 1)
        self.choose_click = QtGui.QLabel(self)
        self.choose_click.setFont(strong_font)
        notes.addWidget(self.choose_click)
        self.randomly_chosen = QtGui.QLabel(self)
        self.randomly_chosen.setFont(strong_font)
        self.randomly_chosen.setAlignment(QtCore.Qt.AlignRight)
        notes.addWidget(self.randomly_chosen)
        rhs.addLayout(notes)
        rhs.addWidget(self.view)

        layout = QtGui.QHBoxLayout(self)
        layout.addLayout(lhs)
        layout.addLayout(rhs)
        self.set_xlim_to_duration(self.params.duration)
        self.params.duration_changed.connect(self.set_xlim_to_duration)
        self._t = 0

        self.retr()


    def retr(self):
        self.params.retr()
        self.lock_button.retr()
        self.play_pause_button.retr()
        self.choose_click.setText(self.tr("Click one for crossing experiment"))
        self.randomly_chosen.setText(self.tr("10 individuals randomly chosen"))
        titles = (self.tr("Forewing"), self.tr("Hindwing"), self.tr("Flight Distance"))
        for (chart, main) in zip(self._charts, titles):
            chart.main.setText(main)
            chart.xlab.setText(self.tr("Generations"))
            chart.summary.retr()
            

    def toggle_lock(self):
        if self.params.isEnabled():
            self.params.setDisabled(True)
            self.params.locked.emit(True)
        else:
            if self._t:
                ret = QtGui.QMessageBox.question(None,
                    self.tr("Note"),
                    self.tr("The simulation state in this tab is reset"),
                    QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok,
                    QtGui.QMessageBox.Ok
                )
                if ret != QtGui.QMessageBox.Ok:
                    return
            self.params.setEnabled(True)
            self.params.unlocked.emit(True)
        return

    def init_thread(self):
        self.play_pause_button.setEnabled(True)
        env_index = self.params.environment.currentIndex()
        self._prev = [0] * 4
        self._t = 0
        simulation.Chromosome.MUTATION_RATE = self.params.mutation_rate
        population = simulation.Population(self.params.pop_size, env_index)
        self.thread = Thread(self, population)
        self.thread.started.connect(self.started)
        self.thread.finished.connect(self.finished)
        self.thread.pop_signal.connect(self.view.assign)
        self.thread.stats_signal.connect(self.plot_)
        self.thread.emit_population()
        self.view.animate()

        self.plot_done.connect(self.thread.plot_done)
        self.view.draw_done.connect(self.thread.draw_done)

    def plot_(self, pheno_array):
        min_ = pheno_array.min(0)
        max_ = pheno_array.max(0)
        mean_ = pheno_array.mean(0)
        sd_ = pheno_array.std(0)
        t = self._t
        self._t += 1
        for (i, (u, s, mi, ma)) in enumerate(zip(mean_, sd_, min_, max_)):
            self._charts[i].canvas.plot_((t, t + 1), (self._prev[i], u))
            self._charts[i].canvas.plot_((t + 1, t + 1), (u - s, u + s))
            self._charts[i].canvas.draw()
            self._prev[i] = u
            self._charts[i].summary.display(u, mi, ma)
        if self._t >= self.params.duration:
            self.thread.kill()
        self.plot_done.emit()
        return

    def play_pause(self):
        if self.thread.isRunning():
            self.thread.kill()
        else:
            if self._t < self.params.duration:
                self.thread.revive()
            self.thread.start()
        return

    def clear_(self):
        self.thread.kill()
        for chart in self._charts:
            chart.canvas.clear_()
        self.view.clear_()
        self.set_xlim_to_duration(self.params.duration)
        return

    def started(self):
        self.lock_button.setDisabled(True)
        self.play_pause_button.set_text_pause()
        return

    def finished(self):
        self.view.animate()
        self.lock_button.setEnabled(True)
        self.play_pause_button.set_text_play()
        self.play_pause_button.setChecked(False)
        if self._t >= self.params.duration:
            self.play_pause_button.setDisabled(True)
        return

    def selected_emit(self, individual):
        return self.selected.emit(individual)

    def set_xlim_to_duration(self, duration):
        for chart in self._charts:
            chart.canvas.set_xlim(duration)
        return

    def animate(self):
        return self.view.animate()

    def freeze(self):
        return self.view.freeze()

    @property
    def label(self):
        return self._label


class CrossingWidget(QtGui.QWidget):
    def __init__(self, master, tabs):
        QtGui.QWidget.__init__(self, master)

        self._parents_layout = QtGui.QHBoxLayout()
        self.parents_labels = []
        self.views = dict()
        self._hybrid_view = GraphicsView(self, [640, 320])
        for (i, tab) in enumerate(tabs):
            view = GraphicsView(self, [270, 270],
                                tab.params.environment.currentIndex())
            tab.params.environment.currentIndexChanged.connect(view.scene().set_oasis)
            tab.selected.connect(view.assign)
            tab.selected.connect(self._hybrid_view.clear_)
            self.views[tab] = view
            vbox = QtGui.QVBoxLayout()
            label = QtGui.QLabel(self)
            vbox.addWidget(label)
            self.parents_labels.append(label)
            vbox.addWidget(view)
            self._parents_layout.addLayout(vbox)

        layout = QtGui.QVBoxLayout(self)
        layout.addLayout(self._parents_layout)
        self.button_cross = QtGui.QPushButton(self, clicked=self.cross)
        layout.addWidget(self.button_cross)
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self._hybrid_view)
        hbox.addStretch()
        layout.addLayout(hbox)

    def cross(self):
        qgias = [v.birds for v in self.views.values()]
        if not all(qgias):
            return QtGui.QMessageBox.information(self,
                self.tr("Crossing Experiment"),
                self.tr("Select an individual from each simulation"))
        substances = [l[0].item().substance for l in qgias]
        return self._hybrid_view.copulate(*substances)

    def animate(self):
        for view in self.views.values() + [self._hybrid_view]:
            view.animate()
        return

    def freeze(self):
        for view in self.views.values() + [self._hybrid_view]:
            view.freeze()
        return
        

#########1#########2#########3#########4#########5#########6#########7#########
## Main widgets


class TabWidget(QtGui.QTabWidget):
    def __init__(self, parent):
        QtGui.QTabWidget.__init__(self, parent)
        self._evotabs = [EvolutionWidget(self) for i in range(2)]
        self._crossing = CrossingWidget(self, self._evotabs)
        for tab in self._evotabs:
            self.addTab(tab, '')
        self.addTab(self._crossing, '')
        self.currentChanged.connect(self.pause_the_rest)

    def pause_the_rest(self, idx):
        [self.widget(i).freeze() for i in range(len(self)) if i != idx]
        self.widget(idx).animate()
        return

    def retr(self):
        self.setTabText(0, self.tr("Environment 1"))
        self.setTabText(1, self.tr("Environment 2"))
        self.setTabText(2, self.tr("Crossing Experiment"))
        self._crossing.parents_labels[0].setText(self.tabText(0))
        self._crossing.parents_labels[1].setText(self.tabText(1))
        self._crossing.button_cross.setText(self.tr("Cross"))
        for tab in self._evotabs:
            tab.retr()


class CentralWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(CentralWidget, self).__init__(parent)
        main_layout = QtGui.QVBoxLayout(self)
        self.tabwidget = TabWidget(self)
        main_layout.addWidget(self.tabwidget)

    def retr(self):
        self.tabwidget.retr()


class MainWindow(QtGui.QMainWindow):
    def __init__(self, locale):
        super(MainWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Origami Bird Simulator")
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.setMaximumSize(960, 840)
        self.setStatusBar(StatusBar(self))
        self.setMenuBar(MenuBar(self))
        self.setCentralWidget(CentralWidget(self))
        self.language = QtGui.QLabel('', self)
        self.toolbar = ToolBar(self)
        self.toolbar.addWidget(self.language)
        self.locale_chooser = LocaleChooser(self, locale)
        self.toolbar.addWidget(self.locale_chooser)
        self.addToolBar(self.toolbar)
        self.resize(400, 400)  # not forcing, but minimizing
        self.retr()

    def retr(self):
        self.language.setText(self.tr("Language"))
        self.centralWidget().retr()
        self.menuBar().retr()
        return

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retr()
        return

    def closeEvent(self, event):
        return
        ret = QtGui.QMessageBox.question(self,
                "Closing the main window",
                "Do you really want to close?",
                QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok,
                QtGui.QMessageBox.Ok)
        if ret == QtGui.QMessageBox.Ok:
            event.accept()
        else:
            event.ignore()


#########1#########2#########3#########4#########5#########6#########7#########
## peripheral widgets

class MenuBar(QtGui.QMenuBar):
    def __init__(self, parent):
        super(MenuBar, self).__init__(parent)
        self.menu_file = self.addMenu('')
        #self.menu_file.addAction(Save(self))
        #self.menu_file.addAction(Open(self))
        self.menu_file.addAction(Quit(self, app))

        self.menu_help = self.addMenu('')
        self.menu_help.addAction(About(self))

        self.menu_language = self.addMenu('')

        self.retr()

    def retr(self):
        self.menu_file.setTitle(self.tr("&File"))
        self.menu_help.setTitle(self.tr("&Help"))
        return


locales = {
"en_US": "English",
"ja_JP": "日本語",
}


class LocaleChooser(QtGui.QComboBox):
    def __init__(self, parent, locale_key):
        super(self.__class__, self).__init__(parent)
        for (key, val) in sorted(locales.items()):
            self.addItem(val)
        self.currentIndexChanged.connect(self.install_translator)
        self.setCurrentIndex(sorted(locales.keys()).index(locale_key))

    def install_translator(self, idx):
        self.translator = Translator(sorted(locales.keys())[idx])
        app.installTranslator(self.translator)


class ToolBar(QtGui.QToolBar):
    def __init__(self, parent):
        super(ToolBar, self).__init__(parent)
        self.setMovable(False)
#        self.addAction(Quit(self, app))
#        self.addAction(Open(self))
#        self.addAction(Save(self))


class StatusBar(QtGui.QStatusBar):
    def __init__(self, parent):
        QtGui.QStatusBar.__init__(self, parent)
        #self.addPermanentWidget(ToolButton(Quit(self)))


class ToolButton(QtGui.QToolButton):
    def __init__(self, action, style=0):
        QtGui.QToolButton.__init__(self, action.parentWidget())
        self.setDefaultAction(action)
        self.setToolButtonStyle(style)


#########1#########2#########3#########4#########5#########6#########7#########
## Global

def center(widget):
    screen = QtGui.QDesktopWidget().screenGeometry()
    margin_left = (screen.width() - widget.width()) // 2
    margin_top = (screen.height() - widget.height()) // 2
    widget.move(margin_left, margin_top)
    return


def _TODO():
    return QtGui.QMessageBox.about(None, "TODO", "TODO")


def Translator(locale):
    translator = QtCore.QTranslator()
    translator.load(":translations/{}.qm".format(locale))
    return translator


app = QtGui.QApplication(sys.argv)


if __name__ == '__main__':
    system_locale = QtCore.QLocale().system().name()
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--locale", default=system_locale,
                        choices=locales.keys())
    args = parser.parse_args()

    if False:
        it = QtCore.QDirIterator(":", QtCore.QDirIterator.Subdirectories)
        while it.hasNext():
            print(it.next())

    win = MainWindow(args.locale)
    win.show()
    win.raise_()  # for Mac
    center(win)
    sys.exit(app.exec_())

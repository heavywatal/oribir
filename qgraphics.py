#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import random

from PyQt4 import QtGui, QtCore

import numpy as np

import simulation
# #######1#########2#########3#########4#########5#########6#########7#########
# Drawings


class GraphicsItemAnimationBird(QtGui.QGraphicsItemAnimation):
    def stop_(self):
        return

    def start_(self):
        return


class CopulatingMale(GraphicsItemAnimationBird):
    def __init__(self, individual, successful=True):
        super(self.__class__, self).__init__(None)
        self.setTimeLine(QtCore.QTimeLine(2000))
        self.setItem(BirdItem(individual))
        self.item().setPos(QtCore.QPointF(210, 190))
        present_x = self.item().pos().x()
        present_y = self.item().pos().y()
        fore_le_rear = 1 if individual.fore_le_rear() else -1
        if successful:
            for i in range(201):
                step = i / 200.0
                self.setPosAt(step, QtCore.QPointF(
                    present_x + step * 120,
                    present_y - 6 * fore_le_rear * np.sin(0.9 * np.pi * step)))
                self.setScaleAt(
                    step, 1, 1 - 0.3 * fore_le_rear * np.sin(np.pi * step))
        else:
            for i in range(201):
                step = i / 200.0
                self.setPosAt(step, QtCore.QPointF(
                    present_x + 70 - abs(step - 0.5) * 140,
                    present_y - 4 * fore_le_rear * np.sin(0.9 * np.pi * step)))
                self.setScaleAt(
                    step, 1, 1 - 0.1 * fore_le_rear * np.sin(np.pi * step))
        return


class CopulatingFemale(GraphicsItemAnimationBird):
    def __init__(self, individual, successful=True):
        super(self.__class__, self).__init__(None)
        self.setTimeLine(QtCore.QTimeLine(2000))
        self.setItem(BirdItem(individual))
        self.item().setPos(QtCore.QPointF(340, 190))
        present_x = self.item().pos().x()
        present_y = self.item().pos().y()
        if successful:
            for i in range(201):
                step = i / 200.0
                self.setPosAt(step, QtCore.QPointF(
                    present_x - 10 * np.sin(np.pi * step),
                    present_y))
                self.setScaleAt(step, 1, 1 + 0.3 * np.sin(np.pi * step))
        else:
            for i in range(201):
                step = i / 200.0
                self.setPosAt(step, QtCore.QPointF(
                    present_x - 10 * np.sin(np.pi * step),
                    present_y))
                self.setScaleAt(step, 1, 1 + 0.1 * np.sin(np.pi * step))
        return


class FlyingBird(QtGui.QGraphicsItemAnimation):
    def __init__(self, individual=simulation.Individual()):
        super(self.__class__, self).__init__(None)

        self.setItem(BirdItem(individual))
        self.setTimeLine(QtCore.QTimeLine(2000))
#        self.timeLine().finished.connect(self.item().set_loop_pos)

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._reset)

    def start_(self):
        self._timer.start(random.randrange(3000))

    def stop_(self):
        self._timer.stop()

    def _reset(self):
        self._timer.setInterval(random.randrange(3000, 5000))
        present_x = self.item().pos().x()
        present_y = self.item().pos().y()
        scene_width = self.item().scene().sceneRect().width()
        distance = self.item().substance.phenotype[2]
        dy = random.uniform(-distance, distance)
        for i in range(201):
            step = i / 200.0
            self.setRotationAt(
                step, -0.2 * distance * np.sin(2.0 * np.pi * step))
            self.setPosAt(step, QtCore.QPointF(
                (present_x + 8 * distance * step) % (scene_width + 32),
                present_y - 2 * distance * np.sin(np.pi * step) + dy * step
            ))
        self.timeLine().start()


class BirdItem(QtGui.QGraphicsItem):
    clicked = QtCore.pyqtSignal()
    _LENGTH = 100
    _SCALE = 5
    _PEN_WIDTH = 10

    def __init__(self, individual=simulation.Individual(), parent=None):
        super(self.__class__, self).__init__(parent)
        self._substance = individual
        self._is_marked = False

    @property
    def substance(self):
        return self._substance

    def boundingRect(self):
        return QtCore.QRectF(-10, -96, 128, 128)

    def paint(self, painter, option, widget):
        forewing = self._SCALE * self._substance.phenotype[0]
        hindwing = self._SCALE * self._substance.phenotype[1]

        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.FlatCap)
        pen.setWidth(self._PEN_WIDTH)
        painter.setPen(pen)

        painter.drawLine(0, 0, self._LENGTH, 0)
        painter.drawEllipse(24, -hindwing, 16, hindwing)
        painter.drawEllipse(60, -forewing, 16, forewing)

        # beak
        pen.setColor(QtGui.QColor(255, 128, 0))
        painter.setPen(pen)
        painter.drawLine(self._LENGTH - 8, 0, self._LENGTH, 0)

        if self._is_marked:
            pen.setColor(QtGui.QColor(255, 16, 16))
            pen.setWidth(3)
            painter.setPen(pen)
            rectf = self.boundingRect()
            rectf.setX(rectf.x() + 4)
            rectf.setY(rectf.y() + 4)
            rectf.setWidth(rectf.width() - 8)
            rectf.setHeight(rectf.height() - 8)
            painter.drawRoundedRect(rectf, 8, 8)
        return

    def set_random_pos(self):
        rectf = self.scene().sceneRect()
        x = np.random.randint(0, rectf.width())
        y = np.random.randint(self.boundingRect().height(), rectf.height())
        return self.setPos(QtCore.QPointF(x, y))

#    def set_loop_pos(self):
#        present_x = self.x()
#        scene_width = self.scene().sceneRect().width()
#        if present_x > scene_width:
#            self.setX((scene_width - present_x) // 2 - self._LENGTH)

    def mark(self):
        self._is_marked = True
        self.update()

    def unmark(self):
        self._is_marked = False
        self.update()

    def mousePressEvent(self, event):
        if self.scene().is_clickable:
            self.scene().selected.emit(self._substance)
            self.mark()
        return


class GraphicsScene(QtGui.QGraphicsScene):
    selected = QtCore.pyqtSignal(simulation.Individual)

    def __init__(self, parent, env_index):
        super(self.__class__, self).__init__(parent)
        self.set_oasis(env_index)
        self.is_clickable = False

    def set_oasis(self, env_index):
        if env_index == 0:
            rgb = (255, 200, 112)
            self._oasis_coords = [(150, -20), (0, 10), (500, 10),
                                  (340, 30), (200, 100)]
            self._oasis_coords += [(20, 150), (360, 160),
                                   (530, 180), (180, 210)]
        elif env_index == 2:
            rgb = (255, 160, 112)
            self._oasis_coords = [(0, 160), (220, 0), (480, 110)]
        else:
            rgb = (240, 180, 112)
            self._oasis_coords = [(10, 100), (200, 0), (240, 180), (420, 100)]
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(*rgb)))

    def drawBackground(self, painter, rect):
        super(self.__class__, self).drawBackground(painter, self.sceneRect())
        for coord in self._oasis_coords:
            self.draw_oasis(painter, coord)
        return

    def draw_oasis(self, painter, anchor=(0, 0)):
        self.paint_puddle(painter, anchor)
        pen = QtGui.QPen(QtGui.QColor(180, 210, 150))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(32, 128, 0)))
        for pos in ((15, 50), (30, 140), (90, 55), (110, 130)):
            self.paint_bush(painter, [a + p for (a, p) in zip(pos, anchor)])
        return

    def paint_bush(self, painter, pos=(0, 0)):
        coords = [(6 * x + pos[0], -48 * (x % 2) + pos[1]) for x in range(11)]
        painter.drawPolygon(*[QtCore.QPointF(x, y) for (x, y) in coords])
        return

    def paint_puddle(self, painter, anchor):
        scale = 180
        pen = QtGui.QPen(QtGui.QColor(240, 248, 255, 96))
        pen.setWidth(10)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(16, 192, 224)))
        xpos = anchor[0] + scale // 2
        ypos = anchor[1] + scale // 2
        center_pos = QtCore.QPoint(xpos, ypos)
        painter.drawEllipse(center_pos, scale // 3, scale // 6)
        return


class GraphicsView(QtGui.QGraphicsView):
    draw_done = QtCore.pyqtSignal()

    def __init__(self, parent, size, env_index=1):
        super(self.__class__, self).__init__(parent)
        self.setMinimumSize(*size)
#        self.setMaximumSize(*size)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setScene(GraphicsScene(self, env_index))
        self.scene().selected.connect(self.unmark)
        self.fit_scene()
        self._birds = []

    def fit_scene(self):
        self.scene().setSceneRect(0, 0, self.width(), self.height())

    def resizeEvent(self, event):
        super(self.__class__, self).resizeEvent(event)
        self.fit_scene()

    def clear_(self):
        self._birds = []  # important: first
        self.scene().clear()  # important: second
        return

    def assign(self, individuals):
        if not isinstance(individuals, (list, tuple, simulation.Population)):
            individuals = [individuals]
        self.clear_()
        for (i, ind) in enumerate(individuals[:min(10, len(individuals))]):
            bird = FlyingBird(ind)
            self.scene().addItem(bird.item())
            self._birds.append(bird)
            bird.item().set_random_pos()
        self.draw_done.emit()

    def copulate(self, male, female):
        self.scene().clear()
        self._children = female * male
        successful = self._children
        copulating_male = CopulatingMale(male, successful)
        copulating_female = CopulatingFemale(female, successful)
        self._birds = [copulating_male, copulating_female]
        for bird in self._birds:
            self.scene().addItem(bird.item())
            bird.timeLine().start()
        if successful:
            self._rgb = [255, 235, 245]
            self._timeline = QtCore.QTimeLine(256)
            self._timeline.valueChanged.connect(self.fg_alpha_up)
            self._timeline.finished.connect(self.birth)
            self._birds[0].timeLine().finished.connect(self._timeline.start)
        return

    def fg_alpha_up(self, step):
        rgba = self._rgb + [255 * step]
        self.scene().setForegroundBrush(QtGui.QBrush(QtGui.QColor(*rgba)))
        return

    def fg_alpha_down(self, step):
        rgba = self._rgb + [255 * (1.0 - step)]
        self.scene().setForegroundBrush(QtGui.QBrush(QtGui.QColor(*rgba)))
        return

    def birth(self):
        self._timeline = QtCore.QTimeLine(512)
        self._timeline.valueChanged.connect(self.fg_alpha_down)
        self._timeline.start()
        self.assign(self._children)
        self.animate()
        return

    def animate(self):
        for bird in self._birds:
            bird.start_()
        return

    def freeze(self):
        for bird in self._birds:
            bird.stop_()
        return

    def unmark(self, individual):
        for bird in self.scene().items():
            if bird._substance == individual:
                continue
            bird.unmark()

    @property
    def birds(self):
        return self._birds

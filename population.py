#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import random
import copy
import math

import selection
from individual import Individual


class FitnessLandscape(object):
    def __init__(self):
        sigma = 0.5
        self._const = - 0.5 / sigma ** 2
        return

    def get(self, env_type=1):
        if env_type == 0:
            return self.hop_favored
        elif env_type == 2:
            return self.fly_favored
        else:
            return self.original

    def original(self, flight):
        return math.exp(self._const * (flight / 30.0 - 0.5)**2)

    def fly_favored(self, flight):
        return math.exp(self._const * (flight / 30.0 - 0.97)**2)

    def hop_favored(self, flight):
        return math.exp(self._const * (flight / 30.0 - 0.03)**2)


class Population(object):
    __slots__ = ["_members", "_egg_masses", "_landscape"]

    def __init__(self, size, env_type=0):
        self._members = [Individual() for i in range(size)]
        self._landscape = FitnessLandscape().get(env_type)
        return

    def __len__(self):
        return len(self._members)

    def __iter__(self):
        return iter(self._members)

    def __getitem__(self, key):
        return self._members[key]

    def reproduce(self):
        fathers = self._members[:len(self) // 2]
        mothers = self._members[len(self) // 2:]
        self._egg_masses = [mom * dad for (mom, dad) in zip(mothers, fathers)]
        return

    def survive(self):
        children = []
        for egg_mass in self._egg_masses:
            children.extend(egg_mass)

        for child in children:
            child.fight(self._landscape)

        n = min(len(self), len(children))
        self._members = selection.roulette(children, 0, n)
        return


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    xaxis = list(range(31))
    landscape = FitnessLandscape()
    figure = plt.figure()
    figure.add_subplot(1, 1, 1)
    ax = figure.axes[0]
    ax.plot(xaxis, [landscape.hop_favored(x) for x in xaxis],
            label="Oasis-rich", linewidth=3, color='#000000')
    ax.plot(xaxis, [landscape.original(x) for x in xaxis],
            label="Original", linewidth=3, color='#000000', linestyle='--')
    ax.plot(xaxis, [landscape.fly_favored(x) for x in xaxis],
            label="Oasis-poor", linewidth=3, color='#000000', linestyle=':')
    plt.ylim(0, 1.05)
#    ax.set_title("Fitness Landscape for Origami Birds")
    ax.set_ylabel("Fitness")
    ax.set_xlabel("Flight distance")
    ax.legend(loc="lower center", ncol=3)
    figure.savefig("fitness_landscape.png")

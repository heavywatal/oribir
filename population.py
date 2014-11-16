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
        self._sigma = 0.5
        self._inv_2_pi_sigma = 1.0 / math.sqrt(2 * math.pi * self._sigma)
        return

    def get(self, env_type=1):
        if env_type == 0:
            return self.hop_favored
        elif env_type == 2:
            return self.fly_favored
        else:
            return self.original

    def gaussian(self, x, mu):
        return math.exp(-0.5 * ((x - mu) / self._sigma)**2) * self._inv_2_pi_sigma

    def original(self, flight):
        return self.gaussian(flight / 30.0, 0.5)

    def fly_favored(self, flight):
        return self.gaussian(flight / 30.0, 0.97)

    def hop_favored(self, flight):
        return self.gaussian(flight / 30.0, 0.03)


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
    ax.plot(xaxis, [landscape.original(x) for x in xaxis],
            label="Original")
    ax.plot(xaxis, [landscape.fly_favored(x) for x in xaxis],
            label="Oasis-poor")
    ax.plot(xaxis, [landscape.hop_favored(x) for x in xaxis],
            label="Oasis-rich")
    ax.set_title("Fitness Landscape for Origami Birds")
    ax.set_ylabel("Fitness")
    ax.set_xlabel("Flight")
    ax.legend(loc="lower center", ncol=3)
    figure.savefig("fitness_landscape.png")

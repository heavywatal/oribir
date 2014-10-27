#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""
import random
import copy
import math

import selection

from individual import Individual

import scipy.stats


def sigmoid(x, gain=1.0):
    return 1.0 / (1.0 + math.exp(-gain * x))

#> pnorm(0:1, 0.5, 0.25510673)
#[1] 0.025 0.975
#> pnorm(0:1, 0.5, 0.21492916)
#[1] 0.01 0.99
#> x = c(0:300) * 0.1; plot(sigmoid(x - 15, 0.25) ~ x)


class FitnessLandscape(object):
    def __init__(self):
        return

    def get(self, env_type=1):
        if env_type == 0:
            return self.hop_favored
        elif env_type == 2:
            return self.fly_favored
        else:
            return self.original

    def original(self, flight):
        return scipy.stats.norm.pdf(flight / 30.0, 0.5, 0.2)

    def fly_favored(self, flight):
        return scipy.stats.beta.pdf(flight / 30.0, 2.4, 1.1)
        #return sigmoid(flight - 15, 0.25)

    def hop_favored(self, flight):
        return scipy.stats.beta.pdf(flight / 30.0, 1.1, 2.4)


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

        #self._members = random.sample(children, len(self._members))
        n = min(len(self), len(children))
        self._members = selection.roulette(children, 0, n)
        return


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    #import numpy as np
    #xaxis = np.arange(0.0, 30.0, 0.5)
    xaxis = list(range(31))
    landscape = FitnessLandscape()

    figure = plt.figure()
    figure.add_subplot(1, 1, 1)
    ax = figure.axes[0]
    ax.plot(xaxis, [landscape.original(x) for x in xaxis], label="Original")
    ax.plot(xaxis, [landscape.fly_favored(x) for x in xaxis], label="Oasis-poor")
    ax.plot(xaxis, [landscape.hop_favored(x) for x in xaxis], label="Oasis-rich")
    ax.set_title("Fitness Landscape for Origami Birds")
    ax.set_ylabel("Fitness")
    ax.set_xlabel("Flight")
    #box = ax.get_position()
    #ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    #ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    ax.legend(loc="lower center", ncol=3)
    figure.savefig("fitness_landscape.png")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import random
import copy
import heapq

import numpy


def partial_sums(items):
    s = 0
    out = []
    for x in items:
        s += x
        out.append(s)
    return out


def roulette(population, elites=0, n=None):
    if not n:
        n = len(population)
    the_fittest = []
    if elites == 1:
        # requires individual.fitness
        the_fittest = [max(population, key=lambda ind: ind.fitness)]
    elif elites > 1:
        the_fittest = heapq.nlargest(elites, population)
    else:
        the_fittest = []
    # requires individual.fitness
    bounds = partial_sums([ind.fitness for ind in population])
    for dart in numpy.random.uniform(0.0, bounds[-1], n - elites):
        for (upper_bound, ind) in zip(bounds, population):
            if dart < upper_bound:
                the_fittest.append(ind)
                break
    return the_fittest


def battle_royal(population, n=None):
    champion = max(population, key=lambda ind: ind.fitness)
    return [copy.copy(champion) for i in range(n or len(population))]

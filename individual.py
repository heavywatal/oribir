#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""
import random
import copy

from chromosome import Chromosome


class Individual(object):
    __slots__ = ["_diploid", "_traits", "_flight", "_fitness"]
    _EGG_MASS_SIZE = 20
    NUM_LOCI = 2

    def __init__(self, other=None):
        if not other:
            loci = self.__class__.NUM_LOCI
            self._diploid = (Chromosome([7] * loci), Chromosome([7] * loci))
        else:
            self._diploid = other
        diploid = [h.decode_() for h in self._diploid]
        self._traits = [(lhs + rhs) / 2 for (lhs, rhs) in zip(*diploid)]
        self._flight = self._traits[1] - self._traits[0] + (4 ** Chromosome._DIGITS) - 1
        self._fitness = 0
        return

    def __mul__(self, other):
        """mating function
        >>> child = mother * father
        """
        if not self.accept(other):
            return []
        eggs = self.gametogenesis()
        sperms = other.gametogenesis()
        return [self.__class__(zygote) for zygote in zip(eggs, sperms)]

    def __repr__(self):
        g = str(self.genotype)
        p = str(self.phenotype)
        f = str(self.fitness)
        return ' '.join([g, p, f])

    @property
    def fitness(self):
        return self._fitness

    @property
    def phenotype(self):
        return self._traits + [self._flight]

    @property
    def genotype(self):
        return [str(haploid) for haploid in self._diploid]

    def fight(self, fitness_landscape):
        self._fitness = fitness_landscape(self._flight)
        #self._fitness = sum(self._traits) * 0.1
        return

    def gametogenesis(self):
        for haploid in self._diploid:
            haploid.mutate()
        gametes = []
        for i in range(self.__class__._EGG_MASS_SIZE // 2):
            mother = copy.copy(self._diploid[0])
            father = copy.copy(self._diploid[1])
            gametes.extend(mother * father)
        return gametes

    def fore_le_rear(self):
        return self._traits[0] <= self._traits[1]

    def accept(self, other):
        """return if crossable or not
        """
        if any([abs(x - y) > 5 for (x, y) in zip(self._traits, other._traits)]):
            return False
        if self.fore_le_rear():
            return self._traits[1] >= other._traits[0]
        else:
            return self._traits[1] <= other._traits[0]


def average_gauss(lhs, rhs):
    return random.gauss((lhs + rhs) / 2, abs(lhs - rhs))

#########1#########2#########3#########4#########5#########6#########7#########

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action='store_true', default=False)
    parser.add_argument("-n", "--dry-run", action='store_true', default=False)
    parser.add_argument("args", nargs='*')
    args = parser.parse_args()

    if not args.args:
        individual = Individual()
        print(individual)
    elif len(args.args) > 1:
        father = Individual([Chromosome(args.args[0]), Chromosome(args.args[1])])
        print(father)
    if len(args.args) > 3:
        mother = Individual([Chromosome(args.args[2]), Chromosome(args.args[3])])
        children = father * mother
        print(mother)
        print(children)

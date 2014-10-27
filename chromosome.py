#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""
import random
import copy
import itertools

import numpy


class Chromosome(object):
    __slots__ = ["_sequence"]
    _DIGITS = 2
    _NUCLEOTIDE = "ATGC"
    _CODEC = tuple(''.join(x) for x in itertools.product(_NUCLEOTIDE, repeat=_DIGITS))

    MUTATION_RATE = 0.01
    CROSSOVER_RATE = MUTATION_RATE

    def __init__(self, other=None):
        if not other:
            self._sequence = ''
        elif isinstance(other, basestring):
            self._sequence = other
        elif isinstance(other, int):
            self.encode_([random.randint(0, 4 ** self.__class__._DIGITS) for i in range(other)])
        elif isinstance(other, (list, tuple)):
            self.encode_(other)

    def __str__(self):
        return self._sequence

    def __len__(self):
        return len(self._sequence)

    def __iter__(self):
        return iter(self._sequence)

    def __getitem__(self, key):
        return self._sequence[key]

    def __setitem__(self, key, value):
        self._sequence = self[:key] + value + self[key + 1:]
        return

    def __mul__(self, other):
        '''gametegenesis with crossover
        '''
        n = numpy.random.poisson(self.__class__.CROSSOVER_RATE * (len(self) - 1))
        for i in numpy.random.randint(1, len(self), n):
            self._crossover(other, i)
        if random.randrange(2):
            (self, other) = (other, self)
        return (self, other)

    def _crossover(self, other, chiasma):
        (self._sequence, other._sequence)\
         = (self[:chiasma] + other[chiasma:], other[:chiasma] + self[chiasma:])
        return

    def decode_(self):
        return [self.__class__._CODEC.index(x) for x in split_(self._sequence, self.__class__._DIGITS)]

    def encode_(self, other):
        self._sequence = ''.join(self.__class__._CODEC[x] for x in other)

    def mutate(self):
        n = numpy.random.poisson(self.__class__.MUTATION_RATE * len(self))
        for i in numpy.random.randint(0, len(self), n):
            self[i] = random.choice(self.__class__._NUCLEOTIDE.replace(self[i], ''))
        ### ALTERNATIVE ###
        #trials = numpy.random.binomial(1, self.__class__._MUTATION_RATE, len(self))
        #for i in indices(trials, 1):
        #    self[i] = random.choice(self.__class__._NUCLEOTIDE.replace(self[i], ''))


def split_(seq, step):
    return (seq[i:i + step] for i in range(0, len(seq), step))


def indices(seq, x, comp=cmp):
    return (i for (i, item) in enumerate(seq) if not comp(item, x))

#########1#########2#########3#########4#########5#########6#########7#########8

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action='store_true', default=False)
    parser.add_argument("-n", "--dry-run", action='store_true', default=False)
    parser.add_argument("args", nargs='*')
    args = parser.parse_args()

    for (i, x) in enumerate(Chromosome._CODEC):
        print("{:2}: {}".format(i, x))

    if args.args:
        chromosome = Chromosome(args.args[0])
        print(chromosome)
        print(chromosome.decode_())

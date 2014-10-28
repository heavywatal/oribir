#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from chromosome import Chromosome
from individual import Individual
from population import Population


def main(duration=10, pop_size=6):
    population = Population(pop_size)

    for i in range(duration):
        population.reproduce()
        population.survive()
        print([x.phenotype for x in population])

    genetic = [ind.genotype for ind in population]
    print(genetic)


if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser(version="%prog 1.0")
    parser.set_usage("usage: %prog [options] [...]")
    parser.add_option("-v", "--verbose", action='store_true', default=False)
    parser.add_option("-n", "--dry-run", action='store_true', default=False)
    (options, args) = parser.parse_args()

    main()

# -*- coding: utf-8 -*-
'''
Модуль для тестирования исправления искажений образов
'''

from lab_3 import *
import unittest
import itertools

class CorruptionTestCase(unittest.TestCase):
    def test_N(self):
        imageN = [[1, -1, -1, -1, 1], [1, 1, -1, -1, 1], [1, -1, 1, -1, 1], [1, -1, -1, 1, 1], [1, -1, -1, -1, 1]]
        N = get_X(imageN)

        indexes = list()
        coefficient = 0.1
        for i in xrange(0, 25):
            indexes.append(i)
        permutations = itertools.permutations(indexes, coefficient*len(N))
        for permutation in permutations:
            N = get_X(imageN)
            for i in permutation:
                N[i] = -N[i]
            if self.assertEqual(imageN, correction([imageN], N)) == 'F':
                print N

    def test_O(self):
        imageO = [[1, 1, 1, 1, 1], [1, -1, -1, -1, 1], [1, -1, -1, -1, 1], [1, -1, -1, -1, 1], [1, 1, 1, 1, 1]]
        O = get_X(imageO)

        indexes = list()
        coefficient = 0.1
        for i in xrange(0, 25):
            indexes.append(i)
        permutations = itertools.permutations(indexes, coefficient*len(O))
        for permutation in permutations:
            O = get_X(imageO)
            for i in permutation:
                O[i] = -O[i]
            self.assertEqual(imageO, correction([imageO], O))

    def test_P(self):
        imageP = [[1, 1, 1, 1, 1], [1, -1, -1, -1, 1], [1, 1, 1, 1, 1], [1, -1, -1, -1, -1], [1, -1, -1, -1, -1]]
        P = get_X(imageP)

        indexes = list()
        coefficient = 0.1
        for i in xrange(0, 25):
            indexes.append(i)
        permutations = itertools.permutations(indexes, coefficient*len(P))
        for permutation in permutations:
            P = get_X(imageP)
            for i in permutation:
                P[i] = -P[i]
            self.assertEqual(imageP, correction([imageP], P))

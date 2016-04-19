# -*- coding: utf-8 -*-
'''
Модуль для тестирования исправления искажений образов
'''

from lab_3 import *
import unittest
import itertools
import matplotlib.pyplot as plt
from DataIO import *

def drawGraph(coefficient, percent, name = 'corruption_letter'):
    plt.plot(coefficient, percent, marker = 'o')
    plt.xlabel('coefficient of corruption, %')
    plt.ylabel('percent of correctly guessed, %')
    plt.axis([0, coefficient[-1]+1, 0, max(percent)+1])
    plt.title(name)
    plt.grid(True)
    plt.savefig('plt_{0}.png'.format(name))
    plt.clf()

def find_percent(image, images, coefficient):
    test_letter = get_X(image)

    indexes = list()
    for i in xrange(0, len(test_letter)):
        indexes.append(i)

    permutations = itertools.permutations(indexes, coefficient*len(test_letter))
    correctly_guessed = 0
    count = 0
    for permutation in permutations:
        count += 1
        test_letter = get_X(image)
        for i in permutation:
            test_letter[i] = -test_letter[i]
        if image == correction(images, test_letter):
            correctly_guessed += 1
    if correctly_guessed == 0:
        return float(0)
    else:
        return float('%.3f' % (float(correctly_guessed)*100/float(count)))

def find_thresholds(image, images):
    array_coeff = list()
    array_percent = list()

    coefficient = 0.1

    percent = find_percent(image, images, coefficient)

    array_coeff.append(float(coefficient)*100)
    array_percent.append(percent)

    while float(percent) != float(0):
        coefficient += 0.05
        percent = find_percent(image, images, coefficient)
        array_coeff.append(float(coefficient)*100)
        array_percent.append(percent)

    return array_coeff, array_percent

class CorruptionTestCase(unittest.TestCase):
    def test_N(self):
        imageN = [[1, -1, -1, -1, 1], [1, 1, -1, -1, 1], [1, -1, 1, -1, 1], [1, -1, -1, 1, 1], [1, -1, -1, -1, 1]]
        imageO = [[1, 1, 1, 1, 1], [1, -1, -1, -1, 1], [1, -1, -1, -1, 1], [1, -1, -1, -1, 1], [1, 1, 1, 1, 1]]
        imageP = [[1, 1, 1, 1, 1], [1, -1, -1, -1, 1], [1, 1, 1, 1, 1], [1, -1, -1, -1, -1], [1, -1, -1, -1, -1]]
        N = get_X(imageN)

        indexes = list()
        coefficient = 0.1
        for i in xrange(0, len(N)):
            indexes.append(i)
        permutations = itertools.permutations(indexes, coefficient*len(N))
        for permutation in permutations:
            N = get_X(imageN)
            for i in permutation:
                N[i] = -N[i]
            self.assertEqual(imageN, correction([imageN, imageO, imageP], N))

    def test_O(self):
        imageN = [[1, -1, -1, -1, 1], [1, 1, -1, -1, 1], [1, -1, 1, -1, 1], [1, -1, -1, 1, 1], [1, -1, -1, -1, 1]]
        imageO = [[1, 1, 1, 1, 1], [1, -1, -1, -1, 1], [1, -1, -1, -1, 1], [1, -1, -1, -1, 1], [1, 1, 1, 1, 1]]
        imageP = [[1, 1, 1, 1, 1], [1, -1, -1, -1, 1], [1, 1, 1, 1, 1], [1, -1, -1, -1, -1], [1, -1, -1, -1, -1]]
        O = get_X(imageO)

        indexes = list()
        coefficient = 0.1
        for i in xrange(0, len(O)):
            indexes.append(i)
        permutations = itertools.permutations(indexes, coefficient*len(O))
        for permutation in permutations:
            O = get_X(imageO)
            for i in permutation:
                O[i] = -O[i]
            self.assertEqual(imageO, correction([imageN, imageO, imageP], O))

    def test_P(self):
        imageN = [[1, -1, -1, -1, 1], [1, 1, -1, -1, 1], [1, -1, 1, -1, 1], [1, -1, -1, 1, 1], [1, -1, -1, -1, 1]]
        imageO = [[1, 1, 1, 1, 1], [1, -1, -1, -1, 1], [1, -1, -1, -1, 1], [1, -1, -1, -1, 1], [1, 1, 1, 1, 1]]
        imageP = [[1, 1, 1, 1, 1], [1, -1, -1, -1, 1], [1, 1, 1, 1, 1], [1, -1, -1, -1, -1], [1, -1, -1, -1, -1]]
        P = get_X(imageP)

        indexes = list()
        coefficient = 0.1
        for i in xrange(0, len(P)):
            indexes.append(i)
        permutations = itertools.permutations(indexes, coefficient*len(P))
        for permutation in permutations:
            P = get_X(imageP)
            for i in permutation:
                P[i] = -P[i]
            self.assertEqual(imageP, correction([imageN, imageO, imageP], P))

def handle_arguments(arguments):
    images = list()
    for argument in arguments:
        if 'Test.py' not in argument:
            images.append(read_images(argument))
    for (index,image) in enumerate(images):
        coefficients, percents = find_thresholds(image, images)
        drawGraph(coefficients, percents, name = 'corruption_image_' + str(index + 1))

if __name__ == '__main__':
        if len(sys.argv) < 2:
            print u'не задан файл образа'
        else:
            handle_arguments(sys.argv)

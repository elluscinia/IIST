# -*- coding: utf-8 -*-
'''
Лабораторная работа No 1
Исследование однослойных нейронных сетей на примере
моделирования булевых выражений.

Цель: Исследовать функционирование простейшей нейронной сети (НС) на базе нейрона с
нелинейной функцией активации и ее обучение по правилу Видроу-Хоффа.

Вариант 23.
'''
import sys
from AF import *
from logistics_AF_education import *
from Tools import boolean_function

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'недостаточное количество параметров'
    else:
        outputFile = sys.argv[1]
        F = list()
        W = [0, 0, 0, 0, 0]
        n = 4
        X = list()
        count = 2**n
        for i in xrange(0, count):
            X.append([int(x) for x in IntToByte(i)])
            while len(X[i]) < 4:
                X[i].insert(0, 0)

        for x in X:
            F.append(boolean_function(x[0], x[1], x[2], x[3]))

        # Получим нейросетевую модель БФ, используя пороговую ФА
        w = list(W)
        f = list(F)
        kind_AF(w, f, outputFile + '_threshold', 'threshold')

        # Получим нейросетевую модель БФ, используя логистическую ФА
        w = list(W)
        f = list(F)
        kind_AF(w, f, outputFile + '_logistics', 'logistics')

        # Найдем минимальный набор обучающих векторов
        w = list(W)
        f = list(F)
        education_AF(w, f, outputFile + '_education')

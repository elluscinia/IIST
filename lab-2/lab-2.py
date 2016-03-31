# -*- coding: utf-8 -*-
'''
Исследовать функционирование нейронной сети (НС) с радиальными базисными функ-
циями (RBF) и ее обучение по правилу Видроу-Хоффа.
'''
import sys
from Education import *

def initialize_components():
    '''
    Функция инциализирует необходимые для расчётов компоненты
    :param return: F - значения БФ, V - начальные весовые коэффициенты, C - центры RBF
    '''
    V = list()
    C = list()
    n = 4 # число переменных
    X = bin_generation(n)
    F = get_F(X)

    count_1 = F.count(1) # кол-во единиц в БФ
    count_0 = F.count(0) # кол-во нулей в БФ

    # формируем ыектор начальных весовых коэффициентов
    for i in xrange(0, (min(count_0, count_1) + 1)):
        V. append(0)

    # сформируем список центров RBF
    if count_0 < count_1:
        for x,f in zip(X,F):
            if f == 0:
                C.append(x)
    else:
        for x,f in zip(X,F):
            if f == 1:
                C.append(x)

    return F, V, C

def get_F(X):
    '''
    Функция возвращает значения БФ на заданных ей наборах переменных
    :param X: наборы переменных значения БФ
    :param return: значения БФ
    '''
    F = list()
    for x in X:
        # x0 в расчёт не берётся. Оно необходимо лишь для правила Видроу-Хоффа
        F.append(boolean_function(x[1], x[2], x[3], x[4]))
    return F

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'отсутствует имя файла вывода'
    else:
        # имя файла вывода
        outputFile = sys.argv[1]

        # инициализируем необходимые для расчётов компоненты
        # F - значение БФ
        # V - исходный набор весов
        # C - центры RBF
        F, V, C = initialize_components()

        education_RBF(list(V), list(F), list(C), outputFile)

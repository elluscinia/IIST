# -*- coding: utf-8 -*-
'''
Получить нейросетевую модель БФ, используя в качестве пороговой ФА
f(net) = {1, net > 0;
          0, net <= 0}
'''
import matplotlib.pyplot as plt
from Tools import *
from DataIO import *
from Calculation import *
from Graphic import *

def kind_AF(W, F, outputFile, kind):
    X = bin_generation(4) # генерируем вектора для 4-х переменных
    nu = 0.3 # норма обучения
    E = 1 # необходимо для начала цикла прохода по эпохам
    k = -1 # необходимо для начала отсчёта эпох

    arrayE = list() # список всех суммарнах квадратичных ошибок
    arrayK = list() # список всех эпох
    Y = list() # вектор для хранения полученного реального выхода текущей эпохи

    file = open(outputFile, 'w')

    while E != 0:
        k += 1

        prev_W = list(W)

        for (x, f) in zip(X, F):
            # 1) считаем net
            n = net(W, x)

            # 2) считаем реальный выход
            y = actual_NN(n)
            Y.append(y)

            # 3) считаем ошибку дельта
            d = delta(f, y)

        # 5) посчитаем суммарную квадратичную ошибку
        E = totalError(Y, F)

        write_Data(file, k, Y, prev_W, E)

        Y = list()

        if E != 0:

            for (x,f) in zip(X, F):

                # 1) считаем net
                n = net(W, x)

                # 2) считаем реальный выход
                y = actual_NN(n)

                # 3) считаем ошибку дельта
                d = delta(f, y)

                # 4) пересчитываем W
                W = recount_W(W, x, d, n, nu, kind)

        arrayK.append(k)
        arrayE.append(E)

    drawGraph(arrayE, arrayK, outputFile)

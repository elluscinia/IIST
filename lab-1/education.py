# -*- coding: utf-8 -*-
'''
Получить нейросетевую модель БФ, используя логистическую ФА (сигмоидальную).
Найти наименьшее возможное для обучения количество векторов.
'''
import matplotlib.pyplot as plt
from Tools import *
from DataIO import *
from Calculation import *
from Graphic import *
import itertools

def education_AF(inputW, inputF, outputFile, kind):
    X = bin_generation(4) # генерируем вектора для 4-х переменных

    for i in xrange(2**4, 2, -1):
        # генерируем комбинации векторов различных длин
        combinations = list(itertools.combinations(zip(X, inputF), i))
        for combination in combinations:
            W, F = list(inputW), list(inputF)

            nu = 0.3 # норма обучения
            E = 1 # необходимо для начала цикла прохода по эпохам
            k = -1 # необходимо для начала отсчёта эпох

            Y = list() # вектор для хранения полученного реального выхода текущей эпохи

            while E != 0 and k < 200:
                k += 1

                e = 0

                prev_W = list(W)

                # проверим выходной вектор на наличие ошибок
                for (x, f) in combination:
                    # 1) считаем net
                    n = net(W, x)

                    # 2) считаем реальный выход
                    y = actual_NN(n)

                    # 3) считаем ошибку дельта
                    d = delta(f, y)

                    if d != 0:
                        e += 1

                # в случае ошибки выходного вектора
                if e != 0:
                    e = 0
                    # обучаем на выборке
                    for (x,f) in combination:
                        # 1) считаем net
                        n = net(W, x)

                        # 2) считаем реальный выход
                        y = actual_NN(n)

                        # 3) считаем ошибку дельта
                        d = delta(f, y)

                        if d != 0:
                            e += 1 # ошибка для обучения на векторе

                        # 4) пересчитываем W
                        W = recount_W(W, x, d, n, nu, kind = kind)
                E = e

            # получили вектор, на котором успешно завершилось обучение - prev_W
            W = list(prev_W)

            # проверим успешность обучения
            for (x, f) in zip(X, F):
                n = net(W, x)
                y = actual_NN(n)
                Y.append(y)

            # 5) посчитаем суммарную квадратичную ошибку
            E = totalError(Y, F)

            # запишем найденные вектора, кол-во эпох обучения и набор весов
            if E == 0:
                min_edication = {'combination': combination, 'k': k+1, 'W': W}

    # запишем в файл найденные значения
    file = open(outputFile, 'w')
    write_Data(file, min_edication['k'], [i for i,j in min_edication['combination']], min_edication['W'], 0)

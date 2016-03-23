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

def write_min(combination, outputFile, W, kind):
    '''
    Функция записывает в файл процесс обучения на минимально возможном количестве векторов
    :param combination: найденная наилучшая комбинация векторов
    :param outputFile: имя файла записи
    :param W: входные значения весовых коэффициентов
    :param kind: вид ФА threshold - пороговая, logistics - логистическая
    :param return: none
    '''
    # запишем в файл найденные значения
    file = open(outputFile, 'w')
    file.write('set:\n')
    for i,x in enumerate(combination[1]):
        file.write('X(' + str(i+1) + ') = (' + str(x[0])[4:-1] + ')')
        file.write('\n')
    file.write('\n')

    nu = 0.3 # норма обучения
    E = 1 # необходимо для начала цикла прохода по эпохам
    k = -1 # необходимо для начала отсчёта эпох

    arrayE = list() # список всех суммарнах квадратичных ошибок
    arrayK = list() # список всех эпох

    Y = list() # вектор для хранения полученного реального выхода текущей эпохи

    F = [i[1] for i in combination[1]] # вектор значений БФ, на котром происходит обучение

    # будем обучать, пока не будет достигнула ошибка 0 или не придём к выводу, что она не достижима
    # для этого в качестве "порога" поиска возьмём ограниченное число эпох для обучения
    while E != 0:
        # перехожим к следующей эпохе +1
        k += 1

        # запоминаем последние полученные весовые коэффициенты на случай получения нулевой ошибки
        prev_W = list(W)

        # проверим выходной вектор на наличие ошибок
        for (x, f) in combination[1]:
            # 1) считаем net
            n = net(W, x)

            # 2) считаем реальный выход
            y = actual_NN(n)
            Y.append(y)

            # 3) считаем ошибку дельта
            d = delta(f, y)

        # 5) посчитаем суммарную квадратичную ошибку
        E = totalError(Y, F)

        # запишем полученные данные в файл
        write_Data(file, k, Y, prev_W, E)

        Y = list() # очистим вектор от полученных данных

        # в случае ошибки выходного вектора
        if E != 0:
            # обучаем на выборке
            for (x,f) in combination[1]:
                # 1) считаем net
                n = net(W, x)

                # 2) считаем реальный выход
                y = actual_NN(n)

                # 3) считаем ошибку дельта
                d = delta(f, y)

                # 4) пересчитываем W
                W = recount_W(W, x, d, n, nu, kind = kind)

        # добавим номер рассчитанной эпохи и найденную для неё среднеквадратичную ошибку
        arrayK.append(k)
        arrayE.append(E)

    # построим график зависимости среднеквадратичной ошибки от эпохи
    drawGraph(arrayE, arrayK, outputFile)

def check_combination(W, combination, kind):
    '''
    Функция проверяется комбинация на "обучаемость"
    :param W: входные значения весовых коэффициентов
    :param combination: найденная наилучшая комбинация векторов
    :param kind: вид ФА threshold - пороговая, logistics - логистическая
    :param return: W, k в случае успеха, W, -1 в обратном случае
    '''
    nu = 0.3 # норма обучения
    E = 1 # необходимо для начала цикла прохода по эпохам
    k = -1 # необходимо для начала отсчёта эпох

    Y = list() # вектор для хранения полученного реального выхода текущей эпохи

    # будем обучать, пока не будет достигнула ошибка 0 или не придём к выводу, что она не достижима
    # для этого в качестве "порога" поиска возьмём ограниченное число эпох для обучения
    epochs = 200
    while E != 0 and k < epochs:
        # перехожим к следующей эпохе +1
        k += 1

        # зададим переменную для поиска ошибок при обучении
        e = 0

        # запоминаем последние полученные весовые коэффициенты на случай получения нулевой ошибки
        prev_W = list(W)

        # проверим выходной вектор на наличие ошибок
        for (x, f) in combination:
            # 1) считаем net
            n = net(W, x)

            # 2) считаем реальный выход
            y = actual_NN(n)

            # 3) считаем ошибку дельта
            d = delta(f, y)

            # если имеется ошибкв, прибавим её к переменной для отслеживания ошибок обучения
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
    if k < epochs:
        return W, k
    else:
        return W, -1

def education_AF(inputW, inputF, outputFile, kind):
    '''
    Функция поиска минимального вектора для обучения
    :param inputW: входные значения весовых коэффициентов
    :param inputF: значения БФ
    :param outputFile: имя файла записи
    :param kind: вид ФА threshold - пороговая, logistics - логистическая
    :param return: none
    '''
    X = bin_generation(4) # генерируем вектора для 4-х переменных

    for i in xrange(2**4, 2, -1):
        # генерируем комбинации векторов различных длин
        combinations = list(itertools.combinations(zip(X, inputF), i))

        arrayKN = list()

        # будем проверять каждую комбинацию
        for combination in combinations:

            Y = list()

            W, k = check_combination(list(inputW), combination, kind)

            if k != -1:

                # проверим успешность обучения
                for (x, f) in zip(X, inputF):
                    n = net(W, x)
                    y = actual_NN(n)
                    Y.append(y)

                # 5) посчитаем суммарную квадратичную ошибку
                E = totalError(Y, inputF)

                # запишем найденные вектора, кол-во эпох обучения и набор весов
                if E == 0:
                    arrayKN.append((k, combination, W))
                    best_combination = sorted(arrayKN, key = lambda education: education[0])[0]

    # запишем минимальный набор с минимальным количеством эпох
    write_min(best_combination, outputFile, list(inputW), kind)

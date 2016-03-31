# -*- coding: utf-8 -*-
'''
Получить модель булевой функции (БФ) на основе RBF-НС.
Требуется найти минимальный набор векторов X , используемых для обучения.
'''
import itertools
from Tools import *
from Graphic import *
from DataIO import *
from Calculation import *

def check_combination(V, combination, C):
    '''
    Функция проверяется комбинация на "обучаемость"
    :param V: входные значения весовых коэффициентов
    :param combination: найденная наилучшая комбинация векторов
    :param C: центры RBF
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

        # список выходов RBF-нейронов
        phi = list()

        # проверим выходной вектор на наличие ошибок
        for (x,f) in combination:
            # 1) считаем выходы RBF-нейронов
            phi = get_phi_array(x, C)

            # 2) считаем net
            n = net(V, phi)

            # 2) считаем реальный выход
            y = actual_NN(n)
            Y.append(y)

            phi = list()

        # 3) считаем суммарную квадратичную ошибку
        E = totalError(Y, [i[1] for i in combination])

        Y = list()

        # в случае ошибки выходного вектора
        if E != 0:
            # обучаем на выборке
            for (x,f) in combination:
                # 1) считаем выходы RBF-нейронов
                phi = get_phi_array(x, C)

                # 2) считаем net
                n = net(V, phi)

                # 3) считаем реальный выход
                y = actual_NN(n)

                # 4) считаем ошибку дельта
                d = delta(f, y)

                # 5) пересчитываем V
                V = recount_V(V, x, d, nu, phi)
                phi = list()

    if k < epochs:
        return V, k
    else:
        return V, -1

def education_RBF(inputV, inputF, C, outputFile):
    '''
    Функция поиска минимального вектора для обучения
    :param inputV: входные значения весовых коэффициентов
    :param inputF: значения БФ
    :param C: центры RBF
    :param outputFile: имя файла записи
    :param return: none
    '''
    X = bin_generation(4) # генерируем вектора для 4-х переменных

    for i in xrange(2**4, 2, -1):
        # генерируем комбинации векторов различных длин
        combinations = list(itertools.combinations(zip(X, inputF), i))

        arrayKN = list()

        # будем проверять каждую комбинацию
        for combination in combinations:

            V, k = check_combination(list(inputV), combination, C)

            if k != -1:
                # проверка успешности обучения
                phi = list()
                Y = list()

                for (x,f) in zip(X, inputF):
                    # 1) считаем выходы RBF-нейронов
                    phi = get_phi_array(x, C)

                    # 2) считаем net
                    n = net(V, phi)

                    # 3) считаем реальный выход
                    y = actual_NN(n)
                    Y.append(y)

                    phi = list()

                # 4) посчитаем суммарную квадратичную ошибку
                E = totalError(Y, inputF)

                # запишем найденные вектора, кол-во эпох обучения и набор весов
                if E == 0:
                    arrayKN.append([k, combination, V])
                    best_combination = sorted(arrayKN, key = lambda education: education[0])[0]

    # запишем минимальный набор с минимальным количеством эпох
    write_min(list(inputV), best_combination[1], C, outputFile)

def write_min(V, combination, C, outputFile):
    '''
    Функция записывает в файл процесс обучения на минимально возможном количестве векторов
    :param V: входные значения весовых коэффициентов
    :param combination: найденная наилучшая комбинация векторов
    :param C: центры RBF
    :param outputFile: имя файла записи
    :param return: none
    '''
    # запишем в файл найденные значения
    file = open(outputFile, 'w')
    file.write('set:\n')
    for i,x in enumerate(combination):
        file.write('X(' + str(i+1) + ') = (' + str(x[0])[4:-1] + ')')
        file.write('\n')
    file.write('\n')

    nu = 0.3 # норма обучения
    E = 1 # необходимо для начала цикла прохода по эпохам
    k = -1 # необходимо для начала отсчёта эпох

    arrayE = list() # список всех суммарнах квадратичных ошибок
    arrayK = list() # список всех эпох

    Y = list() # вектор для хранения полученного реального выхода текущей эпохи

    F = [i[1] for i in combination] # вектор значений БФ, на котром происходит обучение

    # будем обучать, пока не будет достигнула ошибка 0 или не придём к выводу, что она не достижима
    # для этого в качестве "порога" поиска возьмём ограниченное число эпох для обучения
    while E != 0:
        k += 1

        phi = list()

        for (x,f) in combination:

            # 1) считаем выходы RBF-нейронов
            phi = get_phi_array(x, C)

            # 2) считаем net
            n = net(V, phi)

            # 3) считаем реальный выход
            y = actual_NN(n)
            Y.append(y)

            phi = list()

        # 4) посчитаем суммарную квадратичную ошибку
        E = totalError(Y, F)

        # запишем полученные данные в файл
        write_Data(file, k, Y, V, E)

        Y = list() # очистим вектор от полученных данных

        if E != 0:
            for (x,f) in combination:

                # 1) считаем выходы RBF-нейронов
                phi = get_phi_array(x, C)

                # 2) считаем net
                n = net(V, phi)

                # 3) считаем реальный выход
                y = actual_NN(n)

                # 4) считаем ошибку дельта
                d = delta(f, y)

                # 5) пересчитываем V
                V = recount_V(V, x, d, nu, phi)
                phi = list()

        # добавим номер рассчитанной эпохи и найденную для неё среднеквадратичную ошибку
        arrayK.append(k)
        arrayE.append(E)

    # построим график зависимости среднеквадратичной ошибки от эпохи
    drawGraph(arrayE, arrayK, outputFile)

# -*- coding: utf-8 -*-
'''
Исследовать процедуры обучения и функционирования рекуррентных нейронных сетей
(РНС) Хопфилда в качестве устройства автоассоциативной памяти.
'''

import sys
from Calculation import *
from DataIO import *

def count_w(image):
    '''
    Вычисляется матрица вида (X^T)*X
    :param image: образ
    :param return: матрица
    '''
    w = list()
    for i in image:
        string = list()
        for j in image:
            string.append(i*j)
        w.append(string)
    return w

def count_matrix_W(images):
    '''
    Функция настройки веса РНС Хопфилда
    :param images: образы
    :param return: матрица весов
    '''
    w = list()
    for image in images:
        w.append(count_w(image))

    # не будем привызяваться к количеству и размерам образов
    n = len(w[0][0]) # количество элементов в строке
    m = len(w[0]) # количество строк в матрице
    M = list()

    # нулевая матрица размера матрицы весов
    for i in xrange(0, m):
        string = list()
        for j in xrange(0, n):
            string.append(0)
        M.append(string)

    # сумма матриц
    for m in w:
        M = sum_matrix(M, m)

    # обнулим диагональ матрицы
    for i in xrange(0, len(images[0])):
        M[i][i] = 0
    return M

def count_f(net):
    '''
    Функция подсчёта реального выхода
    :param net: сетевой вход
    :param return: реальный выход
    '''
    if net > 0:
        return 1
    elif net < 0:
        return -1
    else:
        return 0

def count_net(W, index_W, y):
    '''
    Функция подсчёта сетевого выхода
    :param W: матрица весов
    :param index_W: номер строки в матрице весов
    :param y: параметры предыдущего реального выхода
    :param return: сетевой вход
    '''
    net = 0
    for index_y in xrange(0, len(y)):
        if index_y != index_W:
            net += W[index_y] * y[index_y]
    return net

def count_y(W, y):
    '''
    Функция подсчёта реального выхода всего набора
    :param W: матрица весов
    :param y: начальный реальный выход
    :param return: исправленый набор
    '''
    Y = list()
    for index_W in xrange(0, len(W)):
        net = count_net(W[index_W], index_W, y)
        if count_f(net) != 0:
            Y.append(count_f(net))
        else:
            Y.append(y[index_W])
    return Y

def check(Y, images_vectors):
    '''
    Функция проверки правильности исправления искажения
    :param Y: реальный выход
    :param images_vectors: векторизованные образы
    :param return: в случае успеха возвращает положительный результат
    '''
    for vector in images_vectors:
        if Y == vector:
            return True

def correction(images, corruption):
    '''
    Функция корректировки искажения
    :param images: образы
    :param corruption: искажённый вектор
    :param return: результат исправления искажения (найденный образ или невозможность восстановления)
    '''
    images_vectors = list()

    # векторизуем образы
    for image in images:
        images_vectors.append(get_X(image))

    # настроим веса
    W = count_matrix_W(images_vectors)

    count = 0
    max_eras = 200 # в случае невозможности достижения исправления

    Y = count_y(W, corruption)
    while check(Y, images_vectors) == None and count < max_eras:
        y = list(Y)
        Y = count_y(W, y)
        count += 1

    if check(Y, images_vectors) != None :
        n = len(images[0][0]) # количество элементов в строке
        standart = get_image(Y, n)
        return standart
    else:
        return 'образ не распознан'

def handle_arguments(arguments):
    '''
    Обработчик аргументов командной строки
    :param arguments: аргументы командной строки
    :param return: None
    '''
    images = list()
    for argument in arguments:
        if 'lab_3.py' not in argument:
            images.append(read_images(argument))
    print u' введите паттерн:'
    inputVector = raw_input('\t')
    if inputVector[0] != str(1) and inputVector[0] != str(-1):
        try:
            f = open(inputVector)
            data = [line[:-1] for line in f]
            f.close()
            corruption = [int(i) for i in data[0].split(' ')]
            result = correction(images, corruption)
        except IOError:
            print u'\tтакого файла нет'
            result = 'образ не распознан'
    else:
        corruption = [int(i) for i in inputVector.split(' ')]
        result = correction(images, corruption)
    if result != 'образ не распознан':
        if 'linux' in sys.platform:
            corrected_vector = get_X(result)
            output_vector = '\t'
            for i in xrange(0, len(corruption)):
                if corruption[i] != corrected_vector[i]:
                    output_vector += '\033[93m' + str(corruption[i]) + '\033[0m' + ' '
                else:
                    output_vector += str(corruption[i]) + ' '
            print output_vector
        print u'\n распознан следующий образ:'
        corruption_image = get_image(corruption, len(result[0]))
        for index_i,i in enumerate(result):
            string = '\t'
            for index_j,j in enumerate(i):
                if 'linux' in sys.platform:
                    if j != corruption_image[index_i][index_j]:
                        string += '\033[93m' + str(j) + '\033[0m' +'\t'
                    elif j == 1:
                        string += '\033[94m' + str(j) + '\033[0m' +'\t'
                    else:
                        string += str(j) + '\t'
                else:
                    string += str(j) + '\t'
            print string
    else:
        print u'\tобраз не распознан'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print u'не задан файл образа'
    else:
        # 1 1 1 1 1 -1 1 1 1 -1 -1 -1 1 -1 -1 -1 -1 -1 1 -1 1 1 1 1 1
        handle_arguments(sys.argv)

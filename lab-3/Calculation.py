# -*- coding: utf-8 -*-
"""
Модуль для работы с матрицами и образами/векторами
"""

def get_X(letter):
    '''
    Функция возвращает векторизованные по столбцам матрицы
    :param letter: матрица для векторизации
    :return: векторизованная матрица
    '''
    X = list()
    for i in xrange(0, len(letter[0])):
        for x in letter:
            X.append(x[i])
    return X

def get_matrix_transpose(matrix):
    '''
    Функция транспонирует матрицу
    :param matrix: матрица
    :param return: транспонированная матрица
    '''
    m = list()
    for i in xrange(0, len(matrix)):
        # обращение к строчке
        string = list()
        for j in xrange(0, len(matrix[0])):
            # образние к элементу строки
            string.append(matrix[j][i])
        m.append(string)
    return m

def get_image(X, n):
    '''
    Функция получения образа из вектора
    :param X: вектор
    :param n: количество элементов в строке образа
    :param return: образ
    '''
    image = list()
    start = 0
    end = n
    while start < len(X):
        image.append(X[start:end])
        start += n
        end += n
    return get_matrix_transpose(image)

def sum_string(a, b):
    '''
    Функция складывает строки поэлементно
    :param a: строка а
    :param b: строка b
    :param return: поэлементная сумма строк a+b
    '''
    summ = list()
    for index in xrange(0, len(a)):
        summ.append(a[index] + b[index])
    return summ

def sum_matrix(a, b):
    '''
    Функция складывает матрицы
    :param a: матрица а
    :param b: матрица b
    :param return: сумма матриц a+b
    '''
    w = list()
    for index in xrange(0, len(a)):
        w.append(sum_string(a[index], b[index]))
    return w



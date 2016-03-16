# -*- coding: utf-8 -*-
'''
Модуль с инструментами, облегчающими работу
'''

def IntToByte(x):
    '''
    Функция переводит десятичную хапись числа в двоичную
    :param x: число в десятичной системе счисления
    :param return: число в двоичной системе счисления (тип string)
    '''
    n = '' if x > 0 else '0'
    while x > 0:
        y = str(x % 2)
        n = y + n
        x = int(x / 2)
    return n

def bin_generation(n):
    '''
    Функция необходима для генерации набора векторов для фиксированного числа переменных
    Перед каждым набором добавляется x0 = 1
    :param n: число переменных
    :param return: список векторов
    '''
    X = list()
    count = 2**n
    for i in xrange(0, count):
        X.append([int(x) for x in IntToByte(i)])
        while len(X[i]) < 4:
            X[i].insert(0, 0)
        X[i].insert(0, 1) # вставили x0
    return X

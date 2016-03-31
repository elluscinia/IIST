# -*- coding: utf-8 -*-
'''
Модуль с инструментами, облегчающими работу
'''
def not_x(x):
    '''
    Функция получения инверсии
    :param x: элемент
    :param return: инверсия элемента
    '''
    return abs(1-x)

def boolean_function(x1, x2, x3, x4):
    '''
    Фукнция, осуществляющая поиск значения БФ от переданных аргументов
    :param x1:
    :param x2:
    :param x3:
    :param x4:
    :param return: значени БФ на переданных аргументах
    '''
    return not_x(((not_x(x2) or x4) and x1) or (x1 and x3))

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

# -*- coding: utf-8 -*-
'''
Модуль с необходимыми для вычисления параметров НС функциями
'''
from math import exp

def actual_NN(net):
    '''
    Функция вычисления y - реального выхода НС.
    :param net: параметр сетевого/комбинированного входа
    :param retrun: значение реального выхода НС
    '''
    if net > 0:
        return 1
    else:
        return 0

def out(net):
    '''
    Функция получения сетевого (недискретизированного) выхода НС
    :param net: сетевой (комбинированный) вход
    :param return: сетевой выход НС
    '''
    return 1/(1+exp(-net))

def net(W, X):
    '''
    Функция получения сетевого/комбинированного входа
    :param W: вектор весовых коэффициентов
    :param X: вектор текущих значений X: x0 x1 x2 x3 x4
    :prama return: значение сетевого (комбинированного) входа
    '''
    net = 0
    for (w,x) in zip(W[1:], X[1:]):
        net += w*x
    net += W[0]
    return net

def delta(t, y):
    '''
    Функция считает ошибку по текущим значениям целевого и реального выхода
    :param t: целевой выход (значение БФ на текущем векторе X)
    :param y: реальный выход
    :param return: ошибка
    '''
    return t - y

def delta_w(nu, delta, net, x, kind):
    '''
    Функция считает текущее delta w, для корректировки согласно дельта-правилу
    :param nu: норма обучения
    :param delta: ошибка
    :param net: сетевой вход
    :param x: значение текущего х
    :param return: delta w
    '''
    if kind == 'logistics':
        return nu * delta * out(net) * (1 - out(net)) * x
    elif kind == 'threshold':
        return nu * delta * x

def recount_W(W, X, d, n, nu, kind):
    '''
    Функция корректирует вектор весовых коэффициентов согласно дельта-правилу
    и подсчитывает реальный выход НС
    :param F:
    :param W: вектор весовых коэффициентов
    :param X: текущий вектор x0 x1 x2 x3 x4
    :param nu: норма обучения
    :param return: откорректированный вектор весовых коэффициентов
                    и вектор реального выхода НС
    '''
    for (i, w) in enumerate(W):
            W[i] += delta_w(nu, d, n, X[i], kind)
    return W

def totalError(Y, F):
    '''
    Функция считает суммарную квадратичную ошибку
    :param Y: реальный выход
    :param F: целевой выход
    :param return: суммарная квадратичная ошибка
    '''
    E = 0
    for (y, f) in zip(Y, F):
        if y != f:
            E += 1
    return E

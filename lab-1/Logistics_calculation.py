# -*- coding: utf-8 -*-
'''
Модуль с необходимыми для вычисления параметров НС функциями
'''
from Threshold_calculation import actual_NN, net, delta, totalError
from math import exp

def out(net):
    return 1/(1+exp(-net))

def delta_w(nu, delta, net, x):
    '''
    Функция считает текущее delta w, для корректировки согласно дельта-правилу
    :param nu: норма обучения
    :param delta: ошибка
    :param x: значение текущего х
    :param return: delta w
    '''
    return nu * delta * out(net) * (1 - out(net)) * x

def recount_W(W, X, delta, net, nu):
    '''
    Функция корректирует вектор весовых коэффициентов согласно дельта-правилу
    :param W: вектор весовых коэффициентов
    :param X: текущий вектор x0 x1 x2 x3 x4
    :param delta: дельта ошибка
    :param nu: норма обучения
    :param return: откорректированный вектор весовых коэффициентов
    '''
    for i, w in enumerate(W):
        W[i] += delta_w(nu, delta, net, X[i])
    return W

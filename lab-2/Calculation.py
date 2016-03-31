# -*- coding: utf-8 -*-
from math import exp

def phi_function(X, C):
    '''
    Функция расчёта функции гауссовой RBF
    :param X: текущий вектор x
    :param C: текущий центр RBF
    :param return: результат функции
    '''
    p = 0
    for x,c in zip(X[1:], C[1:]):
        p += (x - c)**2
    p = exp(-p)
    return p

def get_phi_array(X, C):
    '''
    Функция создаёт список гауссовых RBF для вектора
    :param X: текущий вектор х
    :param C: центры RBF
    :param return: список гауссовых RBF
    '''
    p_l = list()
    for c in C:
        p_l.append(phi_function(X, c))
    p_l.insert(0, 1)
    return p_l

def net(V, PHI):
    '''
    Функция получения сетевого/комбинированного входа
    :param V: вектор весовых коэффициентов
    :param PHI: вектор гауссовых RBF
    :prama return: значение сетевого (комбинированного) входа
    '''
    n = 0
    for (v,p) in zip(V[1:], PHI[1:]):
        n += v*p
    n += V[0]
    return n

def actual_NN(net):
    '''
    Функция вычисления y - реального выхода НС.
    :param net: параметр сетевого/комбинированного входа
    :param retrun: значение реального выхода НС
    '''
    if net >= 0:
        return 1
    else:
        return 0

def delta(t, y):
    '''
    Функция считает ошибку по текущим значениям целевого и реального выхода
    :param t: целевой выход (значение БФ на текущем векторе X)
    :param y: реальный выход
    :param return: ошибка
    '''
    return t - y

def delta_v(nu, d, p):
    '''
    Функция считает текущее delta w, для корректировки согласно дельта-правилу
    :param nu: норма обучения
    :param delta: ошибка
    :param net: сетевой вход
    :param x: значение текущего х
    :param return: delta w
    '''
    return nu * d * p

def recount_V(V, X, d, nu, phi):
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
    for (i, v) in enumerate(V):
        V[i] += delta_v(nu, d, phi[i])
    return V

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

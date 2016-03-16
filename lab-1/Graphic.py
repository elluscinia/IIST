# -*- coding: utf-8 -*-
'''
Графический модуль для рисования графика
'''

import matplotlib.pyplot as plt

def drawGraph(E, k, name = 'E(k)'):
    '''
    Функция выполняет построение и сохранение графика E(k)
    :param E: вектор суммарных квадратичных ошибок
    :param k:вектор эр
    :param label: имя для сохранения
    :param return: NULL
    '''
    plt.plot(k, E, marker = 'o')
    plt.xlabel('Era  k')
    plt.ylabel('Error  E')
    plt.axis([0, k[-1]+1, 0, max(E)+1])
    plt.title('E(k)')
    plt.grid(True)
    plt.savefig('plt_{0}.png'.format(name))

# -*- coding: utf-8 -*-
'''
Лабораторная работа No 1
Исследование однослойных нейронных сетей на примере
моделирования булевых выражений.

Цель: Исследовать функционирование простейшей нейронной сети (НС) на базе нейрона с
нелинейной функцией активации и ее обучение по правилу Видроу-Хоффа.

Вариант 23.
'''
import sys
from AF import *
from education import *
from Tools import boolean_function, bin_generation, IntToByte

def initialize_components():
    '''
    Функция инциализирует необходимые для расчётов компоненты
    :param return: F - значения БФ, W - начальные весовые коэффициенты
    '''
    W = [0, 0, 0, 0, 0]
    n = 4 # число переменных
    X = bin_generation(n)
    F = get_F(X)
    return F, W

def get_F(X):
    '''
    Функция возвращает значения БФ на заданных ей наборах переменных
    :param X: наборы переменных значения БФ
    :param return: значения БФ
    '''
    F = list()
    for x in X:
        # x0 в расчёт не берётся. Оно необходимо лишь для правила Видроу-Хоффа
        F.append(boolean_function(x[1], x[2], x[3], x[4]))
    return F

def nnm_BF(W, F, outputFile):
    '''
    Функция производит расчёт и построения нейросетевой модели БФ, используя пороговую и логистическую ФА
    :param W: начальные весовые коэффициенты
    :param F: значения БФ
    :param outputFile: имя файла вывода
    :param return: none
    '''
    # Получим нейросетевую модель БФ, используя пороговую ФА
    kind_AF(list(W), list(F), outputFile + '_threshold', 'threshold')

    # Получим нейросетевую модель БФ, используя логистическую ФА
    kind_AF(list(W), list(F), outputFile + '_logistics', 'logistics')

def min_setVectors(W, F, outputFile):
    '''
    Функция производит поиск минимального набора обучающих векторов, используя пороговую и логистическую ФА
    :param W: начальные весовые коэффициенты
    :param F:знаечния БФ
    :param outputFile: имя файла вывода
    :param return: none
    '''
    # Найдем минимальный набор обучающих векторов, используя пороговую ФА
    education_AF(W, F, outputFile + '_education_threshold', 'threshold')

    # Найдем минимальный набор обучающих векторов, используя логистическую ФА
    education_AF(W, F, outputFile + '_education_logistics', 'logistics')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'отсутствует имя файла вывода'
    else:
        # имя файла вывода
        outputFile = sys.argv[1]

        # инициализируем необходимые для расчётов компоненты
        # F - значение БФ
        # W - исходный набор весов
        # n - количество переменных
        F, W = initialize_components()

        nnm_BF(list(W), list(F), outputFile)
        min_setVectors(list(W), list(F), outputFile)

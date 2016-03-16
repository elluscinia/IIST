# -*- coding: utf-8 -*-
'''
Модуль для работы с вводом/выводом данных из программы
'''

def read_Data(path):
    '''
    Функция чтения данных из файла
    :param path: путь к файлу
    :param return: начальный вектор весовых коэффициентов, целевой выход
    '''
    file = open(path)
    data = [line[:-1] for line in file]
    for v in data:
        if v[0] == 'W':
            W = [int(float(i)) for i in v[2:]if i != ' ' ]
        elif v[0] == 'F':
            F = [int(float(i)) for i in v[2:]if i != ' ' ]
    return W, F

def write_Data(file, k, Y, W, E):
    '''
    Функция для записи полученных данных в файл
    :param file: ссылка на объект для записи
    :param k: эпоха
    :param Y: реальный выход
    :param W: вектор весовых коэффициентов
    :param E: суммарная квадратичная ошибка
    :param return: NULL
    '''
    file.write('k = ' + str(k) + '\n')
    file.write('Y = (' + str(Y)[1:-1] + '),\n')
    file.write('W = (' + str(W)[1:-1] + '), E = ' + str(E) + '\n')
    file.write('\n\n')

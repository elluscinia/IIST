# -*- coding: utf-8 -*-

def read_images(fileName):
    '''
    Функция чтения образов из файла
    :param fileName: имя файла
    :param return: прочитанный образ
    '''
    file = open(fileName)
    data = [line[:-1] for line in file] 
    image = list()
    for i in data:
        string = list(i.split('\t'))
        image.append([int(s) for s in string])
    return image
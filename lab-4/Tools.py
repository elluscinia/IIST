# -*- coding: utf-8 -*-
def read_file(path):
    f = open(path)
    data = [line[:-1] for line in f]
    f.close()
    dots = list()
    for i in data:
        string = list(i.split('\t'))
        dots.append([int(s) for s in string])
    return dots

def metrics_Manhattan (A, B):
    result = 0
    for a,b in zip(A,B):
        result += abs(a-b)
    return result

def metrics_Chebyshev (A, B):
    return max([abs(a-b) for a,b in zip(A,B)])

def clustering (dot, clusters, metrics):
    if metrics == 'Manhattan':
        classes = [metrics_Manhattan(dot, cluster) for cluster in clusters]
        return clusters[classes.index(min(classes))]
    elif metrics == 'Chebyshev':
        classes = [metrics_Chebyshev(dot, cluster) for cluster in clusters]
        return clusters[classes.index(min(classes))]

def kohonen (dots, centers, metrics):
    return [clustering(dot, centers, metrics) for dot in dots]

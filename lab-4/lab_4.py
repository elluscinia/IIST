# -*- coding: utf-8 -*-
from random import randint
from Tkinter import *
from tkFileDialog import *

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

class Clusterization():
    def __init__ (self):

        self.colors = ['black', 'green', 'blue', 'red', 'magenta', 'grey', 'cyan']

        self.dots = list()
        self.centers = list()

        self.window = Tk()
        self.window.title('Kohonen')
        self.window.geometry('1000x900+100+100')
        self.window.resizable(False, False)

        self.drawing_area = Canvas(self.window, width=980, height=690, bd=7, cursor = 'dot')
        self.drawing_area.place(x = 15, y = 25, width = 900)
        self.drawing_area.bind("<ButtonPress-1>", self.draw_dots)
        self.drawing_area.bind("<ButtonPress-3>", self.draw_centers)

        self.button_manhattan = Button(self.window, bd = 2, text = 'Manhattan', width = 30, height = 1, relief=RIDGE)
        self.button_manhattan.place(x = 10, y = 800, width = 90)
        self.button_manhattan.bind('<Button-1>', self.manhattan)

        self.button_chebyshev = Button(self.window, bd = 2, text = 'Chebyshev', width = 30, height = 1, relief=RIDGE)
        self.button_chebyshev.place(x = 110, y = 800, width = 90)
        self.button_chebyshev.bind('<Button-1>', self.chebyshev)

        self.button_upload_dots = Button(self.window, bd = 2, text = 'Upload dots', width = 30, height = 1, relief=RIDGE)
        self.button_upload_dots.place(x = 210, y = 800, width = 90)
        self.button_upload_dots.bind('<Button-1>', self.upload_dots)

        self.button_upload_centers = Button(self.window, bd = 2, text = 'Upload centers', width = 30, height = 1, relief=RIDGE)
        self.button_upload_centers.place(x = 310, y = 800, width = 90)
        self.button_upload_centers.bind('<Button-1>', self.upload_centers)

        self.button_clear_all = Button(self.window, bd = 2, text = 'C L E A R  A L L', width = 30, height = 1, relief=RIDGE)
        self.button_clear_all.place(x = 210, y = 850, width = 200)
        self.button_clear_all.bind('<Button-1>', self.reset)

        # self.button_write = Button(self.window, bd = 2, text = 'Write data to file', width = 30, height = 1, relief=RIDGE)
        # self.button_write.place(x = 510, y = 850, width = 200)
        #self.button_upload_centers.bind('<Button-1>', self.write_to_file)

    def manhattan(self, event):
        clusters = kohonen(self.dots, self.centers, 'Manhattan')
        self.drawing_area.delete('all')
        for i,center in enumerate(self.centers):
            cl = list()
            for dot,cluster in zip(self.dots,clusters):
                if cluster == center:
                    cl.append(dot)
            cl.insert(0, center)
            x_center = cl[0][0]
            y_center = cl[0][1]
            self.drawing_area.create_oval(x_center, y_center, x_center + 7, y_center + 7, width=1, fill=self.colors[i+1], dash=(4, 4))
            for c in cl[1:]:
                x = c[0]
                y = c[1]
                self.drawing_area.create_oval(x, y, x + 7, y + 7, width=1, fill=self.colors[i+1])


    def chebyshev(self, event):
        clusters = kohonen(self.dots, self.centers, 'Chebyshev')
        self.drawing_area.delete('all')
        for i,center in enumerate(self.centers):
            cl = list()
            for dot,cluster in zip(self.dots,clusters):
                if cluster == center:
                    cl.append(dot)
            cl.insert(0, center)
            x_center = cl[0][0]
            y_center = cl[0][1]
            self.drawing_area.create_oval(x_center, y_center, x_center + 7, y_center + 7, width=1, fill=self.colors[i+1], dash=(4, 4))
            for c in cl[1:]:
                x = c[0]
                y = c[1]
                self.drawing_area.create_oval(x, y, x + 7, y + 7, width=1, fill=self.colors[i+1])


    def draw_dots(self, event):
        event.widget.create_oval(event.x, event.y, event.x + 7, event.y + 7, width=1, fill=self.colors[0])
        self.dots.append([event.x, event.y])


    def draw_centers(self, event):
        event.widget.create_oval(event.x, event.y, event.x + 7, event.y + 7, width=1, fill=self.colors[1], dash=(4, 4))
        self.centers.append([event.x, event.y])

    def upload_dots(self, event):
        Tk().withdraw()
        filename = askopenfilename()
        self.dots += list(read_file(filename))
        for dot in self.dots:
            x = dot[0]
            y = dot[1]
            self.drawing_area.create_oval(x, y, x + 7, y + 7, width=1, fill=self.colors[0])


    def upload_centers(self, event):
        Tk().withdraw()
        filename = askopenfilename()
        self.centers += list(read_file(filename))
        for dot in self.dots:
            x = dot[0]
            y = dot[1]
            self.drawing_area.create_oval(x, y, x + 7, y + 7, width=1, fill=self.colors[1], dash=(4, 4))


    def reset (self, event):
        self.drawing_area.delete('all')
        self.dots = list()
        self.centers = list()

    def run (self):
        self.window.mainloop()


if __name__ == '__main__':
    window = Clusterization()
    window.run()

    
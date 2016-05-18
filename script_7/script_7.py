#!/usr/bin/env python

import os
import random
from datetime import datetime

from PIL import Image, ImageFilter, ImageDraw

def convex_hull(points):
    #https://en.wikibooks.org/wiki/Algorithm_Implementation/Geometry/Convex_hull/Monotone_chain
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]

class Grid(object):
    def __init__(self, size, draw):
        self._list = [[None]*size]*size
        self.draw = draw

    def insert_polygon_at(self, line, column, polygon):
        self._list[line][column] = polygon

class Subspace(object):
    
    def __init__(self, x_start, y_start, x_end, y_end, draw_subspace = False):
        self.x0 = x_start
        self.y0 = y_start
        self.x1 = x_end
        self.y1 = y_start
        self.x2 = x_end
        self.y2 = y_end
        self.x3 = x_start
        self.y3 = y_end

        if draw_subspace:
            draw_subspace.rectangle([self.x0, self.y0, self.x2, self.y2], outline = "grey")

    def __repr__(self):
        return 'Subspace(x0: %s, y0: %s, x2: %s, y2: %s)'%(self.x0, self.y0, self.x2, self.y2)

    def is_in_subspace(self, line):
        pass

class Line(object):
    def __init__(self, x_start, y_start, x_end, y_end):
        self.x_0 = x_start
        self.y_0 = y_start
        self.x_1 = x_end
        self.y_1 = y_end

class Polygon(object):
    def __init__(self):
        self.points = []

    def add_point(self, x, y):
        self.points.append((x, y))

    def draw(self, draw):
        points = convex_hull(self.points)
        draw.polygon(points, outline = 'black')

def get_parallel_offset_line(line, distance):
    return parallel_line

def draw_polygon(grid, subspace):
    polygon = Polygon()

    print 'Subspace', subspace
    #nb_side = random.randint(3,4)
    nb_side = 4
    print '#'*80
    for i in xrange(nb_side):
        if i == 0:
            min_x = subspace.x0
            min_y = subspace.y0
            max_x = (subspace.x2 - subspace.x0)/2 + subspace.x0
            max_y = (subspace.y2 - subspace.y0)/2 + subspace.y0
        elif i == 1:
            min_x = (subspace.x2 - subspace.x0)/2 + subspace.x0
            min_y = subspace.y0
            max_x = subspace.x2
            max_y = (subspace.y2 - subspace.y0)/2 + subspace.y0
        elif i == 2:
            min_x = (subspace.x2 - subspace.x0)/2 + subspace.x0
            min_y = (subspace.y2 - subspace.y0)/2 + subspace.y0
            max_x = subspace.x2
            max_y = subspace.y2
        else:
            min_x = subspace.x0
            min_y = (subspace.y2 - subspace.y0)/2 + subspace.y0
            max_x = (subspace.x2 - subspace.x0)/2 + subspace.x0
            max_y = subspace.y2

        print 'i', i
        print 'min_x', min_x, 'max_x', max_x
        print 'min_y', min_y, 'max_y', max_y
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)

        polygon.add_point(x, y)

    polygon.draw(grid.draw)

    return polygon

def progression():
    nb_polygon_by_line = 30
    size_length = 20
    margin = 20
    canvas_size = (nb_polygon_by_line * size_length) + (margin * 2)

    canvas = Image.frombytes('RGBA', (canvas_size, canvas_size),  '\xFF\xFF\xFF\xFF' * canvas_size * canvas_size)
    draw = ImageDraw.Draw(canvas)

    grid = Grid(nb_polygon_by_line, draw)
    for i in xrange(nb_polygon_by_line):
        for j in xrange(nb_polygon_by_line):
            print '%'*80
            print 'r', i
            print 'c', j
            x_s = margin + (size_length * i)
            y_s = margin + (size_length * j)
            x_e = x_s + size_length
            y_e = y_s + size_length
            subspace = Subspace(x_s, y_s, x_e, y_e, draw_subspace = False)
            polygon = draw_polygon(grid, subspace)
            grid.insert_polygon_at(i, j, polygon)

    canvas = canvas.filter(ImageFilter.GaussianBlur(0.5))

    directory = "results"
    if not os.path.exists(directory):
        os.makedirs(directory)

    now = datetime.now().strftime("%H-%M-%S")
    file_path = os.path.join(directory, "%s-%s.jpg"%(__file__[:-3], now))
    canvas.save(file_path)
    canvas.show()

if __name__ == '__main__':
    progression()

#!/usr/bin/env python

import os
import random
from datetime import datetime

from PIL import Image, ImageFilter, ImageDraw

DRAW_RECT = [0, 0, 0, 0]
DRAW_RECT[1] = [False]
DRAW_RECT[2] = [False, False, False, True, True, True, True]
DRAW_RECT[3] = [False, True, True]

COLORS = [
    '#f4f4f4', #White
    '#f4f4f4', #White
    '#f4f4f4', #White
    '#f43530', #Red
    '#f43530', #Red
    '#e6c700', #Yellow
    '#008cbc'  #Blue
]

CONTOUR_SIZE = 2
CANVAS_SIZE = 500

def divide_cadran(coord_area):

    x_0 = coord_area[0]
    y_0 = coord_area[1]
    x_1 = coord_area[2]
    y_1 = coord_area[3]

    coord_area_list = []

    coord_area_1 = [0]*4
    coord_area_1[0] = x_0
    coord_area_1[1] = y_0
    coord_area_1[2] = (x_1/2)+(x_0/2)
    coord_area_1[3] = (y_1/2)+(y_0/2)
    coord_area_list.append(coord_area_1)

    coord_area_2 = [0]*4
    coord_area_2[0] = (x_1/2)+(x_0/2)
    coord_area_2[1] = y_0
    coord_area_2[2] = x_1
    coord_area_2[3] = (y_1/2)+(y_0/2)
    coord_area_list.append(coord_area_2)

    coord_area_3 = [0]*4
    coord_area_3[0] = x_0
    coord_area_3[1] = (y_1/2)+(y_0/2)
    coord_area_3[2] = (x_1/2)+(x_0/2)
    coord_area_3[3] = y_1
    coord_area_list.append(coord_area_3)

    coord_area_4 = [0]*4
    coord_area_4[0] = (x_1/2)+(x_0/2)
    coord_area_4[1] = (y_1/2)+(y_0/2)
    coord_area_4[2] = x_1
    coord_area_4[3] = y_1
    coord_area_list.append(coord_area_4)

    return coord_area_list

def draw_rectangle(draw, coord, color = False, draw_contour = True):
    effective_coord = coord

    if not color:
        color = get_random_color()

    if draw_contour:
        effective_coord[0] += CONTOUR_SIZE
        effective_coord[1] += CONTOUR_SIZE
        effective_coord[2] -= CONTOUR_SIZE
        effective_coord[3] -= CONTOUR_SIZE

    draw.rectangle(effective_coord, fill = color)

def get_random_color():
    return random.choice(COLORS)

def draw_on_cadran(**kwargs):
    coord_area = kwargs.get('coord_area', None)
    round_index = kwargs.get('round_index', 0)
    number_of_round = kwargs.get('number_of_round', 4)
    draw_contour = kwargs.get('draw_contour', True)

    #Divide
    if round_index < number_of_round:
        if round_index:
            draw_rect = random.choice(DRAW_RECT[round_index])
        else:
            draw_rect = False

        if draw_rect:
            draw_rectangle(kwargs.get('draw'), coord_area, draw_contour = draw_contour)
        else:
            kwargs['round_index'] = round_index+1
            cadrans = divide_cadran(coord_area)
            for cadran in cadrans:
                kwargs['coord_area'] = cadran
                draw_on_cadran(**kwargs)

    #Draw rectangle
    else:
        draw_rectangle(kwargs.get('draw'), coord_area, draw_contour = draw_contour)


def composition_mondrian():
    canvas = Image.frombytes('RGBA', (CANVAS_SIZE, CANVAS_SIZE),  '\x00\x00\x00\x00' * CANVAS_SIZE * CANVAS_SIZE)
    draw = ImageDraw.Draw(canvas)

    config = {}
    config['number_of_round'] = 4 #Value of 4 or below
    config['coord_area'] = [0, 0, CANVAS_SIZE, CANVAS_SIZE]
    config['draw'] = draw
    config['draw_contour'] = True
    draw_on_cadran(**config)

    canvas = canvas.filter(ImageFilter.GaussianBlur(2))

    directory = "results"
    if not os.path.exists(directory):
        os.makedirs(directory)

    now = datetime.now().strftime("%H-%M-%S")
    file_path = os.path.join(directory, "%s-%s.jpg"%(__file__[:-3], now))
    canvas.save(file_path)
    canvas.show()

if __name__ == '__main__':
    composition_mondrian()

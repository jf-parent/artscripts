#!/usr/bin/env python

import os
import random
from datetime import datetime

from PIL import Image, ImageFilter, ImageDraw

WIDTH_LIST = [2] * 10 + [3] * 8 + [4] * 5 + [5] * 3 + [6] * 1

PLUS = [False, True]

BACKGROUND_COLORS = [
    '#decfca',
    '#bbc2c4',
    '#edea9a', #Beige
    '#f4f4f4', #White
]

FORCE_COLORS = [
    '#f4f4f4', #White
]

COLORS = [
    '#f53d00', #Orange
    '#f43530', #Red
    '#ed1135', #Red
    '#e6c700', #Yellow
    '#d3e03a', #Yellow
    '#11edc9', #Blue
    '#008cbc', #Blue
    '#3ab7e0', #Blue
    '#1f1d1c', #Black
]

CANVAS_SIZE = 500

def draw_slide(draw, color):
    coord = [random.randint(0, CANVAS_SIZE),random.randint(0, CANVAS_SIZE),random.randint(0, CANVAS_SIZE),random.randint(0, CANVAS_SIZE)]
    for i in range(random.randint(40, 50)):
        coord[0] = coord[2]
        coord[1] = coord[3]
        coord[2] += random.randint(-30, 30)
        coord[3] += random.randint(-30, 30)
        draw.line(coord, fill = color, width = random.choice(WIDTH_LIST))

        splash_coord = [coord[0], coord[1]]
        for i in range(100):
            plus = random.choice(PLUS)
            if plus:
                splash_coord[0] += random.randint(1, 2)%2
                splash_coord[1] -= random.randint(1, 2)%2
            else:
                splash_coord[0] -= random.randint(1, 2)%2
                splash_coord[1] += random.randint(1, 2)%2
            draw.point(splash_coord, fill = color)

def drip_pollock():
    canvas = Image.frombytes('RGBA', (CANVAS_SIZE, CANVAS_SIZE),  '\x00\x00\x00\x00' * CANVAS_SIZE * CANVAS_SIZE)

    #Create background
    draw = ImageDraw.Draw(canvas)
    bg_color = random.choice(BACKGROUND_COLORS)
    nb_round_bg = random.randint(200, 240)
    for i in range(nb_round_bg):
        draw_slide(draw, bg_color)

    canvas = canvas.filter(ImageFilter.GaussianBlur(8))

    color_slide = [
        FORCE_COLORS[0],
        random.choice(COLORS),
        random.choice(COLORS),
        random.choice(COLORS),
        random.choice(COLORS)
    ]
    draw = ImageDraw.Draw(canvas)
    for _ in range(random.randint(80, 100)):
        color = random.choice(color_slide)
        draw_slide(draw, color)
    canvas = canvas.filter(ImageFilter.GaussianBlur(1))

    directory = "results"
    if not os.path.exists(directory):
        os.makedirs(directory)

    now = datetime.now().strftime("%H-%M-%S")
    file_path = os.path.join(directory, "%s-%s.jpg"%(__file__[:-3], now))
    canvas.save(file_path)
    canvas.show()

if __name__ == '__main__':
    drip_pollock()

#!/usr/bin/env python

import os
import random
from datetime import datetime

from PIL import Image, ImageFilter, ImageDraw

CHARS = ['a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
CANVAS_SIZE = 500

def get_random_color():
    color = []
    for i in range(6):
        color.append(random.choice(CHARS))

    return '#%s'%''.join(color)

def spectrum():
    canvas = Image.frombytes('RGBA', (CANVAS_SIZE, CANVAS_SIZE),  '\xFF\xFF\xFF\x00' * CANVAS_SIZE * CANVAS_SIZE)
    draw = ImageDraw.Draw(canvas)

    nb_square_by_line = 30
    square_size = CANVAS_SIZE / nb_square_by_line
    l_offset = 10
    for i in range(nb_square_by_line):
        for j in range(nb_square_by_line):
            if i <= 5 or \
                    i >= nb_square_by_line - 5 or \
                    j <= 5 or \
                    j >= nb_square_by_line - 5:
                is_not_white = random.randint(0, 1)
            else:
                is_not_white = random.randint(0, 2)

            if is_not_white:
                color = get_random_color()

                x0 = i * square_size + l_offset
                y0 = j * square_size + l_offset
                x1 = x0 + square_size
                y1 = y0 + square_size
                draw.rectangle([x0, y0, x1, y1], fill = color)

    canvas = canvas.filter(ImageFilter.GaussianBlur(0.5))

    directory = "results"
    if not os.path.exists(directory):
        os.makedirs(directory)

    now = datetime.now().strftime("%H-%M-%S")
    file_path = os.path.join(directory, "%s-%s.jpg"%(__file__[:-3], now))
    canvas.save(file_path)
    canvas.show()

if __name__ == '__main__':
    spectrum()

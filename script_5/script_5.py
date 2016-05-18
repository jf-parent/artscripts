#!/usr/bin/env python

import os
import random
from datetime import datetime

from PIL import Image, ImageFilter, ImageDraw

CHARS = ['a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def get_random_color():
    color = []
    for i in range(6):
        color.append(random.choice(CHARS))

    return '#%s'%''.join(color)

def color_for_large_wall():
    nb_square_by_line = random.randint(5, 15)
    square_size = 500 / nb_square_by_line
    canvas_size = square_size * nb_square_by_line

    canvas = Image.frombytes('RGBA', (canvas_size, canvas_size),  '\x00\x00\x00\x00' * canvas_size * canvas_size)
    draw = ImageDraw.Draw(canvas)

    for i in range(nb_square_by_line):
        for j in range(nb_square_by_line):
            x0 = i * square_size
            y0 = j * square_size
            x1 = x0 + square_size
            y1 = y0 + square_size
            draw.rectangle([x0, y0, x1, y1], fill = get_random_color())

    canvas = canvas.filter(ImageFilter.GaussianBlur(1))

    directory = "results"
    if not os.path.exists(directory):
        os.makedirs(directory)

    now = datetime.now().strftime("%H-%M-%S")
    file_path = os.path.join(directory, "%s-%s.jpg"%(__file__[:-3], now))
    canvas.save(file_path)
    canvas.show()

if __name__ == '__main__':
    color_for_large_wall()

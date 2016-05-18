#!/usr/bin/env python

import os
import random
from datetime import datetime

from PIL import Image, ImageFilter, ImageDraw

CHARS = ['a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
CANVAS_SIZE = 500

def get_random_color():
    color = '#%s%s%s%s%s%s'%(
        random.choice(CHARS),
        random.choice(CHARS),
        random.choice(CHARS),
        random.choice(CHARS),
        random.choice(CHARS),
        random.choice(CHARS)
    )
    return color

def combination_238():
    canvas = Image.frombytes('RGBA', (CANVAS_SIZE, CANVAS_SIZE),  '\x00\x00\x00\x00' * CANVAS_SIZE * CANVAS_SIZE)
    draw = ImageDraw.Draw(canvas)

    width_rect = float(CANVAS_SIZE)/17
    height_rect = float(CANVAS_SIZE)/14
    for i in xrange(17):
        for j in xrange(7):
            first_color = get_random_color()
            second_color = get_random_color()
            rect_1_x1 = (i*width_rect)
            rect_1_y1 = (j*height_rect)*2
            rect_1_x2 = rect_1_x1+width_rect
            rect_1_y2 = rect_1_y1+height_rect
            draw.rectangle([rect_1_x1, rect_1_y1, rect_1_x2, rect_1_y2], fill = first_color)

            triangle_1_x1 = rect_1_x1 + (width_rect / 2)
            triangle_1_y1 = rect_1_y1
            triangle_1_x2 = rect_1_x2
            triangle_1_y2 = rect_1_y1 + (height_rect / 2)
            triangle_1_x3 = triangle_1_x1
            triangle_1_y3 = rect_1_y2
            triangle_1_x4 = rect_1_x1
            triangle_1_y4 = triangle_1_y2
            draw.polygon([triangle_1_x1, triangle_1_y1, triangle_1_x2, triangle_1_y2, triangle_1_x3, triangle_1_y3, triangle_1_x4, triangle_1_y4], fill = second_color)

            rect_2_x1 = (i*width_rect)
            rect_2_y1 = rect_1_y2
            rect_2_x2 = rect_2_x1+width_rect
            rect_2_y2 = rect_2_y1+height_rect
            draw.rectangle([rect_2_x1, rect_2_y1, rect_2_x2, rect_2_y2], fill = second_color)

            triangle_2_x1 = rect_2_x1 + (width_rect / 2)
            triangle_2_y1 = rect_2_y1
            triangle_2_x2 = rect_2_x2
            triangle_2_y2 = rect_2_y1 + (height_rect / 2)
            triangle_2_x3 = triangle_2_x1
            triangle_2_y3 = rect_2_y2
            triangle_2_x4 = rect_2_x1
            triangle_2_y4 = triangle_2_y2
            draw.polygon([triangle_2_x1, triangle_2_y1, triangle_2_x2, triangle_2_y2, triangle_2_x3, triangle_2_y3, triangle_2_x4, triangle_2_y4], fill = first_color)

    canvas = canvas.filter(ImageFilter.GaussianBlur(1))

    directory = "results"
    if not os.path.exists(directory):
        os.makedirs(directory)

    now = datetime.now().strftime("%H-%M-%S")
    file_path = os.path.join(directory, "%s-%s.jpg"%(__file__[:-3], now))
    canvas.save(file_path)
    canvas.show()

if __name__ == '__main__':
    combination_238()

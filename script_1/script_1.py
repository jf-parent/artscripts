#!/usr/bin/env python

import os
import inspect
from datetime import datetime
from random import randint
from sys import platform as _platform

from PIL import Image, ImageFilter, ImageDraw, ImageFont

def main():
    canvas_size = 500
    canvas = Image.frombytes('RGBA', (canvas_size, canvas_size),  '\x00\x00\x00\x00' * canvas_size * canvas_size)

    draw = ImageDraw.Draw(canvas)
    
    #RECTANGLE
    x_s = 0
    y_s = canvas_size/2
    x_e = canvas_size
    y_e = canvas_size

    draw.rectangle([(x_s, y_s), (x_e, y_e)], fill = '#db2f27')

    draw.ellipse((-200, 350, 250, 700), fill = '#fbae17')
    for i in range(4):
        x_s = randint(50,150)
        y_s = randint(300, 350)
        x_e = x_s+20
        y_e = y_s+20
        draw.ellipse((x_s, y_s, x_e, y_e), fill = '#fbae17')

    for i in range(3):
        x_s = randint(100,300)
        y_s = randint(300, 375)
        x_e = x_s+20
        y_e = y_s+20
        draw.ellipse((x_s, y_s, x_e, y_e), fill = '#f7772c')

    canvas = canvas.filter(ImageFilter.GaussianBlur(2))

    draw = ImageDraw.Draw(canvas)
    #Line
    for i in range(50):
        x_s = canvas_size
        y_s = 0
        x_e = (canvas_size/2)-(i*10)
        y_e = (canvas_size/2)-1
        draw.line((x_s, y_s, x_e, y_e), fill="white")

    canvas = canvas.filter(ImageFilter.GaussianBlur(1))

    draw = ImageDraw.Draw(canvas)
    #Code
    if _platform == "linux" or _platform == "linux2":
        font_path = '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf'
    elif _platform == "darwin":
        font_path = '/Library/Fonts/Arial.ttf'

    fnt = ImageFont.truetype(font_path, 5)
    text = inspect.getsource(main)
    x = 50
    y = 10
    draw.multiline_text((x, y), text, font=fnt, fill=(255,255,255,128))

    directory = "results"
    if not os.path.exists(directory):
        os.makedirs(directory)

    now = datetime.now().strftime("%H-%M-%S")
    file_path = os.path.join(directory, "script_1-%s.jpg"%now)
    canvas.save(file_path)
    print 'Result located at', file_path
    canvas.show()

if __name__ == '__main__':
    main()

#!/usr/bin/env python

import sys, termios, tty, os, time, threading

import cv2
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

 
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

cam = cv2.VideoCapture(0)

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1 
options.parallel = 1
options.hardware_mapping = 'regular'  
matrix = RGBMatrix(options = options)

left = 0
top = 0
right = 0
bottom = 0
crop_coords = (left, top, right, bottom)

ret, frame = cam.read()

cv2_im = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
image = Image.fromarray(cv2_im)

width, height = image.size
print(image.size)

AR_WIN = matrix.width / matrix.height
AR_IMG = width/height
W_WIN = None
H_WIN = None


if AR_WIN > AR_IMG:
    W_WIN = width
    H_WIN = W_WIN / AR_WIN
else:
    H_WIN = height
    W_WIN = H_WIN * AR_WIN


right = left + W_WIN
bottom = top + H_WIN
crop_coords = (left, top, right, bottom)

key = ""



translation_delta = 10

running = True

def capture_frame():
    global crop_coords
    global matrix
    global cam
    global running

    while running:
    
        ret, frame = cam.read()
        
        cv2_im = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        image = Image.fromarray(cv2_im)
        
        image = image.crop(crop_coords)
    
        # Make image fit our screen.
        image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
        
        matrix.SetImage(image.convert('RGB'))
    return


led = threading.Thread(target=capture_frame)
led.start()

def get_key():
    global running
    global crop_coords
    global left
    global top
    global right
    global bottom
    global translation_delta
    global H_WIN
    global W_WIN
    global led
    
    scaling_factor = 1.1

    while True:
        key = getch()
        print(key)
        print(crop_coords)
        if key == "c":
            running = False
            led.join()
            return

        if key == "w":
            top -= translation_delta
            
        elif key == "a":
            left -= translation_delta

        elif key == "s":
            top += translation_delta

        elif key == "d":
            left += translation_delta

        elif key == "-":
            top -= H_WIN * (scaling_factor - 1.0) / 2
            left -= W_WIN * (scaling_factor - 1.0) / 2
            W_WIN *= scaling_factor
            H_WIN *= scaling_factor
        elif key == "=":
            top -= H_WIN * ((1.0/scaling_factor) - 1.0) / 2
            left -= W_WIN * ((1.0/scaling_factor) - 1.0) / 2
            W_WIN *= 0.9
            H_WIN *= 0.9

        
        left = max(0, left)
        top = min(height - H_WIN, top)
        left = min(width - W_WIN, left)
        top = max(0, top)
        bottom = top + H_WIN
        right = left + W_WIN
        crop_coords = (left, top, right, bottom)
    
        

try:
    get_key()
except:
    print(sys.exc_info())

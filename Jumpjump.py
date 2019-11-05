import autopy
import time
from PIL import ImageGrab
from math import *
time.sleep(2)
def checking_left_or_right(im):
    x=322
    y=281
    im_colour=im.getpixel((322,281))
    Red = im_colour[0]
    Green = im_colour[1]
    Blue = im_colour[2]
    for y in range(420,550):
        for x in range(470,660):
            pixel_colour=im.getpixel((x,y))
            if (abs(pixel_colour[0] - Red) + abs(pixel_colour[1] - Green) + abs(pixel_colour[2] - Blue)) >= 15:
                return 'Left'
    return 'Right'

def get_target_coordinate_left(im):

    x=322
    y=281
    im_colour=im.getpixel((x,y))
    Red=im_colour[0]
    Green=im_colour[1]
    Blue=im_colour[2]
    top_coordinate=[0,0]
    bottom_coordinate=[0,0]
    for y in range(350,720):
        for x in range(500,670):
            pixel_colour=im.getpixel((x,y))
            if (abs(pixel_colour[0] - Red) + abs(pixel_colour[1] - Green) + abs(pixel_colour[2] - Blue)) >= 10:
                pixel_colour=im.getpixel((x,y+5))
                Red=pixel_colour[0]
                Green=pixel_colour[1]
                Blue=pixel_colour[2]
                top_coordinate=[x,y]
                for b in range(y+5, 720):
                    pixel_colour=im.getpixel((x,b))
                    if (abs(pixel_colour[0] - Red) + abs(pixel_colour[1] - Green) + abs(pixel_colour[2] - Blue)) >= 10:
                        bottom_coordinate=[x,b]
                        return (x, (top_coordinate[1]+bottom_coordinate[1])/2)
    return False

def get_target_coordinate_right(im):
    x=322
    y=281
    im_colour=im.getpixel((x,y))
    Red=im_colour[0]
    Green=im_colour[1]
    Blue=im_colour[2]
    top_coordinate=[0,0]
    bottom_coordinate=[0,0]
    for y in range(360,580):
        for x in range(800,1040):
            pixel_colour=im.getpixel((x,y))
            if (abs(pixel_colour[0] - Red) + abs(pixel_colour[1] - Green) + abs(pixel_colour[2] - Blue)) >= 10:
                pixel_colour=im.getpixel((x,y+5))
                Red=pixel_colour[0]
                Green=pixel_colour[1]
                Blue=pixel_colour[2]
                top_coordinate=[x,y]
                for b in range(y+5, 720):
                    pixel_colour=im.getpixel((x,b))
                    if (abs(pixel_colour[0] - Red) + abs(pixel_colour[1] - Green) + abs(pixel_colour[2] - Blue)) >= 10:
                        bottom_coordinate=[x,b]
                        return (x, (top_coordinate[1]+bottom_coordinate[1])/2)
    return False

def calculate_distance(image, initial_coordinate=(735,585)):
    direction=checking_left_or_right(image)
    if direction == 'Left':
        target_coordinate=get_target_coordinate_left(image)
    else:
        target_coordinate=get_target_coordinate_right(image)
    distance = sqrt((target_coordinate[0]-initial_coordinate[0])**2+(target_coordinate[1]-initial_coordinate[1])**2)
    return distance

ending_pixel_colour=(0,0,0)
while ending_pixel_colour[0] not in range (250,256):
    im = ImageGrab.grab()
    distance = calculate_distance(im)
    autopy.mouse.toggle(None,True)
    time.sleep(distance / 550)
    autopy.mouse.toggle(None,False)
    ending_pixel_colour = im.getpixel((712, 320))
    time.sleep(2)



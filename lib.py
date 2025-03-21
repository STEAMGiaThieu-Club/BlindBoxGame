import pygame as window
import serial
from time import sleep as delay
from os import system
import csv
import random

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
PINK = (255, 192, 203)
WIDTH, HEIGHT = 1600, 900

square_size = 120
box_height = square_size
box_width = square_size

box_quantity = 0
item_dict = {}
chance_dict = {}

opened_box_link = "img/open.png"
closed_box_link = "img/closed.png"

logging = True
# logging = False
def log(*args):
    if logging:
        print(*args)

class BlindBox:
    def __init__(self, image, name):
        self.image = image
        self.name = name

alert_height = 400
alert_width = 600
alert_displayed = False
alert_text = "sample"
alert_image = "sample.jpg"
alert_image_height = 200
alert_image_width = 200
alert_image_downshift = 50
alert_text_upshift = 30
alert_font_size = 50

data_displayed = False
data_displayed_height = 500
data_displayed_width = 800
font_size = 35
line_spacing = 40
left_margin = 50


from pico2d import *

class Cursor:
    image = None
    x,y=600,300
    IDLE, PAPER, ROCK = 0, 1, 2
    def __init__(self):
        self.state= self.IDLE
        if Cursor.image == None:
            Cursor.image =  load_image('Main_Map/cursor.png')

    def draw(self):
        hide_cursor()
        self.image.clip_draw(35*self.state, 0, 35, 35, Cursor.x+10,Cursor.y-10)
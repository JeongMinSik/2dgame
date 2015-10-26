import game_framework
import title_state
import class_cursor
from pico2d import *

name = "StartState"
image = None
logo_time = 0.0

def enter(object1=None,object2=None):
    global image
    open_canvas(1200,600,True)
    image = load_image('kpu_credit.png')


def exit():
    global image
    del(image)
    close_canvas()

def update(frame_time):
    global logo_time
    if(logo_time > 1):
        logo_time = 0
        game_framework.push_state(title_state)
    logo_time +=frame_time

def draw(frame_time):
    global image
    clear_canvas()
    image.draw(600,300)
    update_canvas()

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if(event.type == SDL_MOUSEMOTION):
            class_cursor.Cursor.x, class_cursor.Cursor.y=event.x,600-event.y


def pause(): pass
def resume(): pass
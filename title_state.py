import game_framework
from pico2d import *
import main_state
import class_cursor


name = "TitleState"
image = None

def enter(object1=None,object2=None):
    global back_image,space_image, name_image, opacify_time,change, name_x, cursor
    back_image = load_image('Title/title_01.png')
    space_image = load_image('Title/space_bar.png')
    name_image = load_image('Title/title_name_2.png')
    opacify_time, change=0, 1
    name_x = 1500
    cursor=class_cursor.Cursor()

def exit():
    global image
    del(image)


def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    global name_x
    events=get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif(event.type == SDL_MOUSEMOTION):
            class_cursor.Cursor.x,class_cursor.Cursor.y=event.x,600-event.y
        else:
            if(event.type, event.key) == (SDL_KEYDOWN,SDLK_ESCAPE):
                game_framework.quit()
            elif(event.type, event.key) == (SDL_KEYDOWN,SDLK_SPACE):
                if name_x != 365:
                    name_x =365
                else:
                    game_framework.change_state(main_state)


def update(frame_time):
    global space_image, opacify_time, change, name_x
    opacify_time +=frame_time*change
    if opacify_time >1:
        opacify_time =1
        change = -1
    elif opacify_time <0.1:
        opacify_time =0.1
        change = 1
    if name_x > 365:
        name_x -=15
        opacify_time =0
    else: name_x = 365
    space_image.opacify(opacify_time)


def draw(frame_time):
    clear_canvas()
    back_image.draw(600,300)
    name_image.draw(name_x,520)
    if name_x == 365:
        space_image.draw(900,60)
    cursor.draw()
    update_canvas()




import game_framework
from pico2d import *
import main_state
import class_cursor

name = "TitleState"

NEW_GAME, LOAD_GAME, HELP = 1, 2, 3

def enter(object1=None,object2=None):
    global back_image,space_image, name_image, opacify_time,change, name_x, cursor,bgm,select_menu, newgame_image, loadgame_image, help_image, readme_image,ishelp
    bgm=load_music('Sound/title_bgm.mp3')
    bgm.set_volume(40)
    bgm.repeat_play()

    back_image = load_image('Title/title_01.png')
    space_image = load_image('Title/space_bar.png')
    name_image = load_image('Title/title_name_2.png')
    newgame_image = load_image('Title/newgame.png')
    loadgame_image = load_image('Title/loadgame.png')
    help_image = load_image('Title/help.png')
    readme_image = load_image('Title/readme.png')
    readme_image.opacify(0.9)

    select_menu = False
    ishelp = False

    opacify_time, change=0, 1
    name_x = 1500

    cursor=class_cursor.Cursor()

def exit():
    print("타이틀 exit")
    global back_image,space_image, name_image, help_image, readme_image
    del(back_image,space_image, name_image, readme_image)


def pause():
    print("타이틀 pause")

def resume():
    print("타이틀 resume")
    global select_menu,name_x
    bgm.repeat_play()
    select_menu = False
    name_x = 1500


def check_click(x,y):
    if x < 850 : return False
    if x > 1150 : return False
    if y > 400: return False
    if y < 35: return False
    if y > 300: return NEW_GAME
    if y < 270 and y > 160: return LOAD_GAME
    if y < 140: return HELP
    return False

def handle_events(frame_time):
    global name_x, select_menu, ishelp
    events=get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif(event.type == SDL_MOUSEMOTION):
            class_cursor.Cursor.x,class_cursor.Cursor.y=event.x,600-event.y
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button ==SDL_BUTTON_LEFT:
            ishelp = False
            if select_menu == True:
                click_type = check_click(event.x,600-event.y)
                if click_type == NEW_GAME or click_type == LOAD_GAME:
                    game_framework.push_state(main_state,click_type)
                if click_type == HELP:
                    ishelp = True
        else:
            if(event.type) == (SDL_KEYDOWN):
                ishelp=False
            if(event.type, event.key) == (SDL_KEYDOWN,SDLK_ESCAPE):
                game_framework.quit()
            elif(event.type, event.key) == (SDL_KEYDOWN,SDLK_SPACE):
                if name_x != 365:
                    name_x =365
                else:
                    select_menu = True


def update(frame_time):
    global space_image, opacify_time, change, name_x
    opacify_time +=0.025*change
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
        if select_menu == False:
            space_image.draw(900,60)
        else:
            if ishelp:
                readme_image.draw(370,240)
            newgame_image.draw(1000,350)
            loadgame_image.draw(1000,220)
            help_image.draw(1000,90)
    cursor.draw()
    update_canvas()




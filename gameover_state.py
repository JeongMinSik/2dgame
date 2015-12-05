import game_framework
from pico2d import *
import class_cursor

name = "gameover_state"


def enter(object1=None,object2=None):
    global back_image,police_image, cursor,bgm, opacify_time, box_image, font
    bgm=load_music('Sound/game_over.wav')
    bgm.set_volume(50)
    bgm.play()

    back_image = load_image('Game_Over/game_over.png')
    police_image = load_image('Game_Over/police.png')
    box_image = load_image('Main_Map/main_text_box.png')
    box_image.opacify(0.9)
    font=load_font('Font/nanumfont.ttf')
    opacify_time=1
    cursor=class_cursor.Cursor()

def exit():
    global back_image,police_image
    del(back_image,police_image)


def pause():
    pass

def resume():
    pass

def handle_events(frame_time):
    events=get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif(event.type == SDL_MOUSEMOTION):
            class_cursor.Cursor.x,class_cursor.Cursor.y=event.x,600-event.y
        else:
            if opacify_time <= 0.000 and event.type  == SDL_KEYDOWN:
                game_framework.pop_state()


def update(frame_time):
    global space_image, opacify_time, change, name_x
    if opacify_time  > 0:
        opacify_time -=0.01
    police_image.opacify(opacify_time)

def draw(frame_time):
    clear_canvas()
    back_image.draw(600,300)
    if opacify_time >0:
        police_image.draw(600,300)
    else:
        box_image.draw(1025,80)
        font.draw(880,115,"GAME OVER")
        font.draw_unicode(880,85,"혐의가 100%가 되어 체포되었습니다.")
        font.draw_unicode(880,45,"아무키나 누르면 메인화면으로 이동합니다.")
    cursor.draw()
    update_canvas()




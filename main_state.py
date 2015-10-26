from pico2d import *
import random
from background import FixedBackground as Background


import game_framework
import battle_state
import class_user
import class_Npc
import class_main_text
import class_entrance
import class_cursor

name = "MainState"


boy = None
font = None
npc_cnt = 1

def enter():
    global boy,background,font,npc_group,npc_test,status_image,main_text,police,entrance_group,cursor
    #텍스트
    font = load_font('nanumfont.ttf')
    main_text = class_main_text.Main_Text()

    #유저와 백그라운드설정
    boy=class_user.User()
    background = Background(boy)
    boy.set_background(background)
    status_image = load_image('status_box.png')
    status_image.opacify(0.9)

    #입구설정
    entrance_group=[class_entrance.Entrance(i,boy) for i in range(11)]

    #초기 npc그룹 생성
    npc_group =[]
    police=class_Npc.Npc(1040,472,boy,background,npc_group,1)
    npc_group.append(police) #경찰

    #초기 npc 1+9 (10명) 생성
    while npc_cnt <10:
        for i in range(1,11):
            generate(i)
    #유저 위치설정
    #boy.x,boy.y = 1128,464
    boy.x,boy.y = 1152,504

    cursor=class_cursor.Cursor()

def exit():
    global boy, background,npc_group, status_image
    del(boy)
    del(background)
    del(npc_group)
    del(status_image)


def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    global npc_cnt
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        ###########################(개발용) 배열값 콘솔창에 출력 ################################
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            for row in boy.bg.map_matrix:
                 print (row)
        #########################################################################################
        elif(event.type == SDL_MOUSEMOTION):
             class_cursor.Cursor.x, class_cursor.Cursor.y=event.x,600-event.y
        if main_text.npc == None:
            boy.handle_event(event,main_text)
        else:
            if event.type == SDL_KEYDOWN:
                if main_text.step ==0:
                    if event.key == SDLK_RIGHT:
                        main_text.yes = 0
                    elif event.key == SDLK_LEFT:
                        main_text.yes = 1

                    if main_text.yes == 0 and event.key == SDLK_z:
                        if main_text.npc.type >=100:
                            boy.x -=8
                            boy.y-=8
                            boy.state=boy.Down
                            for ent in entrance_group:
                                ent.active_t=0
                        main_text.npc=None
                        main_text.yes = 1
                    elif main_text.yes == 1 and event.key == SDLK_z:
                        if main_text.npc.type < 100:
                            #순찰지역
                            if boy.place == police.place and main_text.npc.type != 70:
                                main_text.string1 = "현재 이 구역은 경찰이 순찰 중이므로                      "
                                main_text.string2 = "강도질을 할 수 없습니다!                                "
                                main_text.string3 = "                                                      "
                                main_text.step =1
                            #약함 - 젊은성인
                            elif boy.dice_num < 4 and main_text.npc.type >= 50 and main_text.npc.type <70:
                                main_text.string1 = "젊은 성인을 상대로 강도질하기엔                      "
                                main_text.string2 = "아직 당신이 너무 약합니다.                                "
                                main_text.string3 = "                                                      "
                                main_text.step =1
                            elif boy.dice_num < 5 and main_text.npc.type == 70:
                                main_text.string1 = "경찰과 싸우기엔 아직 당신이 너무 약합니다.                     "
                                main_text.string2 = "모든 준비를 마친 후에 경찰과 싸우세요.                             "
                                main_text.string3 = "                                                      "
                                main_text.step =1
                            elif boy.suspicion !=0 and main_text.npc.type == 70:
                                main_text.string1 = "경찰을 공격하기 위해서는                     "
                                main_text.string2 = "혐의가 0 % 이어야만 합니다.                             "
                                main_text.string3 = "                                                      "
                                main_text.step =1
                            else:
                                npc_cnt-=1
                                game_framework.push_state(battle_state,boy,main_text.npc)
                                if main_text.npc != police:
                                    for npc in npc_group:
                                        if npc.type == main_text.npc.type: npc_group.remove(npc)
                                main_text.npc=None
                                main_text.yes = 1
                        else:
                            for ent in entrance_group:
                                ent.handle_event(event,main_text)
                elif main_text.step == 1:
                    if event.key == SDLK_z:
                        if main_text.npc.type >=100:
                            boy.x -=8
                            boy.y-=8
                            boy.state=boy.Down
                            for ent in entrance_group:
                                ent.active_t=0
                        main_text.npc=None
                        main_text.yes = 1
                        main_text.step =0

def update(frame_time):
    handle_events(frame_time)
    boy.update(frame_time)
    boy.set_npcgroup(npc_group)
    background.update()
    if main_text.npc == None:
        for npc in npc_group:
            npc.update(frame_time,entrance_group)
            npc.set_npcgroup(npc_group)
    for ent in entrance_group:
        ent.update(main_text)
    delay(0.05)
    # NPC 리젠 + 유저체력감소
    if boy.stepbystep() and npc_cnt < 20:
        generate(random.randint(1,10))

def draw(frame_time):
    clear_canvas()
    background.draw()
    if npc_cnt >2:
        for npc in npc_group:
            npc.draw()
            #npc.draw_bb()
    boy.draw()
    #boy.draw_bb()

    #상태창
    status_image.draw(180,540)
    font.draw_unicode(35 , 570, '체력: %3d'%boy.hp + ' / %3d'%boy.maxhp + '    혐의: %4d'%boy.suspicion + '%    현위치:  '+boy.place)
    font.draw_unicode(35 , 540, '   돈:  %5d'%boy.gold  + '원      주사위최댓값: %3d'%boy.dice_num)
    font.draw_unicode(35 , 510, '최근 범행  [' + '%6s, '%boy.place_s + '%6s, '%boy.type_s + '%6s'%boy.tool_s + ' ]        ')

    main_text.draw()

    cursor.draw()
    update_canvas()

#해당 좌표가 유저에게 보이는지 확인
def camera_view(x,y):
    if boy.x<0 and boy.y<0:
        return 0
    left=right=bottom=top=0
    if boy.canvas_width/2 -boy.x > 0:
        left = boy.x - boy.canvas_width/2 + (boy.canvas_width/2 -boy.x)
        right = boy.x + boy.canvas_width/2 + (boy.canvas_width/2 -boy.x)
    elif boy.bg.w < boy.x + boy.canvas_width/2:
        left = boy.x - boy.canvas_width/2 - (boy.x + boy.canvas_width/2 - boy.bg.w)
        right =  boy.x + boy.canvas_width/2 - (boy.x + boy.canvas_width/2 - boy.bg.w)
    else:
        left = boy.x - boy.canvas_width/2
        right = boy.x + boy.canvas_width/2
    if boy.canvas_height/2 -boy.y > 0:
        bottom = boy.y - boy.canvas_height/2 + (boy.canvas_height/2 -boy.y)
        top = boy.y + boy.canvas_height/2 + (boy.canvas_height/2 -boy.y)
    elif boy.bg.h < boy.y + boy.canvas_height/2:
        bottom = boy.y - boy.canvas_height/2 - (boy.y + boy.canvas_height/2 - boy.bg.h)
        top =  boy.y + boy.canvas_height/2 - (boy.y + boy.canvas_height/2 - boy.bg.h)
    else:
        bottom = boy.y - boy.canvas_height/2
        top = boy.y + boy.canvas_height/2
    if left-5 < x and right+5 > x and bottom-5 < y and top+5 > y:
        return 1
    return 0

def generate(generation_zone):
    global npc_cnt, npc_group
    temp_npc=class_Npc.Npc(0,0,boy,background,npc_group)
    if generation_zone == 1:
        temp_npc.x, temp_npc.y = 584,784
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user) or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 2:
        temp_npc.x, temp_npc.y = 1208,792
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 3:
        temp_npc.x, temp_npc.y = 1728,784
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 4:
        temp_npc.x, temp_npc.y = 376,456
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 5:
        temp_npc.x, temp_npc.y = 616,464
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 6:
        temp_npc.x, temp_npc.y = 1040,472
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 7:
        temp_npc.x, temp_npc.y = 1488,472
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 8:
        temp_npc.x, temp_npc.y = 280,128
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 9:
        temp_npc.x, temp_npc.y = 760,120
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 10:
        temp_npc.x, temp_npc.y = 1200,120
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                del temp_npc
                return

    npc_group.append(temp_npc)
    npc_cnt+=1
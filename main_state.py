from pico2d import *
import random
from background import FixedBackground as Background


import game_framework
import battle_state
import class_user
import class_npc
import class_cursor

class Entrance:
    HOSPITAL,PIZZA_SHOP,GAME,BAKERY,POLICE_STATION,CITY_HALL,HOTEL,EMPTY_HOUSE1,EMPTY_HOUSE2,DRUG_STORE,BURGER_SHOP= 100,101,102,103,104,105,106,107,108,109,110
    def __init__(self,num,user):
        self.x,self.y =0,0
        self.type = num+100
        self.active_type=0
        self.user=user
        self.hp_price=0
        self.police_price=0
        self.dice_price=0

        if self.type == self.HOSPITAL:
            self.x,self.y =264,232
        elif self.type == self.PIZZA_SHOP:
            self.x,self.y =560,184
        elif self.type == self.GAME:
            self.x,self.y = 696,184
        elif self.type == self.BAKERY:
            self.x,self.y = 976,184
        elif self.type == self.POLICE_STATION:
            self.x,self.y = 1136,224
        elif self.type == self.CITY_HALL:
            self.x,self.y = 776,584
        elif self.type == self.HOTEL:
            self.x,self.y = 1160,512
        elif self.type == self.EMPTY_HOUSE1:
            self.x,self.y = 1256,512
        elif self.type == self.EMPTY_HOUSE2:
            self.x,self.y = 1352,544
        elif self.type == self.DRUG_STORE:
            self.x,self.y = 720,792
        elif self.type == self.BURGER_SHOP:
            self.x,self.y = 848,784

    def update(self,main_text):
        if self.collide(self.user):
            self.active_type =self.type
            self.user.running = False
            main_text.npc=self
            if main_text.step ==0:
                if self.type == self.HOSPITAL:
                    main_text.step=1
                    main_text.string1 = "병원                                           "
                    main_text.string2 = "체력이 0이 되면 병원으로 후송됩니다.                               "
                    main_text.string3 = "                                        "
                elif self.type == self.PIZZA_SHOP:
                    main_text.string1 = "피자헛                                           "
                    main_text.string2 = "페페로니피자 600원 (Hp 50 회복)                          "
                    main_text.string3 = "구입해 드시겠습니까?                       "
                elif self.type == self.GAME:
                    main_text.step =1
                    main_text.string1 = "오락실                                           "
                    main_text.string2 = "미구현                          "
                    main_text.string3 = "                                          "
                elif self.type == self.BAKERY:
                    main_text.string1 = "파리바게트                                    "
                    main_text.string2 = "크림빵 100원 (Hp 5 회복)                          "
                    main_text.string3 = "구입해 드시겠습니까?                         "
                elif self.type == self.POLICE_STATION:
                    if self.user.suspicion == 0:
                        main_text.step =1
                        main_text.string1 = "경찰서                                           "
                        main_text.string2 = "당신은 혐의가 0 %이므로                           "
                        main_text.string3 = "경찰서에 올 이유가 없습니다.                             "
                    else:
                        self.police_price = self.user.suspicion *100
                        main_text.string1 = "경찰서                                           "
                        main_text.string2 = "혐의를 0 %%로 만듭니다. 뇌물:%4d"%self.police_price+"원                           "
                        main_text.string3 = "뇌물을 주겠습니까?                         "
                elif self.type == self.CITY_HALL:
                    if self.user.dice_num ==5:
                        main_text.step =1
                        main_text.string1 = "시청                                           "
                        main_text.string2 = "주사위최댓값은 5를 초과할 수 없습니다.           "
                        main_text.string3 = "                                              "
                    else:
                        if self.user.dice_num ==3:
                            self.dice_price=5000
                        else:
                            self.dice_price=10000
                        main_text.string1 = "시청                                           "
                        main_text.string2 = "주사위 최댓값 +1 비용:%5d"%self.dice_price+"원                         "
                        main_text.string3 = "주사위값을 올리시겠습니까?                         "
                elif self.type == self.HOTEL:
                    main_text.string1 = "호텔                                           "
                    main_text.string2 = "현재까지 플레이 상태를 저장합니다.                          "
                    main_text.string3 = "저장하시겠습니까?                         "
                elif self.type == self.EMPTY_HOUSE1:
                    main_text.step=1
                    main_text.string1 = "빈집1                                           "
                    main_text.string2 = "비어있는 집입니다.                          "
                    main_text.string3 = "                                        "
                elif self.type == self.EMPTY_HOUSE2:
                    main_text.step=1
                    main_text.string1 = "빈집2                                           "
                    main_text.string2 = "비어있는 집입니다.                          "
                    main_text.string3 = "                                        "
                elif self.type == self.DRUG_STORE:
                    if self.user.maxhp < 40:
                        self.hp_price= 1000
                    elif self.user.maxhp <60:
                        self.hp_price= 2000
                    elif self.user.maxhp <80:
                        self.hp_price= 4000
                    elif self.user.maxhp <100:
                        self.hp_price= 8000
                    main_text.string1 = "약국                                           "
                    main_text.string2 = "건강증진제 "+"%4d"%self.hp_price +"원 (최대Hp 10 증가)                              "
                    main_text.string3 = "구입해 복용하시겠습니까?                       "
                elif self.type == self.BURGER_SHOP:
                    main_text.string1 = "버거킹                                           "
                    main_text.string2 = "불고기버거 300원 (Hp 20 회복)                          "
                    main_text.string3 = "구입해 드시겠습니까?                         "

    def check_last_place(self):
        if self.user.last_place == 'S' and self.active_type >=self.HOSPITAL and self.active_type <= self.POLICE_STATION:
            return True
        if self.user.last_place == 'W' and self.active_type ==self.CITY_HALL :
            return True
        if self.user.last_place == 'E' and self.active_type >=self.HOTEL and self.active_type <= self.EMPTY_HOUSE2:
            return True
        if self.user.last_place == 'N' and self.active_type >=self.DRUG_STORE and self.active_type <= self.BURGER_SHOP:
            return True
        return False

    def handle_event(self, main_text):
        if self.check_last_place():
            main_text.string2 = "이 건물은 최근 범행구역 안에 있으므로                      "
            main_text.string3 = "이용할 수 없습니다.                                            "
        elif self.active_type == self.PIZZA_SHOP:
            if self.user.gold >=600 and self.user.hp != self.user.maxhp:
                self.user.gold -=600
                self.user.hp +=50
                main_text.string2 = "피자를 먹고 체력 50 을 회복했습니다.                      "
                main_text.string3 = "돈 -600원                                          "
            elif self.user.gold < 600:
                main_text.string2 = "돈이 부족하여 피자를                      "
                main_text.string3 = "구입할 수 없습니다.                                     "
            elif self.user.hp == self.user.maxhp:
                main_text.string2 = "이미 체력이 최대치입니다.                           "
                main_text.string3 = "                                                    "
        elif self.active_type == self.BAKERY:
            if self.user.gold >=100 and self.user.hp != self.user.maxhp:
                self.user.gold -=100
                self.user.hp +=5
                main_text.string2 = "크림빵을 먹고 체력 5 를 회복했습니다.                      "
                main_text.string3 = "돈 -100원                                          "
            elif self.user.gold < 100:
                main_text.string2 = "돈이 부족하여 크림빵을                      "
                main_text.string3 = "구입할 수 없습니다.                                     "
            elif self.user.hp == self.user.maxhp:
                main_text.string2 = "이미 체력이 최대치입니다.                           "
                main_text.string3 = "                                                    "
        elif self.active_type == self.POLICE_STATION:
            if self.user.gold >=self.police_price and self.user.suspicion != 0:
                self.user.gold -=self.police_price
                self.user.suspicion = 0
                main_text.string2 = "뇌물을 주어 혐의가 0 %가 되었습니다.                      "
                main_text.string3 = "돈 -%4d"%self.police_price+"원                                          "
            elif self.user.gold < self.police_price and self.user.suspicion != 0:
                main_text.string2 = "혐의를 0 %로 만들기엔                      "
                main_text.string3 = "가진 돈이 부족합니다.                                     "
        elif self.active_type == self.CITY_HALL:
            if self.user.gold >=self.dice_price and self.user.dice_num != 5:
                self.user.gold -=self.dice_price
                self.user.dice_num += 1
                main_text.string2 = "주사위최댓값이 1 증가했습니다!                      "
                main_text.string3 = "돈 -%4d"%self.dice_price+"원                                          "
            elif self.user.gold < self.dice_price and self.user.dice_num != 5:
                main_text.string2 = "주사위 업그레이드를 하기엔                           "
                main_text.string3 = "가진 돈이 부족합니다.                                     "
        elif self.active_type == self.HOTEL:
                main_text.string2 = "미구현                                     "
                main_text.string3 = "                                          "
        elif self.active_type == self.DRUG_STORE:
            if self.user.gold >= self.hp_price and self.user.maxhp !=99:
                self.user.gold -= self.hp_price
                self.user.maxhp +=10
                main_text.string2 = "최대체력이 10 만큼 증가했습니다!                      "
                main_text.string3 = "돈 -"+"%4d"%self.hp_price+"원                                     "
            elif self.user.gold < self.hp_price:
                main_text.string2 = "돈이 부족하여 건강증진제를                      "
                main_text.string3 = "구입할 수 없습니다.                                     "
            elif self.user.maxhp == 99:
                main_text.string2 = "최대 체력은 99 를 초과할 수 없습니다.                          "
                main_text.string3 = "                                                  "
        elif self.active_type == self.BURGER_SHOP:
            if self.user.gold >=300 and self.user.hp != self.user.maxhp:
                self.user.gold -=300
                self.user.hp +=20
                main_text.string2 = "햄버거를 먹고 체력 20 을 회복했습니다.                      "
                main_text.string3 = "돈 -300원                                          "
            elif self.user.gold < 300:
                main_text.string2 = "돈이 부족하여 햄버거를                      "
                main_text.string3 = "구입할 수 없습니다.                                     "
            elif self.user.hp == self.user.maxhp:
                main_text.string2 = "이미 체력이 최대치입니다.                           "
                main_text.string3 = "                                                    "
        main_text.step =1

    def get_bb(self):
        if self.type == self.CITY_HALL:
            return self.x -16,self.y-4,self.x+16, self.y+4
        return self.x -8,self.y-14,self.x+8, self.y+8

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def collide(self,object):
        left_a, bottom_a, right_a, top_a = self.get_bb()
        left_b, bottom_b, right_b, top_b = object.get_bb()
        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
        return True

class Main_Text:
    box_image=None
    button_image = None
    font = None
    def __init__(self):
        self.yes = True
        self.npc = None
        self.step = 0
        self.string1 = "이름                                          "
        self.string2 = "\"말\"                                        "
        self.string3 = "강도질을 시도하시겠습니까?                       "
        if Main_Text.box_image == None:
            Main_Text.box_image = load_image('Main_Map/main_text_box.png')
            Main_Text.box_image.opacify(0.9)
        if Main_Text.button_image == None:
            Main_Text.button_image = load_image('Main_Map/button_y_n.png')
        if Main_Text.font == None:
            Main_Text.font=load_font('nanumfont.ttf')


    def draw(self):
        if(self.npc != None):
            self.box_image.draw(1025,80)
            if self.step == 0:
                if self.npc.type <100:
                    self.string1 = self.npc.type_s
                    self.string2 = self.npc.speech
                    self.string3 = "강도질을 시도하시겠습니까?                       "
                self.button_image.clip_draw(0, self.yes*30, 96, 30, 1123,45)
            else:
                self.button_image.clip_draw(0, 30, 48, 30, 1147,45)
            self.font.draw_unicode(880,115,self.string1)
            self.font.draw_unicode(880,85,self.string2)
            self.font.draw_unicode(880,45,self.string3)

name = "MainState"
boy = None
font = None
npc_cnt = 1

def enter():
    global boy,background,font,npc_group,status_image,main_text,police,entrance_group,cursor
    #텍스트
    font = load_font('nanumfont.ttf')
    main_text = Main_Text()

    #유저와 백그라운드설정
    boy=class_user.User()
    background = Background(boy)
    boy.set_background(background)
    status_image = load_image('Main_Map/status_box.png')
    status_image.opacify(0.9)

    #입구설정
    entrance_group=[Entrance(i,boy) for i in range(11)]

    #초기 npc그룹 생성
    npc_group =[]
    police=class_npc.Npc(1040,472,boy,background,npc_group,1)
    npc_group.append(police)

    #초기 npc 1+9 (10명) 생성
    while npc_cnt <10:
        for i in range(1,11):
            generate(i)
    #유저 초기위치설정
    boy.x,boy.y = 1152,496

    cursor=class_cursor.Cursor()

def exit():
    global boy,background,font,npc_group,status_image,main_text,police,entrance_group,cursor
    del(boy,background,font,npc_group,status_image,main_text,police,entrance_group,cursor)


def pause():
    pass

def resume():
    pass

def communicate(event):
    global npc_cnt
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
                    boy.state=boy.DOWN
                    for ent in entrance_group:
                        ent.active_type =0
                main_text.npc=None
                main_text.yes = 1
            elif main_text.yes == 1 and event.key == SDLK_z:
                if main_text.npc.type < 100:
                    if boy.place == police.place and main_text.npc.type != 70:
                        main_text.string1 = "현재 이 구역은 경찰이 순찰 중이므로                      "
                        main_text.string2 = "강도질을 할 수 없습니다!                                "
                        main_text.string3 = "                                                      "
                        main_text.step =1
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
                        ent.handle_event(main_text)
        elif main_text.step == 1:
            if event.key == SDLK_z:
                if main_text.npc.type >=100:
                    boy.x -=8
                    boy.y-=8
                    boy.state=boy.DOWN
                    for ent in entrance_group:
                        ent.active_type =0
                main_text.npc=None
                main_text.yes = 1
                main_text.step =0

def handle_events(frame_time):
    global npc_cnt
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        ###########################(개발용) 배열값 콘솔창에 출력 ################################
        #elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
        #    for row in boy.bg.map_matrix:
        #         print (row)
        #########################################################################################
        elif(event.type == SDL_MOUSEMOTION):
             class_cursor.Cursor.x, class_cursor.Cursor.y=event.x,600-event.y
        if main_text.npc == None:
            boy.handle_event(event,main_text)
        else:
            communicate(event)

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
    if boy.stepbystep() and npc_cnt < 20:
        generate(random.randint(1,10))

def draw(frame_time):
    clear_canvas()
    background.draw()
    for npc in npc_group:
        npc.draw()
        #npc.draw_bb()
    boy.draw()
    #boy.draw_bb()
    status_image.draw(180,540)
    font.draw_unicode(35 , 570, '체력: %3d'%boy.hp + ' / %3d'%boy.maxhp + '    혐의: %4d'%boy.suspicion + '%    현위치:  '+boy.place)
    font.draw_unicode(35 , 540, '   돈:  %5d'%boy.gold  + '원      주사위최댓값: %3d'%boy.dice_num)
    font.draw_unicode(35 , 510, '최근 범행  [' + '%6s, '%boy.place_s + '%6s, '%boy.type_s + '%6s'%boy.tool_s + ' ]        ')
    main_text.draw()
    cursor.draw()
    update_canvas()

#해당 좌표가 유저에게 보이는지 확인하는 함수
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
    temp_npc=class_npc.Npc(0,0,boy,background,npc_group)
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
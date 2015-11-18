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

        self.buy_sound = load_music('Sound/effect/ui/ui_buy.wav')
        self.buy_sound.set_volume(70)
        self.fail_sound = load_music('Sound/effect/ui/ui_fail.wav')
        self.fail_sound.set_volume(70)

        ent_data_file = open('Data/Entrance.txt','r')
        ent_data = json.load(ent_data_file)
        ent_data_file.close()
        if self.type == self.HOSPITAL:
            self.x,self.y =ent_data['Hospital']['x'],ent_data['Hospital']['y']
        elif self.type == self.PIZZA_SHOP:
            self.x,self.y =ent_data['Pizza_Shop']['x'],ent_data['Pizza_Shop']['y']
        elif self.type == self.GAME:
            self.x,self.y = ent_data['Game']['x'],ent_data['Game']['y']
        elif self.type == self.BAKERY:
            self.x,self.y = ent_data['Bakery']['x'],ent_data['Bakery']['y']
        elif self.type == self.POLICE_STATION:
            self.x,self.y = ent_data['Police_Station']['x'],ent_data['Police_Station']['y']
        elif self.type == self.CITY_HALL:
            self.x,self.y = ent_data['City_Hall']['x'],ent_data['City_Hall']['y']
        elif self.type == self.HOTEL:
            self.x,self.y = ent_data['Hotel']['x'],ent_data['Hotel']['y']
        elif self.type == self.EMPTY_HOUSE1:
            self.x,self.y = ent_data['Empty_House1']['x'],ent_data['Empty_House1']['y']
        elif self.type == self.EMPTY_HOUSE2:
            self.x,self.y = ent_data['Empty_House2']['x'],ent_data['Empty_House2']['y']
        elif self.type == self.DRUG_STORE:
            self.x,self.y = ent_data['Drug_Store']['x'],ent_data['Drug_Store']['y']
        elif self.type == self.BURGER_SHOP:
            self.x,self.y = ent_data['Burger_Shop']['x'],ent_data['Burger_Shop']['y']

    def update(self,main_text):
        if self.collide(self.user):
            self.active_type =self.type
            self.user.running = False
            main_text.npc=self
            if main_text.step ==0:
                ent_data_file = open('Data/Entrance.txt','r')
                ent_data = json.load(ent_data_file)
                ent_data_file.close()
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
                        if self.user.dice_num == ent_data['Double_Price']['dice']:
                            self.dice_price=ent_data['City_Hall']['dice_price']
                        else:
                            self.dice_price=ent_data['City_Hall']['dice_price']*2
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
                    if self.user.maxhp < ent_data['Double_Price']['hp1']:
                        self.hp_price= ent_data['Drug_Store']['hp_price']
                    elif self.user.maxhp <ent_data['Double_Price']['hp2']:
                        self.hp_price= ent_data['Drug_Store']['hp_price']*2
                    elif self.user.maxhp <ent_data['Double_Price']['hp3']:
                        self.hp_price= ent_data['Drug_Store']['hp_price']*4
                    elif self.user.maxhp <ent_data['Double_Price']['hp4']:
                        self.hp_price= ent_data['Drug_Store']['hp_price']*8
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
        ent_data_file = open('Data/Entrance.txt','r')
        ent_data = json.load(ent_data_file)
        ent_data_file.close()
        if self.check_last_place():
            self.fail_sound.play()
            main_text.string2 = "이 건물은 최근 범행구역 안에 있으므로                      "
            main_text.string3 = "이용할 수 없습니다.                                            "
        elif self.active_type == self.PIZZA_SHOP:
            if self.user.gold >=ent_data['Pizza_Shop']['price'] and self.user.hp != self.user.maxhp:
                self.buy_sound.play()
                self.user.gold -=ent_data['Pizza_Shop']['price']
                self.user.hp +=ent_data['Pizza_Shop']['heal']
                main_text.string2 = "피자를 먹고 체력 50 을 회복했습니다.                      "
                main_text.string3 = "돈 -600원                                          "
            elif self.user.gold < ent_data['Pizza_Shop']['price'] :
                self.fail_sound.play()
                main_text.string2 = "돈이 부족하여 피자를                      "
                main_text.string3 = "구입할 수 없습니다.                                     "
            elif self.user.hp == self.user.maxhp:
                self.fail_sound.play()
                main_text.string2 = "이미 체력이 최대치입니다.                           "
                main_text.string3 = "                                                    "
        elif self.active_type == self.BAKERY:
            if self.user.gold >=ent_data['Bakery']['price'] and self.user.hp != self.user.maxhp:
                self.buy_sound.play()
                self.user.gold -=ent_data['Bakery']['price']
                self.user.hp +=ent_data['Bakery']['heal']
                main_text.string2 = "크림빵을 먹고 체력 5 를 회복했습니다.                      "
                main_text.string3 = "돈 -100원                                          "
            elif self.user.gold < ent_data['Bakery']['price']:
                self.fail_sound.play()
                main_text.string2 = "돈이 부족하여 크림빵을                      "
                main_text.string3 = "구입할 수 없습니다.                                     "
            elif self.user.hp == self.user.maxhp:
                self.fail_sound.play()
                main_text.string2 = "이미 체력이 최대치입니다.                           "
                main_text.string3 = "                                                    "
        elif self.active_type == self.POLICE_STATION:
            if self.user.gold >=self.police_price and self.user.suspicion != 0:
                self.buy_sound.play()
                self.user.gold -=self.police_price
                self.user.suspicion = 0
                main_text.string2 = "뇌물을 주어 혐의가 0 %가 되었습니다.                      "
                main_text.string3 = "돈 -%4d"%self.police_price+"원                                          "
            elif self.user.gold < self.police_price and self.user.suspicion != 0:
                self.fail_sound.play()
                main_text.string2 = "혐의를 0 %로 만들기엔                      "
                main_text.string3 = "가진 돈이 부족합니다.                                     "
        elif self.active_type == self.CITY_HALL:
            if self.user.gold >=self.dice_price and self.user.dice_num != 5:
                self.buy_sound.play()
                self.user.gold -=self.dice_price
                self.user.dice_num += 1
                main_text.string2 = "주사위최댓값이 1 증가했습니다!                      "
                main_text.string3 = "돈 -%4d"%self.dice_price+"원                                          "
            elif self.user.gold < self.dice_price and self.user.dice_num != 5:
                self.fail_sound.play()
                main_text.string2 = "주사위 업그레이드를 하기엔                           "
                main_text.string3 = "가진 돈이 부족합니다.                                     "
        elif self.active_type == self.HOTEL:
                main_text.string2 = "미구현                                     "
                main_text.string3 = "                                          "
        elif self.active_type == self.DRUG_STORE:
            if self.user.gold >= self.hp_price and self.user.maxhp !=99:
                self.buy_sound.play()
                self.user.gold -= self.hp_price
                self.user.maxhp +=ent_data['Drug_Store']['add_hp']
                main_text.string2 = "최대체력이 10 만큼 증가했습니다!                      "
                main_text.string3 = "돈 -"+"%4d"%self.hp_price+"원                                     "
            elif self.user.gold < self.hp_price:
                self.fail_sound.play()
                main_text.string2 = "돈이 부족하여 건강증진제를                      "
                main_text.string3 = "구입할 수 없습니다.                                     "
            elif self.user.maxhp == 99:
                self.fail_sound.play()
                main_text.string2 = "최대 체력은 99 를 초과할 수 없습니다.                          "
                main_text.string3 = "                                                  "
        elif self.active_type == self.BURGER_SHOP:
            if self.user.gold >=ent_data['Burger_Shop']['price'] and self.user.hp != self.user.maxhp:
                self.buy_sound.play()
                self.user.gold -=ent_data['Burger_Shop']['price']
                self.user.hp +=ent_data['Burger_Shop']['heal']
                main_text.string2 = "햄버거를 먹고 체력 20 을 회복했습니다.                      "
                main_text.string3 = "돈 -300원                                          "
            elif self.user.gold < ent_data['Burger_Shop']['price']:
                self.fail_sound.play()
                main_text.string2 = "돈이 부족하여 햄버거를                      "
                main_text.string3 = "구입할 수 없습니다.                                     "
            elif self.user.hp == self.user.maxhp:
                self.fail_sound.play()
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
        self.move_sound=load_music('Sound/effect/ui/ui_move_ok.wav')
        self.move_sound.set_volume(70)
        self.ok_sound = load_music('Sound/effect/ui/ui_user_ok.wav')
        self.ok_sound.set_volume(70)
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
bgm = None

def enter(object1=None,object2=None):
    print("메인스테이트 enter")
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
    npc_data_file = open('Data/Npc.txt','r')
    npc_data = json.load(npc_data_file)
    npc_data_file.close()
    npc_group =[]
    police=class_npc.Npc(npc_data['Police']['x'],npc_data['Police']['y'],boy,background,npc_group,1)
    npc_group.append(police)

    #초기 npc 1+9 (10명) 생성
    while npc_cnt <10:
        for i in range(1,11):
            generate(i)
    #유저 초기위치설정
    user_data_file = open('Data/User.txt','r')
    user_data = json.load(user_data_file)
    user_data_file.close()
    boy.x,boy.y = user_data['User']['x'],user_data['User']['y']

    cursor=class_cursor.Cursor()

def exit():
    print("메인스테이트 exit")
    global boy,background,font,npc_group,status_image,main_text,police,entrance_group,cursor
    del(boy,background,font,npc_group,status_image,main_text,police,entrance_group,cursor)


def pause():
    global background
    print("메인스테이트 pause")
    background.bgm.pause()

def resume():
    global background
    print("메인스테이트 resume")
    background.bgm.resume() #다시 재생되지 않는다.

def communicate(event):
    global npc_cnt
    if event.type == SDL_KEYDOWN:
        if main_text.step ==0:
            if event.key == SDLK_RIGHT:
                main_text.yes = 0
                main_text.move_sound.play()
            elif event.key == SDLK_LEFT:
                main_text.yes = 1
                main_text.move_sound.play()
            if main_text.yes == 0 and event.key == SDLK_z:
                main_text.ok_sound.play()
                if main_text.npc.type >=Entrance.HOSPITAL:
                    boy.x -=boy.DISTANCE
                    boy.y-=boy.DISTANCE
                    boy.state=boy.DOWN
                    for ent in entrance_group:
                        ent.active_type =0
                main_text.npc=None
                main_text.yes = 1
            elif main_text.yes == 1 and event.key == SDLK_z:
                main_text.ok_sound.play()
                if main_text.npc.type < Entrance.HOSPITAL:
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
                main_text.ok_sound.play()
                if main_text.npc.type >=Entrance.HOSPITAL:
                    boy.x -=boy.DISTANCE
                    boy.y -=boy.DISTANCE
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
    zone_data_file = open('Data/Generate.txt','r')
    zone_data = json.load(zone_data_file)
    zone_data_file.close()
    if generation_zone == 1:
        temp_npc.x, temp_npc.y = zone_data['Zone1']['x'],zone_data['Zone1']['y']
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user) or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 2:
        temp_npc.x, temp_npc.y = zone_data['Zone2']['x'],zone_data['Zone2']['y']
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 3:
        temp_npc.x, temp_npc.y = zone_data['Zone3']['x'],zone_data['Zone3']['y']
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 4:
        temp_npc.x, temp_npc.y = zone_data['Zone4']['x'],zone_data['Zone4']['y']
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 5:
        temp_npc.x, temp_npc.y = zone_data['Zone5']['x'],zone_data['Zone5']['y']
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 6:
        temp_npc.x, temp_npc.y = zone_data['Zone6']['x'],zone_data['Zone6']['y']
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 7:
        temp_npc.x, temp_npc.y = zone_data['Zone7']['x'],zone_data['Zone7']['y']
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 8:
        temp_npc.x, temp_npc.y = zone_data['Zone8']['x'],zone_data['Zone8']['y']
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 9:
        temp_npc.x, temp_npc.y = zone_data['Zone9']['x'],zone_data['Zone9']['y']
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                generation_zone+=1
                break
    if generation_zone == 10:
        temp_npc.x, temp_npc.y = zone_data['Zone10']['x'],zone_data['Zone10']['y']
        for npc in npc_group:
            if (npc.type != temp_npc.type and temp_npc.collide(npc)) or temp_npc.collide(temp_npc.user)or camera_view(temp_npc.x,temp_npc.y):
                del temp_npc
                return

    npc_group.append(temp_npc)
    npc_cnt+=1
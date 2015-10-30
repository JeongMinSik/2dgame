import game_framework
from pico2d import *
import random
import class_cursor


###############################################################

class Criminal_Tool:
    HAMMER,CHAIN,SPANNER,KNIFE = 1,2,3,4
    IDLE, FIRST_SELECTED,SECOND_SELECTED,GRABBED = 0, 1, 2, 3
    check_state=0 ## 십의 자리는 첫번째칸, 일의 자리는 두번째칸
    tool_cnt=[0,0,0,0,0] # 0번째칸은 쓰지 않는다, 1~4는 각 도구의 사용 수
    def __init__(self,type):
        self.type = type
        self.state = self.IDLE
        if self.type == self.HAMMER:
            self.image=load_image('Battle_State/tool_hammer.png')
            self.x,self.y = 83,443
        elif self.type == self.CHAIN:
            self.image=load_image('Battle_State/tool_chain.png')
            self.x,self.y = 210,443
        elif self.type == self.SPANNER:
            self.image=load_image('Battle_State/tool_spanner.png')
            self.x,self.y = 83,318
        elif self.type == self.KNIFE :
            self.image=load_image('Battle_State/tool_knife.png')
            self.x,self.y = 210,318

    def get_bb(self):
        return self.x -60,self.y-60,self.x+60, self.y+60  # 120x120

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x,self.y)

class Dice_Number:
    image = None
    First,Second,Third=0,1,2
    def __init__(self,position,player_max):
        self.x,self.y = 0,0
        self.position = position
        self.frame = 0
        self.max = player_max
        if self.position == self.First:
            self.x,self.y = 73,185
        elif self.position == self.Second:
            self.x,self.y = 331,185
        elif self.position == self.Third:
            self.x,self.y = 586,185
        if Dice_Number.image == None:
            Dice_Number.image=load_image('Battle_State/dice_num.png')

    def get_bb(self):
        return self.x -50,self.y-50,self.x+50, self.y+50  # 100x100

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        if(battle_step == STEP_USER_TURN):
            self.frame=random.randint(0,self.max)

    def draw(self):
        if(battle_step != STEP_USER_TURN):
            self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x,self.y)

class Dice_Animation:
    image = None
    First,Second,Third=0,1,2
    def __init__(self,position):
        self.x,self.y = 0,0
        self.position = position
        self.frame = random.randint(0,8)
        if self.position == self.First:
            self.x,self.y = 73,185
        elif self.position == self.Second:
            self.x,self.y = 331,185
        elif self.position == self.Third:
            self.x,self.y = 586,185
        if Dice_Animation.image == None:
            Dice_Animation.image=load_image('Battle_State/dice_animation.png')

    def get_bb(self):
        return self.x -50,self.y-50,self.x+50, self.y+50  # 100x100

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame +1) % 8

    def draw(self):
        if(battle_step == STEP_USER_TURN):
            self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x,self.y)

class Enemy:
    GRANDMA, GRANDPA, GIRL, BOY, WOMAN, MAN, POLICE = 1, 2, 3, 4, 5, 6, 7
    def __init__(self,npc):
        self.x,self.y=600,360
        self.type = (int)(npc.type /10)
        self.type_s = npc.type_s

        if self.type == self.GRANDMA:
            self.hp= random.randint(10,16)
            self.min=1
            self.max=3
            self.gold=150
            self.image = load_image('Battle_State/battle_grandma2.png')
        elif self.type == self.GRANDPA:
            self.hp= random.randint(13,19)
            self.min=1
            self.max=5
            self.gold=300
            self.image = load_image('Battle_State/battle_grandpa2.png')
        elif self.type == self.GIRL:
            self.hp= random.randint(17,23)
            self.min=3
            self.max=6
            self.gold=500
            self.image = load_image('Battle_State/battle_girl2.png')
        elif self.type == self.BOY:
            self.hp= random.randint(22,28)
            self.min=5
            self.max=9
            self.gold=750
            self.image = load_image('Battle_State/battle_boy2.png')
        elif self.type == self.WOMAN:
            self.hp= random.randint(28,34)
            self.min=7
            self.max=12
            self.gold=1100
            self.image = load_image('Battle_State/battle_woman2.png')
        elif self.type == self.MAN:
            self.hp= random.randint(35,40)
            self.min=9
            self.max=15
            self.gold=1500
            self.image = load_image('Battle_State/battle_man2.png')
        elif self.type == self.POLICE:
            self.hp= 99
            self.min=12
            self.max=20
            self.gold=2000
            self.image = load_image('Battle_State/battle_police2.png')
        self.set_attack_value()

    def draw(self):
        self.image.draw(self.x,self.y)

    def set_attack_value(self):
        self.attack_value=random.randint(self.min,self.max)

class Textbox:
    image = None
    def __init__(self):
        self.x,self.y= 875,430
        self.string1 = " "
        self.string2 = " "
        self.string3 = " "
        self.string4 = " "
        self.tool_check1= "  망치   x0      쇠사슬 x0        "
        self.tool_check2=  "스패너  x0        칼   x0        "
        self.wait=0
        if Textbox.image == None:
            Textbox.image=load_font('nanumfont.ttf')

    def update(self,enem,player):
        tool=["  망치  x%3d"%Criminal_Tool.tool_cnt[1]+"     ","쇠사슬 x%3d"%Criminal_Tool.tool_cnt[2]+"       ","스패너 x%3d"%Criminal_Tool.tool_cnt[3]+"         ","칼   x%3d"%Criminal_Tool.tool_cnt[4]+"        "]
        for i in range(1,5):
            if player.last_tool == i:
                tool[i-1] = '(!) '+tool[i-1]
            else:
                tool[i-1] = '    '+tool[i-1]

        self.tool_check1=tool[0]+tool[1]
        self.tool_check2=tool[2]+tool[3]

        if(self.wait == 0):
            if(battle_step == STEP_ENEMY_TURN):
                self.string1 = "상대방의 차례입니다.               "
                self.string2 = "z키를 누르면 상대방이 공격값을 결정합니다.                   "
                self.string3 = "                                                    "
                self.string4 = "                                                      "
            if(battle_step == STEP_USER_TURN ):
                self.string1 = "상대방의 공격값은 "+'%3d'%enem.attack_value + " 입니다.           "
                self.string2 = "z키를 누르면 나의 주사위값이 결정됩니다.                      "
                self.string3 = "                                                       "
                self.string4 = "                                                        "
            elif(battle_step == STEP_SELECT_TOOLS):
                if int(Criminal_Tool.check_state / 10)==0 or int(Criminal_Tool.check_state % 10)==0:
                    self.string1 = "주사위 값이 결정되었습니다.   "
                    self.string2 = "원하는 범행도구를 골라 사용하세요.                "
                    self.string3 = "드래그로 도구를 값 사이에 넣을 수 있습니다.            "
                    self.string4 = "도구를 넣은 후 z키로 결과값을 결정합니다.              "
                else:
                    self.string1 = "범행도구 2개를 모두 선택했습니다.              "
                    self.string2 = "이미 넣은 도구를 변경하고 싶다면,                  "
                    self.string3 = "마우스 오른쪽버튼으로 제거할 수 있습니다.                 "
                    self.string4 = "이제 z키를 눌러 결과값을 확인할 수 있습니다.              "
            elif(battle_step == STEP_CHECK_RESULT):
                pass
            elif(battle_step == STEP_TURN_END):
                pass
            elif battle_step == STEP_BATTLE_END:
                pass

    def draw(self):
        self.image.draw_unicode(31,565,self.tool_check1)
        self.image.draw_unicode(30,535,self.tool_check2)
        self.image.draw_unicode(self.x,self.y,self.string1)
        self.image.draw_unicode(self.x,self.y- 30,self.string2)
        self.image.draw_unicode(self.x,self.y- 60,self.string3)
        self.image.draw_unicode(self.x,self.y- 90,self.string4)

class Number:
    image=None
    def __init__(self):
        self.switch = 0 # 계산을 한번만 하기 위한 스위치
        self.enem_one=self.enem_one_x=self.enem_one_y=self.enem_ten=self.result_one=self.result_ten=self.result_one_x=self.result_one_y=0
        if Number.image == None:
            Number.image=load_image('Battle_State/numbers.png')

    def update(self,enem,dice_group,text_box):
        if(battle_step == STEP_ENEMY_TURN):
            self.attack_value = random.randint(enem.min,enem.max)
        if(battle_step >= STEP_USER_TURN):
            self.attack_value = enem.attack_value

        self.enem_one = (int)(self.attack_value % 10) #일의 자리
        self.enem_ten = (int)(self.attack_value / 10) #십의 자리

        # 자리수에 따른 좌표 결정
        if(self.enem_ten == 0):
            self.enem_one_x,self.enem_one_y= 604,533
        else:
            self.enem_one_x,self.enem_one_y= 620,533

        if battle_step == STEP_CHECK_RESULT and self.switch == 0:
            n1,n2,n3=dice_group[0].frame,dice_group[1].frame,dice_group[2].frame
            symbol1,symbol2=int(Criminal_Tool.check_state / 10),int(Criminal_Tool.check_state % 10)
            if(symbol1 >= symbol2):
                temp = self.calculate(n1,n2,symbol1)
                self.result = self.calculate(temp,n3,symbol2)
            else:
                temp = self. calculate(n2,n3,symbol2)
                self.result = self.calculate(n1,temp,symbol1)

            if self.result == self.attack_value:
                Criminal_Tool.tool_cnt[symbol1] -=1
                Criminal_Tool.tool_cnt[symbol2] -=1
                text_box.string1 = "나의 결과값은 %3d"%self.result + " 입니다.      "
                text_box.string2 = "카운터 공격 성공!!!                         "
                text_box.string3 = "결과값이 적의 공격값과 정확히 일치합니다!     "
                text_box.string4 = "이번 턴은 도구 사용횟수가 오르지 않습니다.     "
            else:
                if self.result <0: self.result =0
                string_tool1=""
                string_tool2=""
                if symbol1 == Criminal_Tool.HAMMER: string_tool1 = "망치"
                elif symbol1 == Criminal_Tool.CHAIN: string_tool1 = "쇠사슬"
                elif symbol1 == Criminal_Tool.SPANNER: string_tool1 = "스패너"
                elif symbol1 == Criminal_Tool.KNIFE: string_tool1 = "칼"
                if symbol2 == Criminal_Tool.HAMMER: string_tool2 = "망치"
                elif symbol2 == Criminal_Tool.CHAIN: string_tool2 = "쇠사슬"
                elif symbol2 == Criminal_Tool.SPANNER: string_tool2 = "스패너"
                elif symbol2 == Criminal_Tool.KNIFE: string_tool2 = "칼"
                text_box.string1 = "나의 결과값은 %3d"%self.result + " 입니다.                    "
                if symbol1 != symbol2 :
                    text_box.string3 = string_tool1 +", " + string_tool2 + "의 사용횟수가             "
                    text_box.string4 = "각각 1회 증가했습니다.                                    "
                else:
                    text_box.string3 = string_tool1 + "의 사용횟수가 2회 증가했습니다.                 "
                    text_box.string4 = "                                                         "
                text_box.string2 = "                                                            "
            self.result_one = (int)(self.result % 10) #일의 자리
            self.result_ten = (int)(self.result / 10) #십의 자리
            if self.result_ten == 0:
                self.result_one_x,self.result_one_y= 770,200
            else:
                self.result_one_x,self.result_one_y= 790,200

            self.switch +=1

        if battle_step == STEP_TURN_END and self.switch == 1:
            text_box.string1 = "                               "
            text_box.string2 = "                                "
            text_box.string3 = "                               "
            text_box.string4 = "                               "
            if self.result == self.attack_value:
                enem.hp -= self.result
                text_box.string1 = "카운터 공격에 성공했으므로                   "
                text_box.string2 = "상대에게 %3d"%self.result + " 만큼의 피해를 입힙니다.        "
            elif self.result > self.attack_value:
                enem.hp -= (self.result - self.attack_value)
                text_box.string1 = "나의 결과값이 상대보다 크므로                "
                text_box.string2 = "상대에게 %3d"%(self.result - self.attack_value) + " 만큼의 피해를 주었습니다.           "
            else:
                Player.hp -= (self.attack_value - self.result)
                text_box.string1 = "나의 결과값이 상대보다 작으므로              "
                text_box.string2 = "내가 %3d"%(self.attack_value - self.result) + " 만큼의 피해를 받았습니다.           "
            if enem.hp <=0:
                enem.hp =0
                text_box.string4 = "상대의 체력이 0이 되었습니다!           "
            if Player.hp <=0 :
                Player.hp =0
                text_box.string4 = "나의 체력이 0이 되었습니다!            "
            self.switch = 0

    def calculate(self,n1,n2,sym):
        if sym == Criminal_Tool.HAMMER: #더하기
            Criminal_Tool.tool_cnt[1] +=1
            return n1 + n2
        elif sym == Criminal_Tool.CHAIN: #빼기
            Criminal_Tool.tool_cnt[2] +=1
            return n1 - n2
        elif sym == Criminal_Tool.SPANNER: #곱하기
            Criminal_Tool.tool_cnt[3] +=1
            return n1 * n2
        elif sym == Criminal_Tool.KNIFE: #시그마
            Criminal_Tool.tool_cnt[4] +=1
            sum = 0
            if(n1 - n2 < 0):
                while n1 <= n2:
                    sum += n1
                    n1+=1
            else:
                while n2 <= n1:
                    sum+=n2
                    n2+=1
            return sum

    def draw(self):
        self.image.clip_draw(self.enem_one * 55, 0, 55, 65, self.enem_one_x,self.enem_one_y)
        if(self.enem_ten > 0):
                self.image.clip_draw(self.enem_ten * 55, 0, 55, 65, self.enem_one_x-38,self.enem_one_y)
        if(battle_step >= STEP_CHECK_RESULT):
            self.image.clip_draw(self.result_one * 55, 0, 55, 65, self.result_one_x, self.result_one_y)
            if(self.result_ten > 0):
                self.image.clip_draw(self.result_ten * 55, 0, 55, 65, self.result_one_x-38, self.result_one_y)


class Hp:
    user_image=enem_image=None
    def __init__(self,player,enem):
        self.enem_hp_one = int(enem.hp % 10)
        self.enem_hp_ten = int(enem.hp / 10)
        self.user_hp_one = int(player.hp % 10)
        self.user_hp_ten = int(player.hp / 10)
        if Hp.user_image == None:
            Hp.user_image=load_image('Battle_State/hp_numbers_red.png')
        if Hp.enem_image == None:
            Hp.enem_image=load_image('Battle_State/hp_numbers_blue.png')

    def update(self,player,enem):
        self.enem_hp_one = int(enem.hp % 10)
        self.enem_hp_ten = int(enem.hp / 10)
        self.user_hp_one = int(player.hp % 10)
        self.user_hp_ten = int(player.hp / 10)


    def draw(self):
        if(self.enem_hp_ten > 0):
                self.enem_image.clip_draw(self.enem_hp_ten * 60, 0, 60, 67, 735,410)
                self.enem_image.clip_draw(self.enem_hp_one * 60, 0, 60, 67, 795,410)
        else:
            self.enem_image.clip_draw(self.enem_hp_one * 60, 0, 60, 67, 760,410)

        if(self.user_hp_ten > 0):
            self.user_image.clip_draw(self.user_hp_ten * 100, 0, 100, 128, 1011, 72)
        self.user_image.clip_draw(self.user_hp_one * 100, 0, 100, 128, 1111, 72)


###############################################################
name = "BattleState"
image = None
text_image = None
STEP_ENEMY_TURN, STEP_USER_TURN, STEP_SELECT_TOOLS, STEP_CHECK_RESULT, STEP_TURN_END, STEP_BATTLE_END= 0,1,2,3,4,5
battle_step=STEP_ENEMY_TURN
Player= None
"""
step0 : 처음 시작
step1 : 적의 공격값 제시, 주사위 굴러감
step2 : 주사위 값 나옴, 연산기호선택
step3 : 결과값 나옴(디스플레이)
step4 : 결과값에 따른 체력 적용, 사용한 총 범행도구 수 확인
-> 전투가 끝나지 않았으면 다시 1로
-> 전투 끝(step5)
step5 전투종료 (승리 혹은 패배)
"""

# 메인에서 유저객체와 npc의 타입을 받아와 설정해준다.
def enter(user,npc):
    global ground_image, text_image, tool_group, dice_group,ani_group,enemy, textbox, number, hp, Player, cursor
    Player = user
    ground_image = load_image('Battle_State/battle_ground_test3.png')
    text_image = load_image('Battle_State/battle_text_box.png')
    text_image.opacify(0.8)
    textbox=Textbox()
    tool_group=[Criminal_Tool(i) for i in range(1,5)]
    dice_group=[Dice_Number(i,Player.dice_num) for i in range(3)]
    ani_group=[Dice_Animation(i) for i in range(3)]
    enemy = Enemy(npc)
    number=Number()
    hp=Hp(Player,enemy)
    for i in range(0,5):
        Criminal_Tool.tool_cnt[i] =0
    cursor=class_cursor.Cursor()


def exit():
    global ground_image, text_image, tool_group, dice_group,ani_group,enemy, textbox, number, hp
    del(ground_image)
    del(text_image)
    for tool in tool_group:
        del(tool)
    for dice in dice_group:
        del(dice)
    for ani in ani_group:
        del(ani)
    del(enemy)
    del(textbox)
    del(number)
    del(hp)

def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    global battle_step,cursor
    events=get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
                #버튼키를 누를 때
            elif event.key == SDLK_z:
                if(battle_step < STEP_SELECT_TOOLS):
                    battle_step +=1
                elif battle_step ==STEP_SELECT_TOOLS and int(Criminal_Tool.check_state / 10)!=0 and int(Criminal_Tool.check_state % 10)!=0:
                    battle_step +=1
                elif battle_step == STEP_CHECK_RESULT:
                    battle_step +=1
                elif battle_step == STEP_TURN_END:
                    if Player.hp == 0:
                        battle_lose()
                        battle_step +=1
                    elif enemy.hp == 0:
                        battle_win()
                        battle_step +=1
                    else:
                        initialize_turn()
                elif battle_step == STEP_BATTLE_END: #결과창 떠있는 상태
                    initialize_turn()
                    game_framework.pop_state()
        if(event.type == SDL_MOUSEMOTION):
            class_cursor.Cursor.x, class_cursor.Cursor.y=event.x,600-event.y
            for tool in tool_group:
                #손가락을 펼치는 조건들
                if battle_step == STEP_SELECT_TOOLS and collide(event.x,600-event.y,tool) and tool.state == tool.IDLE and ( int(Criminal_Tool.check_state / 10)==0 or int(Criminal_Tool.check_state % 10)==0):
                    cursor.state = cursor.PAPER
                    break
                else:
                    cursor.state = cursor.IDLE
            for tool in tool_group:
                if tool.state == tool.GRABBED: # 잡은 상태에서 드래그
                    cursor.state = cursor.ROCK
                    tool.x=event.x
                    tool.y=600-event.y
        #마우스 버튼 클릭
        if(event.type == SDL_MOUSEBUTTONDOWN):
            #왼쪽
            if (event.button == SDL_BUTTON_LEFT) and ( int(Criminal_Tool.check_state / 10)==0 or int(Criminal_Tool.check_state % 10)==0):
                for tool in tool_group:
                    if battle_step == STEP_SELECT_TOOLS and collide(event.x,600-event.y,tool) and tool.state == tool.IDLE:
                        cursor.state=cursor.ROCK
                        tool.x=event.x
                        tool.y= 600-event.y
                        tool.state = tool.GRABBED # 잡은 상태
                        if tool.type == tool.HAMMER:
                            textbox.wait = 1
                            textbox.string1 = " [망치]                            "
                            textbox.string2 = "     왼쪽 숫자 + 오른쪽 숫자               "
                            textbox.string3 = "     연산우선순위 4번째                    "
                            textbox.string4 = "                                         "
                        elif tool.type ==tool.CHAIN:
                            textbox.wait = 1
                            textbox.string1 = " [쇠사슬]                                "
                            textbox.string2 = "     왼쪽 숫자 - 오른쪽 숫자               "
                            textbox.string3 = "     연산우선순위 3번째                       "
                            textbox.string4 = "                                       "
                        elif tool.type ==tool.SPANNER:
                            textbox.wait = 1
                            textbox.string1 = " [스패너]                               "
                            textbox.string2 = "     왼쪽 숫자 x 오른쪽 숫자                   "
                            textbox.string3 = "     연산우선순위 2번째                          "
                            textbox.string4 = "스패너는 한 턴에 한번만 사용할 수 있습니다."
                        elif tool.type ==tool.KNIFE:
                            textbox.wait = 1
                            textbox.string1 = " [칼]                              "
                            textbox.string2 = "     '작은수~큰수' 사이 모든 수의 합            "
                            textbox.string3 = "     연산우선순위 1번째                     "
                            textbox.string4 = "칼은 한 턴에 한번만 사용할 수 있습니다."
            #오른쪽
            if (event.button == SDL_BUTTON_RIGHT):
                 for tool in tool_group:
                    if battle_step == STEP_SELECT_TOOLS and collide(event.x,600-event.y,tool):
                        if tool.state == tool.FIRST_SELECTED: #첫번째 칸을 오른쪽클릭
                            Criminal_Tool.check_state -=10*tool.type
                            tool_group.remove(tool)
                        elif tool.state == tool.SECOND_SELECTED:
                            Criminal_Tool.check_state -=tool.type
                            tool_group.remove(tool)
        #마우스 왼쪽 버튼을 떼었을 때
        elif(event.type == SDL_MOUSEBUTTONUP and event.button ==SDL_BUTTON_LEFT and event.button !=SDL_BUTTON_RIGHT):
            cursor.state=cursor.IDLE
            for tool in tool_group:
                if tool.state ==tool.GRABBED:
                    toolbox=collide_toolbox(tool)
                    first_box_type = int(Criminal_Tool.check_state / 10) # 첫번째 연산기호 (십의 자리)
                    second_box_type = int(Criminal_Tool.check_state % 10) # 두번째 연산기호 (일의 자리)
                    textbox.wait=0
                    if first_box_type == 0 and toolbox == 1 and (tool.type < tool.SPANNER or tool.type !=second_box_type): # 첫번째칸이 비었고, 첫번째 안에서 마우스버튼을 떼었을 때
                        tool.state = tool.FIRST_SELECTED #첫번째 캄
                        tool.x, tool.y = 203, 185
                        Criminal_Tool.check_state +=10*tool.type
                        tool_group.append(Criminal_Tool(tool.type))
                    elif second_box_type == 0 and toolbox == 2 and (tool.type < tool.SPANNER or tool.type !=first_box_type):
                            tool.state = tool.SECOND_SELECTED #두번째 칸
                            tool.x, tool.y = 460,185
                            Criminal_Tool.check_state +=tool.type
                            tool_group.append(Criminal_Tool(tool.type))
                    else:
                        tool.__init__(tool.type) #원래 자리로 초기화


def collide(mouse_x,mouse_y,object):
    left_b, bottom_b, right_b, top_b = object.get_bb()
    if mouse_x > right_b: return False
    if mouse_x < left_b: return False
    if mouse_y < bottom_b: return False
    if mouse_y > top_b: return False
    return True

def collide_toolbox(tool):
    if 142 < tool.x and tool.x < 264 and 124 < tool.y and tool.y < 246: return 1 # 첫번째 칸
    elif 400 < tool.x and tool.x < 520 and 124 < tool.y and tool.y <246 : return 2 # 두번째 칸
    else: return 0

def initialize_turn():
    global battle_step, tool_group
    battle_step = STEP_ENEMY_TURN
    Criminal_Tool.check_state =0
    for tool in tool_group:
        del(tool)
    tool_group=[Criminal_Tool(i) for i in range(1,5)]
    for dice in dice_group:
        dice.frame=0
    enemy.set_attack_value()

def battle_win():
    global Player, enemy
    Player.gold += enemy.gold
    suspicion_sum=0
    textbox.string1 = "강도질 성공!!                              "
    textbox.string2 = "카운터 공격으로만 상대를 제압했습니다.          "
    textbox.string3 = "완전 범죄이므로 혐의가 오르지 않습니다.          "
    #가장 많이 사용한 도구 찾기
    max_index=1
    for i in range(2,5):
        if Criminal_Tool.tool_cnt[i] >= Criminal_Tool.tool_cnt[max_index]:
            max_index = i

    if Criminal_Tool.tool_cnt[max_index] != 0: #완전범죄가 아닐 때
        suspicion_sum += enemy.type #기본 혐의값
        if Player.last_tool == max_index: #지난 범죄와 같은 도구면
            suspicion_sum += enemy.type
        Player.last_tool = max_index
        if Player.last_tool == Criminal_Tool.HAMMER:            Player.tool_s = "망치"
        elif Player.last_tool == Criminal_Tool.CHAIN:            Player.tool_s = "쇠사슬"
        elif Player.last_tool == Criminal_Tool.SPANNER:            Player.tool_s = "스패너"
        elif Player.last_tool == Criminal_Tool.KNIFE:            Player.tool_s = "칼"
        if Player.last_type == enemy.type: #지난 범죄와 같은 유형의 피해자면
            suspicion_sum += enemy.type
        Player.last_type = enemy.type
        Player.type_s = enemy.type_s

        if Player.last_place == Player.place:
            suspicion_sum += enemy.type
        Player.last_place = Player.place
        Player.place_s = Player.place+'구역'
        Player.suspicion += suspicion_sum

        textbox.string1 = "강도질 성공!!                                     "
        textbox.string2 = Player.place_s+"에서  "+ Player.type_s +"을(를)  "+ Player.tool_s+ "로     "
        textbox.string3 = "강도질에 성공했습니다.            "
    textbox.string4 = "혐의 +"+"%3d"%suspicion_sum + "%" + ",    돈 + " + "%5d"%enemy.gold +"원        "

def battle_lose():
    global Player
    #피해자
    Player.last_type = enemy.type
    Player.type_s = enemy.type_s
    #범행도구
    max_index=1
    for i in range(2,5):
        if Criminal_Tool.tool_cnt[i] >= Criminal_Tool.tool_cnt[max_index]:
            max_index = i
    Player.last_tool = max_index
    if Player.last_tool == Criminal_Tool.HAMMER:            Player.tool_s = "망치"
    elif Player.last_tool == Criminal_Tool.CHAIN:            Player.tool_s = "쇠사슬"
    elif Player.last_tool == Criminal_Tool.SPANNER:            Player.tool_s = "스패너"
    elif Player.last_tool == Criminal_Tool.KNIFE:            Player.tool_s = "칼"
    #장소
    Player.last_place = Player.place
    Player.place_s = Player.place+'구역'

    textbox.string1 = "강도질 실패...                                     "
    textbox.string2 = "혐의가 대폭 증가합니다.                             "
    textbox.string3 = "병원으로 이송되었습니다.                            "
    textbox.string4 = "혐의 +"+"%3d"%(enemy.type * 4) + "%                "
    Player.x,Player.y,Player.state = 256,224,Player.Down
    Player.hp= 20 # 죽으면 체력은 20으로 (20을 채우는 비용 < 혐의 4퍼 낮추는 비용)
    Player.suspicion += (enemy.type * 4)



def update(frame_time):
    global Player
    for ani in ani_group:
        ani.update()
    for dice in dice_group:
        dice.update()
    number.update(enemy,dice_group,textbox)
    if battle_step <= STEP_TURN_END:
        hp.update(Player,enemy)
        textbox.update(enemy,Player)


def draw(frame_time):
    clear_canvas()
    ground_image.draw(600,300)
    text_image.draw(1018,383)
    textbox.draw()
    enemy.draw()
    for dice in dice_group:
        dice.draw()
    for ani in ani_group:
        ani.draw()
    number.draw()
    hp.draw()

    #안 잡은 도구들
    for tool in tool_group:
        if tool.state != tool.GRABBED:
            tool.draw()
    #잡은 도구 마지막에
    for tool in tool_group:
        if tool.state == tool.GRABBED:
            tool.draw()
            break

    cursor.draw()
    update_canvas()
    delay(0.03)




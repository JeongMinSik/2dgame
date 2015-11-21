from pico2d import *
import random

class Npc:
    DOWN, UP, LEFT, RIGHT = 3, 2, 1, 0
    # 10번 할머니, 20번 할아버지 30번 소녀 40번 소년 50번 젊은여성 60번 젊은남성 70번 경찰
    GRANDMA,GRANDPA,GIRL,BOY,WOMAN,MAN,POLICE= 1,2,3,4,5,6,70

    PIXEL_PER_METER = (8 / 1)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 60.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3

    DISTANCE = 8

    def __init__(self,x,y,user,bg,npc_group=None,type=None):
        npc_data_file = open('Data/Npc.txt','r')
        npc_data = json.load(npc_data_file)
        npc_data_file.close()
        self.x, self.y = x, y
        self.npc_group =npc_group
        self.bg=bg
        self.user=user
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.frame = 0
        self.running = False
        self.waiting_time = 0
        self.dir = self.DOWN
        self.state = random.randint(0,3)
        self.type_s = " "
        self.speech = "\"디폴트!\"                        "
        self.place = ""
        if type == None:
            self.select_type() # 타입지정
        elif type <70:
            self.type = type
        else:
            self.type = self.POLICE
            self.type_s="경찰"
            self.speech = "\"이 마을의 치안은 저한테 맡기세요!\"                 "
        if   self.type == npc_data['Grandma']['rangemin']:     self.image = load_image('Npc/oldwoman_0.png')
        elif self.type == npc_data['Grandma']['rangemin']+1:     self.image = load_image('Npc/oldwoman_1.png')
        elif self.type == npc_data['Grandma']['rangemin']+2:     self.image = load_image('Npc/oldwoman_2.png')
        elif self.type == npc_data['Grandpa']['rangemin']:     self.image = load_image('Npc/oldman_0.png')
        elif self.type == npc_data['Grandpa']['rangemin']+1:     self.image = load_image('Npc/oldman_1.png')
        elif self.type == npc_data['Grandpa']['rangemin']+2:     self.image = load_image('Npc/oldman_2.png')
        elif self.type == npc_data['Grandpa']['rangemin']+3:     self.image = load_image('Npc/oldman_3.png')
        elif self.type == npc_data['Girl']['rangemin']:     self.image = load_image('Npc/girl_0.png')
        elif self.type == npc_data['Girl']['rangemin']+1:     self.image = load_image('Npc/girl_1.png')
        elif self.type == npc_data['Girl']['rangemin']+2:     self.image = load_image('Npc/girl_2.png')
        elif self.type == npc_data['Girl']['rangemin']+3:     self.image = load_image('Npc/girl_3.png')
        elif self.type == npc_data['Girl']['rangemin']+4:     self.image = load_image('Npc/girl_4.png')
        elif self.type == npc_data['Girl']['rangemin']+5:     self.image = load_image('Npc/girl_5.png')
        elif self.type == npc_data['Boy']['rangemin']:     self.image = load_image('Npc/boy_0.png')
        elif self.type == npc_data['Boy']['rangemin']+1:     self.image = load_image('Npc/boy_1.png')
        elif self.type == npc_data['Boy']['rangemin']+2:     self.image = load_image('Npc/boy_2.png')
        elif self.type == npc_data['Boy']['rangemin']+3:     self.image = load_image('Npc/boy_3.png')
        elif self.type == npc_data['Boy']['rangemin']+4:     self.image = load_image('Npc/boy_4.png')
        elif self.type == npc_data['Boy']['rangemin']+5:     self.image = load_image('Npc/boy_5.png')
        elif self.type == npc_data['Boy']['rangemin']+6:     self.image = load_image('Npc/boy_6.png')
        elif self.type == npc_data['Woman']['rangemin']:     self.image = load_image('Npc/woman_0.png')
        elif self.type == npc_data['Woman']['rangemin']+1:     self.image = load_image('Npc/woman_1.png')
        elif self.type == npc_data['Woman']['rangemin']+2:     self.image = load_image('Npc/woman_2.png')
        elif self.type == npc_data['Woman']['rangemin']+3:     self.image = load_image('Npc/woman_3.png')
        elif self.type == npc_data['Woman']['rangemin']+4:     self.image = load_image('Npc/woman_4.png')
        elif self.type == npc_data['Woman']['rangemin']+5:     self.image = load_image('Npc/woman_5.png')
        elif self.type == npc_data['Woman']['rangemin']+6:     self.image = load_image('Npc/woman_6.png')
        elif self.type == npc_data['Woman']['rangemin']+7:     self.image = load_image('Npc/woman_7.png')
        elif self.type == npc_data['Woman']['rangemin']+8:     self.image = load_image('Npc/woman_8.png')
        elif self.type == npc_data['Woman']['rangemin']+9:     self.image = load_image('Npc/woman_9.png')
        elif self.type == npc_data['Man']['rangemin']:     self.image = load_image('Npc/man_0.png')
        elif self.type == npc_data['Man']['rangemin']+1:     self.image = load_image('Npc/man_1.png')
        elif self.type == npc_data['Man']['rangemin']+2:     self.image = load_image('Npc/man_2.png')
        elif self.type == npc_data['Man']['rangemin']+3:     self.image = load_image('Npc/man_3.png')
        elif self.type == npc_data['Man']['rangemin']+4:     self.image = load_image('Npc/man_4.png')
        elif self.type == npc_data['Man']['rangemin']+5:     self.image = load_image('Npc/man_5.png')
        elif self.type == npc_data['Man']['rangemin']+6:     self.image = load_image('Npc/man_6.png')
        elif self.type == npc_data['Man']['rangemin']+7:     self.image = load_image('Npc/man_7.png')
        elif self.type == npc_data['Man']['rangemin']+8:     self.image = load_image('Npc/man_8.png')
        elif self.type == npc_data['Man']['rangemin']+9:     self.image = load_image('Npc/man_9.png')
        elif self.type == npc_data['Man']['rangemin']+10:     self.image = load_image('Npc/street_police.png')

    def select_type(self):
        bigtype = random.randint(1,6)
        find_switch =0 #같은 타입이 이미 존재하는걸 찾았는가?
        npc_data_file = open('Data/Npc.txt','r')
        npc_data = json.load(npc_data_file)
        npc_data_file.close()
        while(1):
            if(bigtype == self.GRANDMA):
                for i in range(npc_data['Grandma']['rangemin'],npc_data['Grandma']['rangemax']):
                    self.type = i
                    for npc in self.npc_group:
                        if(self.type == npc.type):
                            find_switch=1
                            break
                    if find_switch == 0:
                        self.type_s = " 할머니"
                        self.speech = "\"반가워요 호호호...\"                   "
                        return
                    else: find_switch = 0
                bigtype +=1
            if(bigtype ==self.GRANDPA):
                for i in range(npc_data['Grandpa']['rangemin'],npc_data['Grandpa']['rangemax']):
                    self.type = i
                    for npc in self.npc_group:
                        if(self.type == npc.type):
                            find_switch=1
                            break
                    if find_switch == 0:
                        self.type_s = "할아버지"
                        self.speech = "\"아이고 허리야...\"                          "
                        return
                    else: find_switch=0
                bigtype +=1
            if(bigtype ==self.GIRL):
                for i in range(npc_data['Girl']['rangemin'],npc_data['Girl']['rangemax']):
                    self.type = i
                    for npc in self.npc_group:
                        if(self.type == npc.type):
                            find_switch=1
                            break
                    if find_switch == 0:
                        self.type_s = "소녀"
                        self.speech = "\"안녕하세요!\"                   "
                        return
                    else: find_switch=0
                bigtype +=1
            if(bigtype ==self.BOY):
                for i in range(npc_data['Boy']['rangemin'],npc_data['Boy']['rangemax']):
                    self.type = i
                    for npc in self.npc_group:
                        if(self.type == npc.type):
                            find_switch=1
                            break
                    if find_switch == 0:
                        self.type_s = "소년"
                        self.speech = "\"왜 불러요! 바쁘다구요!!\"                 "
                        return
                    else: find_switch=0
                bigtype +=1
            if(bigtype ==self.WOMAN):
                for i in range(npc_data['Woman']['rangemin'],npc_data['Woman']['rangemax']):
                    self.type = i
                    for npc in self.npc_group:
                        if(self.type == npc.type):
                            find_switch=1
                            break
                    if find_switch == 0:
                        self.type_s = "젊은여성"
                        self.speech = "\"길 막지 말고 비켜줄래요?\"                 "
                        return
                    else: find_switch =0
                bigtype +=1
            if(bigtype ==self.MAN):
                for i in range(npc_data['Man']['rangemin'],npc_data['Man']['rangemax']):
                    self.type = i
                    for npc in self.npc_group:
                        if(self.type == npc.type):
                            find_switch = 1
                            break
                    if find_switch == 0:
                        self.type_s = "젊은남성"
                        self.speech = "\"저한테 무슨 볼일이라도?\"                 "
                        return
                    else: find_switch = 0
                bigtype = self.GRANDMA


    def get_bb(self):
        return self.x -8,self.y-13,self.x+8, self.y+9

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def set_npcgroup(self,ng):
        self.npc_group=ng

    def collide(self,user):
          left_a, bottom_a, right_a, top_a = self.get_bb()
          left_b, bottom_b, right_b, top_b = user.get_bb()
          if left_a > right_b: return False
          if right_a < left_b: return False
          if top_a < bottom_b: return False
          if bottom_a > top_b: return False
          return True

    def check_police_place(self):
        place_data_file = open('Data/Place.txt','r')
        place_data = json.load(place_data_file)
        place_data_file.close()
        if self.type == self.POLICE:
            if self.y >= place_data['North']['y']:   self.place = 'N'
            elif self.y <= place_data['South']['y']: self.place = 'S'
            else:
                temp_x, temp_y = place_data['East_West']['x'], place_data['North']['y']
                while temp_y > place_data['South']['y']:
                    if self.x >temp_x and self.y == temp_y:
                        self.place = 'E'
                        break
                    elif self.x <= temp_x and self.y == temp_y:
                        self.place = 'W'
                        break
                    temp_x -=Npc.DISTANCE
                    temp_y -=Npc.DISTANCE

    def move(self,frame_time,entrance_group):
        self.waiting_time += frame_time
        if self.running == True:
            if self.waiting_time > self.type / 30: # n초간 달린 후 휴식
                self.running =  False
                self.waiting_time = 0
            if self.dir == self.RIGHT:
                self.x+=Npc.DISTANCE
                for npc in self.npc_group:
                    if (npc.type != self.type and self.collide(npc)) or self.collide(self.user) or self.bg.map_matrix[int(self.y / Npc.DISTANCE)][int(self.x / Npc.DISTANCE)] != 0:
                        self.x-=Npc.DISTANCE
                        self.frame = 0
                        return
                self.state = self.RIGHT
                self.frame = self.frame = (self.frame +1) % 3
            elif self.dir == self.LEFT:
                self.x-=Npc.DISTANCE
                #병원 주변에는 못 가도록
                place_data_file = open('Data/Place.txt','r')
                place_data = json.load(place_data_file)
                place_data_file.close()
                if self.x <=place_data['Hospital']['x'] and self.y >= place_data['Hospital']['bottom'] and self.y <=place_data['Hospital']['top']:
                    self.x += Npc.DISTANCE
                    self.frame = 0
                    return
                for npc in self.npc_group:
                    if (npc.type != self.type and self.collide(npc)) or  self.collide(self.user) or self.bg.map_matrix[int(self.y / Npc.DISTANCE)][int(self.x / Npc.DISTANCE)] != 0:
                        self.x += Npc.DISTANCE
                        self.frame = 0
                        return
                self.state = self.LEFT
                self.frame = self.frame = (self.frame +1) % 3
            elif self.dir == self.UP:
                self.x+=Npc.DISTANCE
                self.y+=Npc.DISTANCE
                for npc in self.npc_group:
                    if (npc.type != self.type and self.collide(npc)) or  self.collide(self.user) or self.bg.map_matrix[int(self.y / Npc.DISTANCE)][int(self.x / Npc.DISTANCE)] != 0:
                        self.y -= Npc.DISTANCE
                        self.x -= Npc.DISTANCE
                        self.frame = 0
                        return
                for ent in entrance_group:
                    if self.collide(ent):
                        self.y -= Npc.DISTANCE
                        self.x -= Npc.DISTANCE
                        self.frame = 0
                        return
                self.state = self.UP
                self.frame = self.frame = (self.frame +1) % 3
            elif self.dir ==self.DOWN:
                self.x-=Npc.DISTANCE
                self.y-=Npc.DISTANCE
                for npc in self.npc_group:
                    if (npc.type != self.type and self.collide(npc)) or self.collide(self.user) or self.bg.map_matrix[int(self.y / Npc.DISTANCE)][int(self.x / Npc.DISTANCE)] != 0:
                        self.y += Npc.DISTANCE
                        self.x += Npc.DISTANCE
                        self.frame = 0
                        return
                self.state = self.DOWN
                self.frame = self.frame = (self.frame +1) % 3
        else:
            self.frame = 0
            if self.waiting_time > 1:
                self.running = True
                self.wating_time = 0
                self.dir = random.randint(0,3)

    def update(self,frame_time,entrance_group):
        self.check_police_place()
        self.move(frame_time,entrance_group)


    def draw(self):
       if (self.user.x - self.canvas_width//2 >= 0 ): # 주인공좌표-캔버스반값이 양수일때
           if self.user.x+ self.canvas_width//2 <= self.bg.w:  # 주인공좌표+캔버스반값이 맵을 초과하지 않을 때
                position_x = self.x - (self.user.x - self.canvas_width//2) # 주인공좌표-캔버스반값 만큼 NPC.x의 값을 감소시킨다.
           else:
               position_x = self.x - (self.bg.w - self.canvas_width) # 주인공좌표를 최대값으로 치환한다. (이 경우 오른쪽 끝)
       else: #이 경우 왼쪽에 있는 것이므로 그냥 그대로 그려주면 된다.
           position_x=self.x

       if self.user.y - self.canvas_height//2 >= 0:
           if(self.user.y+ self.canvas_height//2 <= self.bg.h):
               position_y = self.y - (self.user.y - self.canvas_height//2)
           else:
               position_y = self.y - (self.bg.h - self.canvas_height)
       else:
           position_y=self.y

       self.image.clip_draw(self.frame * 32, self.state*32, 32, 32, position_x,position_y)

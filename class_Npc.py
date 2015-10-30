from pico2d import *
import random

class Npc:
    DOWN, UP, LEFT, RIGHT = 3, 2, 1, 0
    # 10번 할머니, 20번 할아버지 30번 소녀 40번 소년 50번 젊은여성 60번 젊은남성 70번 경찰
    GRANDMA,GRANDPA,GIRL,BOY,WOMAN,MAN,POLICE= 1,2,3,4,5,6,70
    OFF,ON = 0 ,1
    def __init__(self,x,y,user,bg,npc_group=None,police=None):
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
        if police == None:
            self.select_type() # 타입지정
        else:
            self.type = self.POLICE
            self.type_s="경찰"
            self.speech = "\"이 마을의 치안은 저한테 맡기세요!\"                 "
        if   self.type == 10:     self.image = load_image('Npc/oldwoman_0.png')
        elif self.type == 11:     self.image = load_image('Npc/oldwoman_1.png')
        elif self.type == 12:     self.image = load_image('Npc/oldwoman_2.png')
        elif self.type == 20:     self.image = load_image('Npc/oldman_0.png')
        elif self.type == 21:     self.image = load_image('Npc/oldman_1.png')
        elif self.type == 22:     self.image = load_image('Npc/oldman_2.png')
        elif self.type == 23:     self.image = load_image('Npc/oldman_3.png')
        elif self.type == 30:     self.image = load_image('Npc/girl_0.png')
        elif self.type == 31:     self.image = load_image('Npc/girl_1.png')
        elif self.type == 32:     self.image = load_image('Npc/girl_2.png')
        elif self.type == 33:     self.image = load_image('Npc/girl_3.png')
        elif self.type == 34:     self.image = load_image('Npc/girl_4.png')
        elif self.type == 35:     self.image = load_image('Npc/girl_5.png')
        elif self.type == 40:     self.image = load_image('Npc/boy_0.png')
        elif self.type == 41:     self.image = load_image('Npc/boy_1.png')
        elif self.type == 42:     self.image = load_image('Npc/boy_2.png')
        elif self.type == 43:     self.image = load_image('Npc/boy_3.png')
        elif self.type == 44:     self.image = load_image('Npc/boy_4.png')
        elif self.type == 45:     self.image = load_image('Npc/boy_5.png')
        elif self.type == 46:     self.image = load_image('Npc/boy_6.png')
        elif self.type == 50:     self.image = load_image('Npc/woman_0.png')
        elif self.type == 51:     self.image = load_image('Npc/woman_1.png')
        elif self.type == 52:     self.image = load_image('Npc/woman_2.png')
        elif self.type == 53:     self.image = load_image('Npc/woman_3.png')
        elif self.type == 54:     self.image = load_image('Npc/woman_4.png')
        elif self.type == 55:     self.image = load_image('Npc/woman_5.png')
        elif self.type == 56:     self.image = load_image('Npc/woman_6.png')
        elif self.type == 57:     self.image = load_image('Npc/woman_7.png')
        elif self.type == 58:     self.image = load_image('Npc/woman_8.png')
        elif self.type == 59:     self.image = load_image('Npc/woman_9.png')
        elif self.type == 60:     self.image = load_image('Npc/man_0.png')
        elif self.type == 61:     self.image = load_image('Npc/man_1.png')
        elif self.type == 62:     self.image = load_image('Npc/man_2.png')
        elif self.type == 63:     self.image = load_image('Npc/man_3.png')
        elif self.type == 64:     self.image = load_image('Npc/man_4.png')
        elif self.type == 65:     self.image = load_image('Npc/man_5.png')
        elif self.type == 66:     self.image = load_image('Npc/man_6.png')
        elif self.type == 67:     self.image = load_image('Npc/man_7.png')
        elif self.type == 68:     self.image = load_image('Npc/man_8.png')
        elif self.type == 69:     self.image = load_image('Npc/man_9.png')
        elif self.type == 70:     self.image = load_image('Npc/street_police.png')

    def select_type(self):
        bigtype = random.randint(1,6)
        find_switch =0 #같은 타입이 이미 존재하는걸 찾았는가?
        while(1):
            if(bigtype == self.GRANDMA):
                for i in range(10,13):
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
                for i in range(20,24):
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
                for i in range(30,36):
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
                for i in range(40,47):
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
                for i in range(50,60):
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
                for i in range(60,70):
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
        return self.x -8,self.y-13,self.x+8, self.y+9  # 폭:16, 높이 22

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
        if self.type == self.POLICE:
            if self.y >= 720:   self.place = 'N'
            elif self.y <= 392: self.place = 'S'
            else:
                temp_x, temp_y = 1168, 720
                while temp_y > 392:
                    if self.x >temp_x and self.y == temp_y:
                        self.place = 'E'
                        break
                    elif self.x <= temp_x and self.y == temp_y:
                        self.place = 'W'
                        break
                    temp_x -=8
                    temp_y -=8

    def move(self,frame_time,entrance_group):
        self.waiting_time += frame_time
        if self.running == True:
            if self.waiting_time > self.type / 30: # n초간 달린 후 휴식
                self.running =  False
                self.waiting_time = 0
            if self.dir == self.RIGHT:
                self.x+=8
                for npc in self.npc_group:
                    if (npc.type != self.type and self.collide(npc)) or self.collide(self.user) or self.bg.map_matrix[int(self.y / 8)][int(self.x / 8)] != 0:
                        self.x-=8
                        self.frame = 0
                        return
                self.state = self.RIGHT
                self.frame = self.frame = (self.frame +1) % 3
            elif self.dir == self.LEFT:
                self.x-=8
                #병원 주변에는 못 가도록
                if self.x <=320 and self.y >= 200 and self.y <=240:
                    self.x += 8
                    self.frame = 0
                    return
                for npc in self.npc_group:
                    if (npc.type != self.type and self.collide(npc)) or  self.collide(self.user) or self.bg.map_matrix[int(self.y / 8)][int(self.x / 8)] != 0:
                        self.x += 8
                        self.frame = 0
                        return
                self.state = self.LEFT
                self.frame = self.frame = (self.frame +1) % 3
            elif self.dir == self.UP:
                self.x+=8
                self.y+=8
                for npc in self.npc_group:
                    if (npc.type != self.type and self.collide(npc)) or  self.collide(self.user) or self.bg.map_matrix[int(self.y / 8)][int(self.x / 8)] != 0:
                        self.y -= 8
                        self.x -= 8
                        self.frame = 0
                        return
                for ent in entrance_group:
                    if self.collide(ent):
                        self.y -= 8
                        self.x -= 8
                        self.frame = 0
                        return
                self.state = self.UP
                self.frame = self.frame = (self.frame +1) % 3
            elif self.dir ==self.DOWN:
                self.x-=8
                self.y-=8
                for npc in self.npc_group:
                    if (npc.type != self.type and self.collide(npc)) or self.collide(self.user) or self.bg.map_matrix[int(self.y / 8)][int(self.x / 8)] != 0:
                        self.y += 8
                        self.x += 8
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

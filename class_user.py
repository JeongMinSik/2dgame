from pico2d import *

class User:
    image = None
    RIGHT,LEFT,UP,DOWN = 0, 1, 2, 3
    HP_PER_STEPS = 80


    PIXEL_PER_METER = (8 / 1)           # 1 pixel 10 cm
    RUN_SPEED_KMPH = 60.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3

    DISTANCE = 8

    def __init__(self):
        self.meet_sound = load_wav ('Sound/ui_meet.wav')
        self.meet_sound.set_volume(80)

        user_data_file = open('Data/User.txt','r')
        user_data = json.load(user_data_file)
        user_data_file.close()
        self.x, self.y = -1,-1
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.frame = 0
        self.state = self.DOWN
        self.running = False
        self.step_cnt = 0
        self.save_state = 0 #(개발용) 0기본 1저장상태 2삭제상태

        self.hp = self.maxhp = user_data['User']['maxhp']
        self.gold=user_data['User']['gold']
        self.dice_num=user_data['User']['dice']
        self.suspicion= 0
        self.place=''

        self.last_tool =0
        self.last_type =0
        self.last_place =''
        self.tool_s = "------"
        self.type_s = "------"
        self.place_s = "------"
        if User.image == None:
            User.image = load_image('Npc/user.png')

    def get_bb(self):
        return self.x -7,self.y-14,self.x+7, self.y-6

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def collide(self,user):
          left_a, bottom_a, right_a, top_a = self.get_bb()
          left_b, bottom_b, right_b, top_b = user.get_bb()
          if left_a > right_b: return False
          if right_a < left_b: return False
          if top_a < bottom_b: return False
          if bottom_a > top_b: return False
          return True

    def max_value(self):
        if self.hp > self.maxhp:
            self.hp=self.maxhp
        if self.maxhp > 99:
            self.maxhp = 99
        if self.gold > 99999:
            self.gold=99999
        if self.suspicion > 100:
            self.suspicion=100

    def move(self,frame_time):
        if self.running == True:
            self.frame = (self.frame +1) % 3
            if self.state == self.RIGHT:
                self.x += User.DISTANCE
                self.step_cnt +=1
                for npc in self.npc_group:
                    if self.collide(npc) or self.bg.map_matrix[int(self.y / User.DISTANCE)][int(self.x / User.DISTANCE)] != 0:
                        self.x -= User.DISTANCE
                        self.step_cnt -=1
                        break
            elif self.state == self.LEFT:
                self.x -= User.DISTANCE
                self.step_cnt +=1
                for npc in self.npc_group:
                    if self.collide(npc) or self.bg.map_matrix[int(self.y / User.DISTANCE)][int(self.x / User.DISTANCE)] != 0:
                        self.x += User.DISTANCE
                        self.step_cnt -=1
                        break
            elif self.state == self.UP:
                self.y += User.DISTANCE
                self.x += User.DISTANCE
                self.step_cnt +=1
                for npc in self.npc_group:
                    if self.collide(npc) or self.bg.map_matrix[int(self.y / User.DISTANCE)][int(self.x / User.DISTANCE)] != 0:
                       self.y -= User.DISTANCE
                       self.x -= User.DISTANCE
                       self.step_cnt -=1
                       break
            elif self.state == self.DOWN:
                self.y -= User.DISTANCE
                self.x -= User.DISTANCE
                self.step_cnt +=1
                for npc in self.npc_group:
                    if self.collide(npc) or self.bg.map_matrix[int(self.y / User.DISTANCE)][int(self.x / User.DISTANCE)] != 0:
                        self.y += User.DISTANCE
                        self.x += User.DISTANCE
                        self.step_cnt -=1
                        break
        else:
            self.frame = 0
        self.x = clamp(0,self.x,self.bg.w)
        self.y = clamp(0,self.y,self.bg.h)

    def check_user_place(self):
        place_data_file = open('Data/Place.txt','r')
        place_data = json.load(place_data_file)
        place_data_file.close()
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
                temp_x -=User.DISTANCE
                temp_y -=User.DISTANCE

    def update(self,frame_time):
        self.max_value()
        self.move(frame_time)
        self.check_user_place()

        ##############(개발용) 캐릭터가 서 있는 좌표의 배열값을 0 또는 1로 변경#############
        if self.save_state == 1:
            self.bg.map_matrix[int(self.y/8)][int(self.x/8)] = 0
        elif self.save_state == 2:
            self.bg.map_matrix[int(self.y/8)][int(self.x/8)] = 1
        ####################################################################################

    def check_front(self,main_text):
        if self.state == self.RIGHT:
            self.x += User.DISTANCE
            for npc in self.npc_group:
                if self.collide(npc):
                    self.meet_sound.play()
                    npc.state = npc.LEFT
                    main_text.npc =npc
                    self.running =False
            self.x -= User.DISTANCE
        elif self.state == self.LEFT:
            self.x -= User.DISTANCE
            for npc in self.npc_group:
                if self.collide(npc):
                    self.meet_sound.play()
                    npc.state = npc.RIGHT
                    main_text.npc =npc
                    self.running =False
            self.x += User.DISTANCE
        elif self.state == self.UP:
            self.y += User.DISTANCE
            self.x += User.DISTANCE
            for npc in self.npc_group:
                if self.collide(npc):
                    self.meet_sound.play()
                    npc.state = npc.DOWN
                    main_text.npc =npc
                    self.running =False
            self.y -= User.DISTANCE
            self.x -= User.DISTANCE
        elif self.state == self.DOWN:
            self.y -= User.DISTANCE
            self.x -= User.DISTANCE
            for npc in self.npc_group:
                if self.collide(npc):
                    self.meet_sound.play()
                    npc.state = npc.UP
                    main_text.npc =npc
                    self.running =False
            self.y += User.DISTANCE
            self.x += User.DISTANCE

    def set_background(self,bg):
        self.bg=bg

    def set_npcgroup(self,npc_group):
        self.npc_group=npc_group

    def stepbystep(self):
        if self.step_cnt >= self.HP_PER_STEPS:
            if self.hp > 1:     self.hp -=1
            self.step_cnt = 0
            return 1
        else: return 0

    def draw(self):
        x_left_offset = min(0, self.x - self.canvas_width//2)
        x_right_offset = max(0, self.x - self.bg.w + self.canvas_width//2)
        x_offset = x_left_offset + x_right_offset
        y_left_offset = min (0, self.y - self.canvas_height//2)
        y_right_offset = max(0, self.y - self.bg.h + self.canvas_height//2)
        y_offset = y_left_offset + y_right_offset
        self.image.clip_draw(self.frame * 32, self.state*32, 32, 32, self.canvas_width//2+x_offset,self.canvas_height//2+y_offset)

    def handle_event(self, event, main_text):
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_RIGHT or event.key == SDLK_LEFT or event.key ==  SDLK_UP or event.key == SDLK_DOWN:
                    self.running = True
                if event.key == SDLK_RIGHT:
                    self.state = self.RIGHT
                elif event.key == SDLK_LEFT:
                    self.state = self.LEFT
                elif event.key == SDLK_UP:
                    self.state = self.UP
                elif event.key == SDLK_DOWN:
                    self.state = self.DOWN
                elif event.key == SDLK_z:
                    self.check_front(main_text)
            ###########################(개발용) 세이브 데이터###############################
                elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
                    pass
            ####################################################################################
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_RIGHT and self.state == self.RIGHT:
                    self.running = False
                elif event.key == SDLK_LEFT and self.state == self.LEFT:
                    self.running = False
                elif event.key == SDLK_DOWN and self.state == self.DOWN:
                    self.running = False
                elif event.key == SDLK_UP and self.state == self.UP:
                    self.running = False
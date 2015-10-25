from pico2d import *
import game_framework
import battle_state

class User:
    image = None
    Down, Up, Left, Right = 3, 2, 1, 0

    PIXEL_PER_METER = (8.0 / 1)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3

    def __init__(self):
        self.x, self.y = -1,-1 #npc생성을 방해하지 않기 위한 초기의 x,y값
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.frame = 0
        self.state = self.Down
        self.running = 0
        self.step_cnt = 0
        self.save_state = 0 #(개발용) 0기본 1저장상태 2삭제상태

        self.hp = self.maxhp = 20 #현재체력 / 최대체력
        self.gold=3000 #돈
        self.dice_num=3 #주사위 최대값
        self.suspicion=0 #혐의
        self.place=''

        self.last_tool =0 #지난 범죄 사용 도구
        self.last_type =0 #지난 범죄 피해자 유형
        self.last_place =''
        self.tool_s = "------"
        self.type_s = "------"
        self.place_s = "------"
        if User.image == None:
            User.image = load_image('user.png')

    def get_bb(self):
        return self.x -7,self.y-14,self.x+7, self.y #폭14 높이 14

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

    def update(self,frame_time):
        if self.hp > self.maxhp:
            self.hp=self.maxhp
        if self.maxhp > 99:
            self.maxhp = 99
        if self.gold > 99999:
            self.gold=99999
        if self.suspicion > 100:
            self.suspicion=100

        if self.running == 1:
            self.frame = (self.frame +1) % 3
            if self.state == self.Right:
                self.x += 8
                self.step_cnt +=1
                for npc in self.npc_group:
                    if self.collide(npc) or self.bg.map_matrix[int(self.y / 8)][int(self.x / 8)] != 0:
                        self.x -= 8
                        self.step_cnt -=1
                        break
            elif self.state == self.Left:
                self.x -= 8
                self.step_cnt +=1
                for npc in self.npc_group:
                    if self.collide(npc) or self.bg.map_matrix[int(self.y / 8)][int(self.x / 8)] != 0:
                        self.x += 8
                        self.step_cnt -=1
                        break
            elif self.state == self.Up:
                self.y += 8
                self.x += 8
                self.step_cnt +=1
                for npc in self.npc_group:
                    if self.collide(npc) or self.bg.map_matrix[int(self.y / 8)][int(self.x / 8)] != 0:
                       self.y -= 8
                       self.x -= 8
                       self.step_cnt -=1
                       break
            elif self.state == self.Down:
                self.y -= 8
                self.x -= 8
                self.step_cnt +=1
                for npc in self.npc_group:
                    if self.collide(npc) or self.bg.map_matrix[int(self.y / 8)][int(self.x / 8)] != 0:
                        self.y += 8
                        self.x += 8
                        self.step_cnt -=1
                        break
        else:
            self.frame = 0
        self.x = clamp(0,self.x,self.bg.w)
        self.y = clamp(0,self.y,self.bg.h)

        #플레이어는 어느 구역에 있는가?#
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

        ##############(개발용) 캐릭터가 서 있는 좌표의 배열값을 0 또는 1로 변경#############
        if self.save_state == 1:
            self.bg.map_matrix[int(self.y/8)][int(self.x/8)] = 0
        elif self.save_state == 2:
            self.bg.map_matrix[int(self.y/8)][int(self.x/8)] = 1
        ####################################################################################

    def check_front(self,main_text):
        if self.state == self.Right:
            self.x += 8
            for npc in self.npc_group:
                if self.collide(npc):
                    npc.state = 1
                    main_text.npc =npc
                    self.running =0
            self.x -= 8
        elif self.state == self.Left:
            self.x -= 8
            for npc in self.npc_group:
                if self.collide(npc):
                    npc.state = 0
                    main_text.npc =npc
                    self.running =0
            self.x += 8
        elif self.state == self.Up:
            self.y += 8
            self.x += 8
            for npc in self.npc_group:
                if self.collide(npc):
                    npc.state = 3
                    main_text.npc =npc
                    self.running =0
            self.y -= 8
            self.x -= 8
        elif self.state == self.Down:
            self.y -= 8
            self.x -= 8
            for npc in self.npc_group:
                if self.collide(npc):
                    npc.state = 2
                    main_text.npc =npc
                    self.running =0
            self.y += 8
            self.x += 8

    def set_background(self,bg):
        self.bg=bg

    def set_npcgroup(self,npc_group):
        self.npc_group=npc_group

    def stepbystep(self):
        if self.step_cnt >= 70:
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
                    self.running = 1
                if event.key == SDLK_RIGHT:
                    self.state = self.Right
                elif event.key == SDLK_LEFT:
                    self.state = self.Left
                elif event.key == SDLK_UP:
                    self.state = self.Up
                elif event.key == SDLK_DOWN:
                    self.state = self.Down
                elif event.key == SDLK_z:
                    self.check_front(main_text)
            ###########################(개발용) 좌표 세이브,삭제모드################################
                elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
                    self.save_state = 1
                    print ("세이브 모드")
                elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
                    self.save_state = 2
                    print (" 삭제 모드")
                elif event.type == SDL_KEYDOWN and event.key == SDLK_q:
                    self.save_state = 0
                    print("모드 종료")
                elif event.type == SDL_KEYDOWN and event.key == SDLK_c:
                    print("골드",self.gold,"혐의:",self.suspicion,"지난범죄도구",self.last_tool,"지난피해자:",self.last_type)
            ####################################################################################
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_RIGHT and self.state == self.Right:
                    self.running = 0
                elif event.key == SDLK_LEFT and self.state == self.Left:
                    self.running = 0
                elif event.key == SDLK_DOWN and self.state == self.Down:
                    self.running = 0
                elif event.key == SDLK_UP and self.state == self.Up:
                    self.running = 0
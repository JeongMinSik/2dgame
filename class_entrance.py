from pico2d import *

class Entrance:

    def __init__(self,num,user):
        self.x,self.y =264,232
        self.type = num+100
        self.active_t=0
        self.user=user
        self.hp_price=0
        self.police_price=0
        self.dice_price=0

        if self.type == 100: #병원
            self.x,self.y =264,232
        elif self.type == 101: #피자가게
            self.x,self.y =560,184
        elif self.type == 102: #오락실
            self.x,self.y = 696,184
        elif self.type == 103: #빵집
            self.x,self.y = 976,184
        elif self.type == 104: #경찰서
            self.x,self.y = 1136,224
        elif self.type == 105: #시청
            self.x,self.y = 776,584
        elif self.type == 106: #호텔
            self.x,self.y = 1160,512
        elif self.type == 107: #빈집1
            self.x,self.y = 1256,512
        elif self.type == 108: #빈집2
            self.x,self.y = 1352,544
        elif self.type == 109: #약국
            self.x,self.y = 720,792
        elif self.type == 110: #버거킹
            self.x,self.y = 848,784

    def update(self,main_text):
        if self.collide(self.user):
            self.active_t =self.type
            self.user.running = 0
            main_text.npc=self
            if main_text.step ==0:
                if self.type == 100:
                    main_text.step=1
                    main_text.string1 = "병원                                           "
                    main_text.string2 = "체력이 0이 되면 오는 곳입니다.                               "
                    main_text.string3 = "                                        "
                elif self.type == 101:
                    main_text.string1 = "피자헛                                           "
                    main_text.string2 = "페페로니피자 600원 (Hp 50 회복)                          "
                    main_text.string3 = "구입해 드시겠습니까?                       "
                elif self.type == 102:
                    main_text.step =1
                    main_text.string1 = "오락실                                           "
                    main_text.string2 = "미구현                          "
                    main_text.string3 = "                                          "
                elif self.type == 103:
                    main_text.string1 = "파리바게트                                    "
                    main_text.string2 = "크림빵 100원 (Hp 5 회복)                          "
                    main_text.string3 = "구입해 드시겠습니까?                         "
                elif self.type == 104:
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
                elif self.type == 105:
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
                elif self.type == 106:
                    main_text.string1 = "호텔                                           "
                    main_text.string2 = "현재까지 플레이 상태를 저장합니다.                          "
                    main_text.string3 = "저장하시겠습니까?                         "
                elif self.type == 107:
                    main_text.step=1
                    main_text.string1 = "빈집1                                           "
                    main_text.string2 = "비어있는 집입니다.                          "
                    main_text.string3 = "                                        "
                elif self.type == 108:
                    main_text.step=1
                    main_text.string1 = "빈집2                                           "
                    main_text.string2 = "비어있는 집입니다.                          "
                    main_text.string3 = "                                        "
                elif self.type == 109:
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
                elif self.type == 110:
                    main_text.string1 = "버거킹                                           "
                    main_text.string2 = "불고기버거 300원 (Hp 20 회복)                          "
                    main_text.string3 = "구입해 드시겠습니까?                         "

    def handle_event(self, event, main_text):
        if (self.user.last_place == 'S' and self.active_t >=100 and self.active_t <= 104) or (self.user.last_place == 'W' and self.active_t ==105) or (self.user.last_place == 'E' and self.active_t >=106 and self.active_t <= 108) or (self.user.last_place == 'N' and self.active_t >=109 and self.active_t <= 110):
            main_text.string2 = "이 건물은 최근 범행구역 안에 있으므로                      "
            main_text.string3 = "이용할 수 없습니다.                                            "
        elif self.active_t == 101: #피자가게
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
        elif self.active_t == 103: #빵집
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
        elif self.active_t == 104: #경찰서
            if self.user.gold >=self.police_price and self.user.suspicion != 0:
                self.user.gold -=self.police_price
                self.user.suspicion = 0
                main_text.string2 = "뇌물을 주어 혐의가 0 %가 되었습니다.                      "
                main_text.string3 = "돈 -%4d"%self.police_price+"원                                          "
            elif self.user.gold < self.police_price and self.user.suspicion != 0:
                main_text.string2 = "혐의를 0 %로 만들기엔                      "
                main_text.string3 = "가진 돈이 부족합니다.                                     "
        elif self.active_t == 105: #시청
            if self.user.gold >=self.dice_price and self.user.dice_num != 5:
                self.user.gold -=self.dice_price
                self.user.dice_num += 1
                main_text.string2 = "주사위최댓값이 1 증가했습니다!                      "
                main_text.string3 = "돈 -%4d"%self.dice_price+"원                                          "
            elif self.user.gold < self.dice_price and self.user.dice_num != 5:
                main_text.string2 = "주사위 업그레이드를 하기엔                           "
                main_text.string3 = "가진 돈이 부족합니다.                                     "
        elif self.active_t == 106: #호텔
                main_text.string2 = "미구현                                     "
                main_text.string3 = "                                          "
        elif self.active_t == 109:
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
        elif self.active_t == 110: #버거킹
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
        if self.type == 105:
            return self.x -16,self.y-4,self.x+16, self.y+4
        return self.x -4,self.y-4,self.x+4, self.y+4

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
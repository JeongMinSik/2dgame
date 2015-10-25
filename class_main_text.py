from pico2d import *



class Main_Text:
    box_image=None
    button_image = None
    font = None
    def __init__(self):
        self.yes = 1
        self.npc = None
        self.step = 0
        self.string1 = "이름                                          "
        self.string2 = "\"말\"                                        "
        self.string3 = "강도질을 시도하시겠습니까?                       "
        if Main_Text.box_image == None:
            Main_Text.box_image = load_image('main_text_box.png')
            Main_Text.box_image.opacify(0.9)
        if Main_Text.button_image == None:
            Main_Text.button_image = load_image('button_y_n.png')
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
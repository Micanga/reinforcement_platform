import inspect
import tkinter
from tkinter import *
from pygame import mixer
import random

from Game import Game
from log import *
from math import *
from MyCommons import *
import numpy as np
from utils import *

WHITE = [255.0, 255.0, 255.0]
YELLOW = [255.0, 255.0, 0.0]
BLUE = [0.0, 0.0, 200.0]
GREEN = [0.0, 200.0, 0.0]
RED = [200.0, 0.0, 0.0]
BLACK = [0.0, 0.0, 0.0]
BABY_BLUE = [137.0, 207.0, 240.0]
BG_COLOR = BABY_BLUE

class Screen(Game):

    """
    .####.##....##.####.########
    ..##..###...##..##.....##...
    ..##..####..##..##.....##...
    ..##..##.##.##..##.....##...
    ..##..##..####..##.....##...
    ..##..##...###..##.....##...
    .####.##....##.####....##...
    """
    def __init__(self, master, prev_sc, main_bg, bg_img=None, screen_name=''):
        start_log = "---------------------------------\n" + \
                    "| LOG " + screen_name + "\n" + \
                    "---------------------------------"
        print(start_log)
        super().__init__()

        # 1. setting screen components
        if prev_sc is not None:
            self.destroyAll(prev_sc)

        self.master = master
        self.main_bg = main_bg
        self.prev_sc = prev_sc
        self.sw, self.sh = self.master.winfo_screenwidth(), self.master.winfo_screenheight()

        self.radius = 2*self.sw/3 if self.sw < self.sh else 2*self.sh/3
        self.center_w, self.center_h = self.sw/2, 4*self.sh/5
        self.points = tkinter.StringVar()
        self.points.set(0)

        # 2. initialising screen variables
        self.widgets = []
        self.buttons = []

        # 3. maintaing game main variables
        attributes = [i for i in dir(self.prev_sc) if not inspect.ismethod(i)]

        if 'nickname' in attributes:
            self.nickname = self.prev_sc.nickname
        else:
            self.nickname = None
        if 'start_time' in attributes:
            self.start_time = self.prev_sc.start_time
        else:
            self.start_time = None
        if 'group' in attributes:
            self.group = self.prev_sc.group
        else:
            self.group = None
        if 'stage' in attributes:
            self.stage = self.prev_sc.stage

            if bg_img is not None:
                update_screen(self,BG_COLOR)
                self.main_bg = set_bg(self.master, self.main_bg, bg_img)
            elif self.main_bg is not None:
                self.main_bg.destroy()
                update_screen(self,BG_COLOR)
        else:
            self.stage = None

            if bg_img is not None:
                update_screen(self)
                self.main_bg = set_bg(self.master, self.main_bg, bg_img)
            elif self.main_bg is not None:
                self.main_bg.destroy()
                update_screen(self)

        if 'aco_file' in attributes:
            self.aco_file = self.prev_sc.aco_file
        else:
            self.aco_file = ''

        if 'game' in attributes:
            self.game = self.prev_sc.game
        else:
            self.game = []
        if 'settings' in attributes:
            self.settings = self.prev_sc.settings
        else:
            self.settings = {\
                'actions_per_block':10,\
                'min_blocks':6,\
                'max_blocks':20,\
                'IRT_threshold':0.1,\
                'return_click':0,\
                'choose_aco':True,\
                'fade_flag':True,
            }

    def destroyAll(self, prev_sc):
        clean_log = "| - destroying previous screen"
        print(clean_log)

        # destroying everything from the previous screen
        destroyWidgets(prev_sc.widgets)
        removeButtons(prev_sc.buttons)

    """
    .####.##....##.########.########.########..########....###.....######..########
    ..##..###...##....##....##.......##.....##.##.........##.##...##....##.##......
    ..##..####..##....##....##.......##.....##.##........##...##..##.......##......
    ..##..##.##.##....##....######...########..######...##.....##.##.......######..
    ..##..##..####....##....##.......##...##...##.......#########.##.......##......
    ..##..##...###....##....##.......##....##..##.......##.....##.##....##.##......
    .####.##....##....##....########.##.....##.##.......##.....##..######..########
    """
    def createButtons(self, center_h, center_w, radius):
            # print(self.createb_txt)
        diameter = self.sh/5
        
        self.button_1 = CircularButton(self.master, diameter, diameter,
                                       color=RED, bg=BG_COLOR, command=self.button1_click)
        self.button_1.place(x=center_w-radius,
                            y=center_h,
                            anchor='center')
        self.buttons.append(self.button_1)

        self.button_2 = CircularButton(self.master, diameter, diameter,
                                       color=RED, bg=BG_COLOR, command=self.button2_click)
        self.button_2.place(x=center_w-radius*cos(pi/7),
                            y=center_h-radius*sin(pi/7),
                            anchor='center')
        self.buttons.append(self.button_2)

        self.button_3 = CircularButton(self.master, diameter, diameter,
                                       color=RED, bg=BG_COLOR, command=self.button3_click)
        self.button_3.place(x=center_w-radius*cos(2*pi/7),
                            y=center_h-radius*sin(2*pi/7),
                            anchor='center')
        self.buttons.append(self.button_3)

        self.button_4 = CircularButton(self.master, diameter, diameter,
                                       color=RED, bg=BG_COLOR, command=self.button4_click)
        self.button_4.place(x=center_w-radius*cos(3*pi/7),
                            y=center_h-radius*sin(3*pi/7),
                            anchor='center')
        self.buttons.append(self.button_4)

        self.button_5 = CircularButton(self.master, diameter, diameter,
                                       color=RED, bg=BG_COLOR, command=self.button5_click)
        self.button_5.place(x=center_w-radius*cos(4*pi/7),
                            y=center_h-radius*sin(4*pi/7),
                            anchor='center')
        self.buttons.append(self.button_5)

        self.button_6 = CircularButton(self.master, diameter, diameter,
                                       color=RED, bg=BG_COLOR, command=self.button6_click)
        self.button_6.place(x=center_w-radius*cos(5*pi/7),
                            y=center_h-radius*sin(5*pi/7),
                            anchor='center')
        self.buttons.append(self.button_6)

        self.button_7 = CircularButton(self.master, diameter, diameter,
                                       color=RED, bg=BG_COLOR, command=self.button7_click)
        self.button_7.place(x=center_w-radius*cos(6*pi/7),
                            y=center_h-radius*sin(6*pi/7),
                            anchor='center')
        self.buttons.append(self.button_7)

        self.button_8 = CircularButton(self.master, diameter, diameter,
                                       color=RED, bg=BG_COLOR, command=self.button8_click)
        self.button_8.place(x=center_w-radius*cos(pi),
                            y=center_h-radius*sin(pi),
                            anchor='center')
        self.buttons.append(self.button_8)

    def button1_click(self):
        #print("|--- button 1 click             |")
        self.check_action(1)

    def button2_click(self):
        #print("|--- button 2 click             |")
        self.check_action(2)

    def button3_click(self):
        #print("|--- button 3 click             |")
        self.check_action(3)

    def button4_click(self):
        #print("|--- button 4 click             |")
        self.check_action(4)

    def button5_click(self):
        #print("|--- button 5 click             |")
        self.check_action(5)

    def button6_click(self):
        #print("|--- button 6 click             |")
        self.check_action(6)

    def button7_click(self):
        #print("|--- button 7 click             |")
        self.check_action(7)

    def button8_click(self):
        #print("|--- button 8 click             |")
        self.check_action(8)

    def createPointCounter(self):
        self.points = tkinter.StringVar()

        if hasattr(self, 'prev_sc'):
            self.points = self.prev_sc.points
        else:
            self.points.set(0)

        self.points_label = tkinter.Label(self.master, textvariable=self.points, width=3,
                                          bg='white', fg='black',
                                          font=Font(family='Helvetica',
                                                    size=30, weight='bold'),
                                          padx=20, pady=20, bd=4, highlightbackground='black',
                                          highlightthickness=2, relief="solid")

        # points label
        self.points_label.place(
            x=self.center_w, y=self.center_h, anchor='center')
        self.widgets.append(self.points_label)

    def createReturnButton(self, center_h, center_w):
        self.return_button = CircularButton(self.master, 150, 150,
                                       color=YELLOW, bg=BG_COLOR, command=self.return_button_click)
        self.return_button.place(x=center_w,
                            y=center_h,
                            anchor='center')

    def return_button_click(self):
        # - creating the buttons and enabling the mouse
        self.createButtons(self.center_h, self.center_w, self.radius)
        self.return_button.destroy()

    """
    ..........................................................
    ..######...######..########..########.########.##....##...
    .##....##.##....##.##.....##.##.......##.......###...##...
    .##.......##.......##.....##.##.......##.......####..##...
    ..######..##.......########..######...######...##.##.##...
    .......##.##.......##...##...##.......##.......##..####...
    .##....##.##....##.##....##..##.......##.......##...###...
    ..######...######..##.....##.########.########.##....##...
    ..........................................................
    ..######..##.....##....###....##....##..######...########.
    .##....##.##.....##...##.##...###...##.##....##..##.......
    .##.......##.....##..##...##..####..##.##........##.......
    .##.......#########.##.....##.##.##.##.##...####.######...
    .##.......##.....##.#########.##..####.##....##..##.......
    .##....##.##.....##.##.....##.##...###.##....##..##.......
    ..######..##.....##.##.....##.##....##..######...########.
    ..........................................................
    """
    def stageFade(self):
        # a. calculating the color fade
        self.cur_color -= (0.015*self.ref_color)
        self.text_cur_color -= (0.015*self.text_ref_color)

        # b. checking the fade stop
        if (int(self.cur_color[0]) >= 0 and int(self.cur_color[1]) >= 0 and int(self.cur_color[2]) >= 0\
            and int(self.cur_color[0]) < 255 and int(self.cur_color[1]) < 255 and int(self.cur_color[2]) < 255):
            self.main_bg.configure(bg="#%02x%02x%02x" %
                               (int(self.cur_color[0]), int(self.cur_color[1]), int(self.cur_color[2])))
            self.stage_txt.configure(
                bg="#%02x%02x%02x" % (int(self.cur_color[0]), int(self.cur_color[1]), int(self.cur_color[2])),
                fg="#%02x%02x%02x" % (int(self.text_cur_color[0]), int(self.text_cur_color[1]), int(self.text_cur_color[2])))
            self.master.after(50, self.stageFade)
        else:
            if self.stage == 1:
                self.goToStage1(fade=False)
            if self.stage == 2:
                self.goToStage2(fade=False)
            if self.stage == 3:
                self.goToStage3(fade=False)
            if self.stage == 4:
                self.goToStage4(fade=False)
            if self.stage == 5:
                self.goToStage5(fade=False)
            if self.stage == 6:
                self.goToStage6(fade=False)

    def goToStage1(self,fade=True):
        if fade and self.settings['fade_flag']:
            removeButtons(self.buttons)
            destroyWidgets(self.widgets)
            self.cur_color = BG_COLOR
            self.ref_color = self.cur_color - np.array(random.sample([YELLOW,RED,BLUE],1)[0])
            self.text_cur_color = BG_COLOR
            self.text_ref_color = self.cur_color - np.array(BLACK)

            self.stage_txt = tkinter.Label(self.master,\
                bg= "#%02x%02x%02x" % (int(self.cur_color[0]), int(self.cur_color[1]), int(self.cur_color[2])),\
                fg = "#%02x%02x%02x" % (int(self.text_cur_color[0]), int(self.text_cur_color[1]), int(self.text_cur_color[2])),\
                text='FASE 1', font=Font(family='Helvetica', size=96, weight='bold'))
            self.stage_txt.place(x=self.sw/2,y=self.sh/2,anchor='center')

            self.stageFade()
        else:
            txt = "| Going to Stage 1 Screen"
            print(txt)
            from Stage1 import Stage1
            Stage1(self.master, self, self.main_bg)

    def goToStage2(self,fade=True):
        if fade and self.settings['fade_flag']:
            removeButtons(self.buttons)
            destroyWidgets(self.widgets)
            self.cur_color = BG_COLOR
            self.ref_color = self.cur_color - np.array(random.sample([YELLOW,RED,BLUE],1)[0])
            self.text_cur_color = BG_COLOR
            self.text_ref_color = self.cur_color - np.array(BLACK)

            self.stage_txt = tkinter.Label(self.master,\
                bg= "#%02x%02x%02x" % (int(self.cur_color[0]), int(self.cur_color[1]), int(self.cur_color[2])),\
                fg = "#%02x%02x%02x" % (int(self.text_cur_color[0]), int(self.text_cur_color[1]), int(self.text_cur_color[2])),\
                text='FASE 2', font=Font(family='Helvetica', size=96, weight='bold'))
            self.stage_txt.place(x=self.sw/2,y=self.sh/2,anchor='center')

            self.stageFade()
        else:
            txt = "| Going to Stage 2 Screen"
            print(txt)
            from Stage2 import Stage2
            Stage2(self.master, self, self.main_bg)

    def goToStage3(self,fade=True):
        if fade and self.settings['fade_flag']:
            removeButtons(self.buttons)
            destroyWidgets(self.widgets)
            self.cur_color = BG_COLOR
            self.ref_color = self.cur_color - np.array(random.sample([YELLOW,RED,BLUE],1)[0])
            self.text_cur_color = BG_COLOR
            self.text_ref_color = self.cur_color - np.array(BLACK)

            self.stage_txt = tkinter.Label(self.master,\
                bg= "#%02x%02x%02x" % (int(self.cur_color[0]), int(self.cur_color[1]), int(self.cur_color[2])),\
                fg = "#%02x%02x%02x" % (int(self.text_cur_color[0]), int(self.text_cur_color[1]), int(self.text_cur_color[2])),\
                text='FASE 3', font=Font(family='Helvetica', size=96, weight='bold'))
            self.stage_txt.place(x=self.sw/2,y=self.sh/2,anchor='center')

            self.stageFade()
        else:
            txt = "| Going to Stage 3 Screen"
            print(txt)
            from Stage3 import Stage3
            Stage3(self.master, self, self.main_bg)

    def goToStage4(self,fade=True):
        if fade and self.settings['fade_flag']:
            removeButtons(self.buttons)
            destroyWidgets(self.widgets)
            self.cur_color = BG_COLOR
            self.ref_color = self.cur_color - np.array(random.sample([YELLOW,RED,BLUE],1)[0])
            self.text_cur_color = BG_COLOR
            self.text_ref_color = self.cur_color - np.array(BLACK)

            self.stage_txt = tkinter.Label(self.master,\
                bg= "#%02x%02x%02x" % (int(self.cur_color[0]), int(self.cur_color[1]), int(self.cur_color[2])),\
                fg = "#%02x%02x%02x" % (int(self.text_cur_color[0]), int(self.text_cur_color[1]), int(self.text_cur_color[2])),\
                text='FASE 1', font=Font(family='Helvetica', size=96, weight='bold'))
            self.stage_txt.place(x=self.sw/2,y=self.sh/2,anchor='center')

            self.stageFade()
        else:
            txt = "| Going to Stage 4 Screen"
            print(txt)
            from Stage4 import Stage4
            Stage4(self.master, self, self.main_bg)

    def goToStage5(self,fade=True):
        if fade and self.settings['fade_flag']:
            removeButtons(self.buttons)
            destroyWidgets(self.widgets)
            self.cur_color = BG_COLOR
            self.ref_color = self.cur_color - np.array(random.sample([YELLOW,RED,BLUE],1)[0])
            self.text_cur_color = BG_COLOR
            self.text_ref_color = self.cur_color - np.array(BLACK)

            self.stage_txt = tkinter.Label(self.master,\
                bg= "#%02x%02x%02x" % (int(self.cur_color[0]), int(self.cur_color[1]), int(self.cur_color[2])),\
                fg = "#%02x%02x%02x" % (int(self.text_cur_color[0]), int(self.text_cur_color[1]), int(self.text_cur_color[2])),\
                text='FASE 2', font=Font(family='Helvetica', size=96, weight='bold'))
            self.stage_txt.place(x=self.sw/2,y=self.sh/2,anchor='center')

            self.stageFade()
        else:
            txt = "| Going to Stage 5 Screen"
            print(txt)
            from Stage5 import Stage5
            Stage5(self.master, self, self.main_bg)

    def goToStage6(self,fade=True):
        if fade and self.settings['fade_flag']:
            removeButtons(self.buttons)
            destroyWidgets(self.widgets)
            self.cur_color = BG_COLOR
            self.ref_color = self.cur_color - np.array(random.sample([YELLOW,RED,BLUE],1)[0])
            self.text_cur_color = BG_COLOR
            self.text_ref_color = self.cur_color - np.array(BLACK)

            self.stage_txt = tkinter.Label(self.master,\
                bg= "#%02x%02x%02x" % (int(self.cur_color[0]), int(self.cur_color[1]), int(self.cur_color[2])),\
                fg = "#%02x%02x%02x" % (int(self.text_cur_color[0]), int(self.text_cur_color[1]), int(self.text_cur_color[2])),\
                text='FASE 3', font=Font(family='Helvetica', size=96, weight='bold'))
            self.stage_txt.place(x=self.sw/2,y=self.sh/2,anchor='center')

            self.stageFade()
        else:
            txt = "| Going to Stage 6 Screen"
            print(txt)
            from Stage6 import Stage6
            Stage6(self.master, self, self.main_bg)

    def goToNickName(self):
        txt = "| Going to Nickname Screen"
        print(txt)

        from NickName import NickName
        NickName(self.master, self, self.main_bg)

    def goToSettings(self):
        txt = "| Going to Settings Screen"
        print(txt)

        from Settings import Settings
        Settings(self.master, self, self.main_bg)

    def goToMenu(self):
        txt = "| Going to Menu Screen"
        print(txt)

        from Menu import Menu
        Menu(self.master, self, self.main_bg)

    def goToExit(self):
        self.master.destroy()

        exit_log = "| Exit Button Pressed"
        print(exit_log)

    def averageIRT(self):
        # verifying if the number of blocks is sufficient to calculate the averageIRT
        if self.settings['min_blocks'] < 6:
            return 1.0

        # calculating irt
        # a. getting the mean time per block
        irt_per_block = []

        for i in range( len(self.game)-self.settings['min_blocks'], len(self.game)):
            irt_per_block.append(np.sum(self.game[i]['time2answer']))
            irt_per_block[-1] = (irt_per_block[-1].total_seconds())/10

        # b. calculating (for real)

        print("This is our IRT per Block")
        print(irt_per_block)
        R = (irt_per_block[0] + irt_per_block[1] + irt_per_block[2])/3 - \
                (irt_per_block[3] + irt_per_block[4] + irt_per_block[5])/3
        
        R /= (np.sum(irt_per_block)/6)

        print("This is our IRT")
        print(R)

        # returning the result
        return np.abs(R)

import inspect
import tkinter
from tkinter import *
from pygame import mixer

from log import *
from math import *
from MyCommons import *
import numpy as np
from utils import *

WHITE = [255.0, 255.0, 255.0]
GREEN = [0.0, 200.0, 0.0]
RED = [255.0, 0.0, 0.0]
BLACK = [0.0, 0.0, 0.0]
BABY_BLUE = [137.0, 207.0, 240.0]
BG_COLOR = BABY_BLUE


class Screen:

    def __init__(self, master, prev_sc, main_bg, bg_img=None):
        start = "---------------------------------\n" + \
                "| New Screen                     |\n" + \
                "---------------------------------"
        print(start)

        # a. setting screen components
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

        # c. initialising screen variables
        self.widgets = []
        self.buttons = []

        # d. maintaing game main variables
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

        if 'game' in attributes:
            self.game = self.prev_sc.game
        else:
            self.game = None
        if 'settings' in attributes:
            self.settings = self.prev_sc.settings
        else:
            self.settings = {\
                'actions_per_block':10,\
                'min_blocks':6,\
                'max_blocks':20,\
                'IRT_threshold':0.1
            }

        print('| Settings')
        print(self.settings)

    def destroyAll(self, prev_sc):
        clean_log = "| Cleaning Last Screen           |"
        print(clean_log)

        # destroying everything from the previous screen
        destroyWidgets(prev_sc.widgets)
        removeButtons(prev_sc.buttons)

    # Starting a game Screen
    def createButtons(self, center_h, center_w, radius):
            # print(self.createb_txt)
        self.button_1 = CircularButton(self.master, 100, 100,
                                       color=RED, bg=BG_COLOR, command=self.button1_click)
        self.button_1.place(x=center_w-radius,
                            y=center_h,
                            anchor='center')
        self.buttons.append(self.button_1)

        self.button_2 = CircularButton(self.master, 100, 100,
                                       color=RED, bg=BG_COLOR, command=self.button2_click)
        self.button_2.place(x=center_w-radius*cos(pi/7),
                            y=center_h-radius*sin(pi/7),
                            anchor='center')
        self.buttons.append(self.button_2)

        self.button_3 = CircularButton(self.master, 100, 100,
                                       color=RED, bg=BG_COLOR, command=self.button3_click)
        self.button_3.place(x=center_w-radius*cos(2*pi/7),
                            y=center_h-radius*sin(2*pi/7),
                            anchor='center')
        self.buttons.append(self.button_3)

        self.button_4 = CircularButton(self.master, 100, 100,
                                       color=RED, bg=BG_COLOR, command=self.button4_click)
        self.button_4.place(x=center_w-radius*cos(3*pi/7),
                            y=center_h-radius*sin(3*pi/7),
                            anchor='center')
        self.buttons.append(self.button_4)

        self.button_5 = CircularButton(self.master, 100, 100,
                                       color=RED, bg=BG_COLOR, command=self.button5_click)
        self.button_5.place(x=center_w-radius*cos(4*pi/7),
                            y=center_h-radius*sin(4*pi/7),
                            anchor='center')
        self.buttons.append(self.button_5)

        self.button_6 = CircularButton(self.master, 100, 100,
                                       color=RED, bg=BG_COLOR, command=self.button6_click)
        self.button_6.place(x=center_w-radius*cos(5*pi/7),
                            y=center_h-radius*sin(5*pi/7),
                            anchor='center')
        self.buttons.append(self.button_6)

        self.button_7 = CircularButton(self.master, 100, 100,
                                       color=RED, bg=BG_COLOR, command=self.button7_click)
        self.button_7.place(x=center_w-radius*cos(6*pi/7),
                            y=center_h-radius*sin(6*pi/7),
                            anchor='center')
        self.buttons.append(self.button_7)

        self.button_8 = CircularButton(self.master, 100, 100,
                                       color=RED, bg=BG_COLOR, command=self.button8_click)
        self.button_8.place(x=center_w-radius*cos(pi),
                            y=center_h-radius*sin(pi),
                            anchor='center')
        self.buttons.append(self.button_8)

    def createPointCounter(self):
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
        
    def load_sfx(self,sfx_path='local/default/sfx.wav'):
        mixer.init()
        mixer.music.load(sfx_path)

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

    def check_action(self, clicked_button):
        # a. updating game log
        self.game[-1]['answer'].append(clicked_button)
        
        self.game[-1]['time2answer'].append(
            datetime.datetime.now() - self.round_start_time)
        self.game[-1]['frequency'][clicked_button] += 1

        # b.reinforcing the action
        if self.conditionalReinforce():
            removeButtons(self.buttons)
            self.game[-1]['reinforced'].append(True)
            self.cur_color = np.array(BG_COLOR)
            self.ref_color = np.array(BG_COLOR) - np.array(GREEN)

            mixer.music.play() 
            self.positive_reinforce_action()
            
        else:
            removeButtons(self.buttons)
            self.game[-1]['reinforced'].append(False)
            self.cur_color = np.array(BG_COLOR)
            self.ref_color = np.array(BG_COLOR) - np.array(BLACK)
            self.negative_reinforce_action()
            #print(sum(self.game['frequency'].values()))

    def conditionalReinforce(self):
        #print("This is the standard conditionalReforce")
        return True

    def number_of_blocks(self):
        block_counter = 0

        # NOTE: the first game in the array is the
        # initial one, so we don't count it
        for i in range(1,len(self.game)):
            if self.game[i]['group'] == self.group\
            and self.game[i]['stage'] == self.stage:
             block_counter += 1

        return block_counter

    def number_of_rounds(self):
        round_counter = \
            len(self.game[-1]['group'])
        return round_counter

    def positive_reinforce_action(self):
        # a. calculating the color fade (to green)
        self.cur_color -= (0.1*self.ref_color)

        # b. changing background color
        self.main_bg.configure(bg="#%02x%02x%02x" %
                               (int(self.cur_color[0]), int(self.cur_color[1]), int(self.cur_color[2])))

        # c. checking the fade stop
        if (self.ref_color[1] >= 0 and int(self.cur_color[1]) > 200)\
                or (self.ref_color[1] < 0 and int(self.cur_color[1]) < 200):
            self.master.after(50, self.positive_reinforce_action)
        else:
            # - setting green bg
            self.main_bg.configure(bg="#%02x%02x%02x" % (0, 200, 0))
            # self.points.set(int(self.points.get())+int(self.settings['points']))
            # self.master.after(int(float(self.settings['iti'])*1000),self.replay)
            self.points.set(int(self.points.get())+10)
            self.master.after(1*1000, self.replay)

    def negative_reinforce_action(self):
        # a. calculating the color fade (to green)
        self.cur_color -= (0.1*self.ref_color)

        # b. changing background color
        self.main_bg.configure(bg="#%02x%02x%02x" %
                               (int(self.cur_color[0]), int(self.cur_color[1]), int(self.cur_color[2])))

        # c. checking the fade stop
        if (self.ref_color[1] >= 0 and int(self.cur_color[1]) > 0)\
                or (self.ref_color[1] < 0 and int(self.cur_color[1]) < 0):
            self.master.after(50, self.negative_reinforce_action)
        else:
            # - setting green bg
            self.main_bg.configure(bg="#%02x%02x%02x" % (0, 0, 0))
            # self.points.set(int(self.points.get())+int(self.settings['points']))
            # self.master.after(int(float(self.settings['iti'])*1000),self.replay)
            self.master.after(1*1000, self.replay)

    def averageIRT(self):

        time2answerReinforced = [i for i, val in enumerate(self.game[-1]['reinforced']) if (val == True)] 
        #time2answerReinforced = self.game[-1]['time2answer'][time2answerReinforced]

        print("!time2answer")
        print(time2answerReinforced)
        
       
    def auto_play(self):
        coin = float(random.uniform(0,8))
        if coin <= 1:
            self.button1_click()
        elif coin <= 2:
            self.button2_click()
        elif coin <= 3:
            self.button3_click()
        elif coin <= 4:
            self.button4_click()
        elif coin <= 5:
            self.button5_click()
        elif coin <= 6:
            self.button6_click()
        elif coin <= 7:
            self.button7_click()
        else:
            self.button8_click()

    def replay(self):
        # 1. Checking replay conditions
        # a. checking the end of the block (10 actions)
        if self.number_of_rounds() == self.settings['actions_per_block']:
            self.game[-1]['block_time'] = (datetime.datetime.now() - self.block_start_time)
            write_result(self.game,self.nickname,self.start_time)

            self.block_start_time = datetime.datetime.now()
            self.update_variables()
        # b. or not end of the block
        else:
            # - writing results in log file
            write_round(self.game,self.nickname,self.start_time)

        # 2. Checking the stop coditions
        # a. maximum blocks
        if number_of_blocks() == self.settings['max_blocks']:
            # IMPLEMENT THE TIMEOUT

        # b. end stage
        elif self.check_stage_end_conditions():
            self.rgb = np.array([0.0,200.0,0.0])
            self.win_txt = tkinter.Label(self.master, bg= "#%02x%02x%02x" % (0, 200, 0), fg = "#%02x%02x%02x" % (0, 200, 0),\
                 text='ATÉ O MOMENTO VOCÊ ACUMULOU '+str(int(self.points.get())+int(self.prev_sc.points.get()))+\
                 ' PONTOS!', font=Font(family='Helvetica', size=16, weight='bold'))
            self.master.after(20,self.fadeResetText)
        # c. keep playing
        else:
            # - setting the round start variable
            self.round_start_time = datetime.datetime.now()
            self.main_bg.configure(bg="#%02x%02x%02x" %\
                (int(BG_COLOR[0]),int(BG_COLOR[1]),int(BG_COLOR[2])))

            # - creating the buttons and enabling the mouse
            self.createButtons(self.center_h, self.center_w, self.radius)
            reset_mouse_position(self)
            ableMouse(self)

        if self.AUTO:
            self.auto_play()

    def update_variables(self):
        # a. screen var
        self.game.append({})

        self.game[-1]['group'] = self.group
        self.game[-1]['stage'] = self.stage

        # b. round var
        self.game[-1]['answer'] = []
        self.game[-1]['time2answer'] = []
        self.game[-1]['reinforced'] = []
        self.game[-1]['frequency'] = self.game[-2]['frequency']
        self.round_start_time = datetime.datetime.now()

        self.game[-1]['points'] = self.game[-2]['points']

        # c. block var
        self.game[-1]['block_time'] = 0
        self.block_start_time = datetime.datetime.now()

    # Going to another Screen
    def check_stage_conditions(self):
	    return False

    def goToStage1(self):
        txt = "| Going to Stage 1 Screen        |"
        print(txt)

        # Nickname Screen
        from Stage1 import Stage1
        Stage1(self.master, self, self.main_bg)

    def goToStage2(self):
        txt = "| Going to Stage 2 Screen        |"
        print(txt)

        # Nickname Screen
        from Stage2 import Stage2
        Stage2(self.master, self, self.main_bg)

    def goToNickName(self):
        txt = "| Going to Nickname Screen       |"
        print(txt)

        # Nickname Screen
        from NickName import NickName
        NickName(self.master, self, self.main_bg)

    def goToSettings(self):
        txt = "| Going to Settings Screen      |"
        print(txt)

        from Settings import Settings
        Settings(self.master, self, self.main_bg)

    def goToMenu(self):
        txt = "| Going to Menu Screen           |"
        print(txt)

        from Menu import Menu
        Menu(self.master, self, self.main_bg)

    def goToExit(self):
        self.master.destroy()

        exit_log = "| Exit Button Pressed            |"
        print(exit_log)

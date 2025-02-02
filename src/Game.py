import inspect
import tkinter
from tkinter import *
from pygame import mixer

from log import *
from math import *
from MyCommons import *
import numpy as np
import random as rd
from time import sleep
from utils import *

WHITE = [255.0, 255.0, 255.0]
GREEN = [0.0, 200.0, 0.0]
RED = [255.0, 0.0, 0.0]
BLACK = [0.0, 0.0, 0.0]
BABY_BLUE = [137.0, 207.0, 240.0]
BG_COLOR = BABY_BLUE

class Game(object):

    def __init__(self):
        self.test = False
        self.fixed_file = False
        """if self.test and self.fixed_file:
            self.sleep_time = []
            self.sleep_index = 0
            self.click_time_file = '28MARCOteste1_G1_F3_28-03-2021_13h22m19s.csv'
            with open("./results/"+self.click_time_file) as ref_file:
                counter = 0
                for line in ref_file:
                    if counter != 0:
                        self.sleep_time.append(float(line.split(';')[6])) 
                        if counter != 1:
                            self.sleep_time[-1] -= 1.59
                    counter += 1"""

    def auto_play(self):
        ####
        # FOR TEST
        ####
        """if self.test and self.fixed_file:
            print(self.sleep_time[self.sleep_index])
            sleep(self.sleep_time[self.sleep_index])
            self.sleep_index += 1
        else:
            sleep(rd.randrange(1,2))"""

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

    def number_of_blocks(self):
        block_counter = 0

        for i in range(len(self.game)):
            if self.game[i]['group'] == self.group\
            and self.game[i]['stage'] == self.stage:
             block_counter += 1

        return block_counter

    def number_of_rounds(self):
        round_counter = \
            len(self.game[-1]['reinforced'])
        return round_counter
        
    def load_sfx(self,sfx_path='local/default/sfx.wav'):
        if not self.test:
            mixer.init()
            mixer.music.load(sfx_path)

    def check_action(self, clicked_button):
        # a. updating game log
        self.game[-1]['answer'].append(clicked_button)
        self.game[-1]['frequency'][clicked_button] +=1
        self.game[-1]['time2answer'].append(
            datetime.datetime.now() - self.round_start_time)
        self.round_start_time = datetime.datetime.now()

        # b.reinforcing the action
        if self.conditionalReinforce():
            self.gif = AnimatedGIF(self.master, './local/default/coin-flip.gif',False)
            self.gif.place(x=self.sw/2,y=self.sh/2,anchor='center')
            
            removeButtons(self.buttons)
            self.game[-1]['reinforced'].append(True)
            self.cur_color = np.array(BG_COLOR)
            self.ref_color = np.array(BG_COLOR) - np.array(GREEN)

            if not self.test:
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
        return True

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
            self.points.set(int(self.points.get())+1)
            self.master.after(1*1000, self.replay)

    def negative_reinforce_action(self):
        # a. calculating the color fade (to black)
        self.cur_color -= (0.1*self.ref_color)

        # b. changing background color
        self.main_bg.configure(bg="#%02x%02x%02x" %
                               (int(self.cur_color[0]), int(self.cur_color[1]), int(self.cur_color[2])))

        # c. checking the fade stop
        if (self.ref_color[1] >= 0 and int(self.cur_color[1]) > 0)\
                or (self.ref_color[1] < 0 and int(self.cur_color[1]) < 0):
            self.master.after(50, self.negative_reinforce_action)
        else:
            # - setting black bg
            self.main_bg.configure(bg="#%02x%02x%02x" % (0, 0, 0))
            # self.points.set(int(self.points.get())+int(self.settings['points']))
            # self.master.after(int(float(self.settings['iti'])*1000),self.replay)
            self.master.after(1*1000, self.replay)

    def replay(self):
        #could be that we are destroyng the gif without any reinforce hihi
        if hasattr(self, 'gif'):
            self.gif.destroy()
        # 1. Writting results
        # - writing results in log file
        write_round(self.game,self.nickname,self.group,self.stage,self.start_time)

        # 2. Checking the stop coditions
        # a. maximum blocks allowed (Fail)
        stage3or6_check = ((self.stage == 3 or self.stage == 6) and
            (self.number_of_blocks() == self.blocksS3 and self.number_of_rounds() == self.settings['actions_per_block']))
        otherStages_check = ((self.stage != 3 and self.stage != 6) and 
            (self.number_of_blocks() == self.settings['max_blocks'] and self.number_of_rounds() == self.settings['actions_per_block']))

        if stage3or6_check or otherStages_check:
            self.master.after(20,self.nextStage)
            #myFailPopUp(self,'Fim da Fase '+str(self.stage)+'!\n'+\
                #'Você será encaminhado para a próxima fase.')
        # b. keep playing
        else:
            # - end of the block
            if self.number_of_rounds() == self.settings['actions_per_block']:
                # - end game
                if self.check_stage_end_conditions() == True:
                    print("| END STAGE")
                    if self.game[-1]['reinforced'][-1]:
                        self.cur_color = np.array([0.0,200.0,0.0])
                        self.ref_color = self.cur_color - np.array(BLACK)
                    else:
                        self.cur_color = np.array([0.0,0.0,0.0])
                        self.ref_color = self.cur_color - np.array(WHITE)

                    self.master.after(20,self.nextStage)

                    if(self.stage == 3 or self.stage == 6):
                        self.win_txt = tkinter.Label(self.master,\
                            bg= "#%02x%02x%02x" % (int(self.cur_color[0]), int(self.cur_color[1]), int(self.cur_color[2])),\
                            fg = "#%02x%02x%02x" % (int(self.cur_color[0]), int(self.cur_color[1]), int(self.cur_color[2])),\
                            text='ATÉ O MOMENTO VOCÊ ACUMULOU '+str(int(self.points.get())+int(self.prev_sc.points.get()))+\
                            ' PONTOS!', font=Font(family='Helvetica', size=16, weight='bold'))
                        self.win_txt.place(x=self.sw/2,y=self.sh/2,anchor='center')
                   
                else:
                    self.add_block()

                    # - recovering std background    
                    self.main_bg.configure(bg="#%02x%02x%02x" %\
                        (int(BG_COLOR[0]),int(BG_COLOR[1]),int(BG_COLOR[2])))

                    # - replaying
                    # reseting the mouse
                    if self.settings['return_click']:
                        reset_mouse_position(self)

                    # creating the components
                    self.createButtons(self.center_h, self.center_w, self.radius)
                    ableMouse(self)

                    if self.test:
                        self.auto_play()
            # - updating round
            else:
                # - recovering std background    
                self.main_bg.configure(bg="#%02x%02x%02x" %\
                    (int(BG_COLOR[0]),int(BG_COLOR[1]),int(BG_COLOR[2])))

                # - replaying
                if self.settings['return_click']:
                    reset_mouse_position(self)

                # - creating the buttons and enabling the mouse
                self.createButtons(self.center_h, self.center_w, self.radius)
                ableMouse(self)
                if self.test:
                    self.auto_play()

    def fadeNextStage(self):
        print("Fading")
        if(self.stage == 3 or self.stage == 6):
                    self.win_txt.configure(fg="#%02x%02x%02x" %
                                (0,0,0))
                    
        self.points.set(int(self.points.get()) +int(self.prev_sc.points.get()))
        self.master.after(3000,self.nextStage)

    def return_click(self):
        ableMouse(self)
        self.createReturnButton(self.center_h, self.center_w)

    def init_variables(self):
        self.game.append({})

        self.game[-1]['group'] = self.group
        self.game[-1]['stage'] = self.stage

        self.game[-1]['answer'] = []
        self.game[-1]['time2answer'] = []
        self.game[-1]['reinforced'] = []
        self.game[-1]['frequency'] = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0}

      
        if hasattr(self, 'prev_sc'):
            self.game[-1]['points'] = int(self.prev_sc.points.get())
        else:
            self.game[-1]['points'] = 0
            
        self.game[-1]['block_time'] = 0

        self.round_start_time = datetime.datetime.now()
        self.block_start_time = datetime.datetime.now()

    def add_block(self):
        self.game.append({})

        self.game[-1]['group'] = self.group
        self.game[-1]['stage'] = self.stage

        self.game[-1]['answer'] = []
        self.game[-1]['time2answer'] = []
        self.game[-1]['reinforced'] = []
        self.game[-1]['frequency'] = self.game[-2]['frequency']
        
        self.game[-1]['points'] = self.game[-2]['points']
        self.game[-1]['block_time'] = 0

        self.block_start_time = self.round_start_time

    #get All blocks from the group and stage specified    

    def getAllBlocks(self,group,stage):

        blocks = []
        
        for i in range(len(self.game)):
            if self.game[i]['group'] == group and self.game[i]['stage'] == stage:
                blocks.append(i)

        return blocks
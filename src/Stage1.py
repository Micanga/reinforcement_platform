# Interface Imports
import tkinter
from tkinter import *
from tkinter import font
from tkinter import LEFT, RIGHT, BOTTOM, TOP, NONE
from tkinter import messagebox, filedialog, StringVar
from tkinter.font import Font

# Utils Imports
from copy import deepcopy
import datetime
from math import *
import numpy as np
import os
import random
import time

from pygame import mixer
#import winsound

import log
from MyCommons import *
from Screen import Screen
import utils

AUTO = False

WHITE = [255.0,255.0,255.0]
GREEN = [0.0,200.0,0.0]
RED = [255.0,0.0,0.0]
BABY_BLUE = [137.0,207.0,240.0]

BG_COLOR = BABY_BLUE

AUTO = True

class Stage1(Screen):

	def __init__(self, master, prev_sc, main_bg):
		# 1. Initializing the necessary variables
		# a. initializing the screen
		super().__init__(master, prev_sc, main_bg)
		self.update_variables(prev_sc)

		# b. log text
		self.start_log = 		"---------------------------------\n" + \
								"| LOG STAGE 1 PLAY SCREEN       |\n" + \
								"---------------------------------"
		self.createb_txt =		"|--- creating buttons           |"
		self.timeout_txt = 		"| Time Out                      |"
		self.finish_txt = 		"| Stage Finished                |"
		print(self.start_log)

		# 2. Setting the screen buttons and widgets
		# a. buttons
		self.radius = 2*self.sw/3 if self.sw < self.sh else 2*self.sh/3
		self.center_w, self.center_h = self.sw/2, 4*self.sh/5
		self.createButtons(self.center_h, self.center_w, self.radius)
		utils.ableButtonsAndMouse(self)

		# b. points counter
		self.createPointCounter()

		# c. sound effects
		self.load_sfx()

		# d. auto-play
		if AUTO:
			self.auto_play()

	def auto_play(self):
		coin = int(random.uniform(0,8))
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

	def update_variables(self,prev_sc):
		# a. screen var
		self.points = tkinter.StringVar()
		self.points.set(0)

		self.game = []
		self.game.append({})

		self.game[-1]['group'] = prev_sc.group
		self.game[-1]['stage'] = 1

		# b. round var
		self.game[-1]['answer'] = []
		self.game[-1]['time2answer'] = []
		self.game[-1]['reinforced'] = []
		self.game[-1]['frequency'] = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0}
		self.round_start_time = datetime.datetime.now()

		self.game[-1]['points'] = 0

		# c. block var
		self.game[-1]['block_time'] = 0
		self.block_start_time = datetime.datetime.now()

	# THE GAME METHODS
	def check_action(self,clicked_button):
		# a. updating game log
		self.game[-1]['answer'].append(clicked_button)
		self.game[-1]['reinforced'].append(True)
		self.game[-1]['time2answer'].append(datetime.datetime.now() - self.round_start_time)
		self.game[-1]['frequency'][clicked_button] += 1

		# b.reinforcing the action
		# - removing buttons and disabling the mouse
		utils.removeButtons(self.buttons)
		utils.disableMouse(self)

		# - checking if the action was reinforced
		self.cur_color = np.array(BG_COLOR)
		self.ref_color = np.array(BG_COLOR) - np.array(GREEN)

		mixer.music.play() 
		self.positive_reinforce_action()

	def replay(self):
		# 1. Writing results in log file
		log.write_round(self.game,self.nickname,self.start_time)

		# 2. Checking replay conditions
		# a. checking the end of the block (8 actions)
		if len(self.game[-1]['reinforced']) == 8:
			print("|--- starting new block         |")
			self.game[-1]['block_time'].append(datetime.datetime.now() - self.block_start_time)
			self.block_start_time = datetime.datetime.now()
			self.game.append({})

		# b. end stage
		if self.check_stage_end_conditions():
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
			utils.reset_mouse_position(self)
			utils.ableMouse(self)

		if AUTO:
			self.auto_play()

	def check_stage_end_conditions(self):
		# if the number of blocks is greather than 16, finish the stage
		if len(self.game) > 16:
			return True
		# else keep playing
		return False

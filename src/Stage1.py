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

from MyCommons import *
import utils

AUTO = False

WHITE = [255.0,255.0,255.0]
GREEN = [0.0,200.0,0.0]
RED = [255.0,0.0,0.0]
BABY_BLUE = [137.0,207.0,240.0]

BG_COLOR = BABY_BLUE

class Stage1:

	def __init__(self, master, prev_sc, main_bg):
		# 1. Initializing the necessary variables
		# a. screen and log components
		self.master = master
		self.main_bg = main_bg
		self.update_variables(prev_sc)
		utils.update_screen(self,BG_COLOR)
		self.sw, self.sh = master.winfo_screenwidth(), master.winfo_screenheight()

		# b. log text
		self.start_log = 		"---------------------------------\n" + \
								"| LOG STAGE 1 PLAY SCREEN       |\n" + \
								"---------------------------------"
		self.createb_txt =		"|--- creating buttons           |"
		self.timeout_txt = 		"| Time Out                      |"
		self.finish_txt = 		"| Stage Finished                |"
		print(self.start_log)

		# 2. Setting the screen buttons and widgets
		self.buttons = []
		self.widgets = []

		# a. buttons
		self.radius = 2*self.sw/3 if self.sw < self.sh else 2*self.sh/3
		self.center_w, self.center_h = self.sw/2, 4*self.sh/5
		self.createButtons(self.center_h, self.center_w, self.radius)
		utils.ableButtonsAndMouse(self)

		# b. points counter
		self.points_label = tkinter.Label(self.master, textvariable=self.points, width=3,\
									 bg='white', fg = 'black',\
									 font=Font(family='Helvetica', size=30, weight='bold'),\
									 padx=20,pady=20,bd=4,highlightbackground='black',\
									 highlightthickness=2, relief="solid")
		self.points_label.place(x=self.center_w,y=self.center_h,anchor='center')

		# c. loading sound and reset mouse position
		#mixer.init()
		#mixer.music.load('local/default/sfx.wav')
		utils.reset_mouse_position(self)

	def update_variables(self,prev_sc):
		# a. screen var
		self.points = tkinter.StringVar()
		self.points.set(0)

		# b. round var
		self.game = {}
		self.game['answer'] = []
		self.game['reinforced'] = []
		self.game['time2answer'] = []
		self.game['frequency'] = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0}
		self.round_start_time = datetime.datetime.now()

		# c. block var
		self.game['block_time'] = []
		self.block_start_time = datetime.datetime.now()

	def createButtons(self, center_h, center_w,radius):
		print(self.createb_txt)
		self.button_1 = CircularButton(self.master,100,100,
			color = RED,bg = BG_COLOR, command=self.button1_click)
		self.button_1.place(x=center_w-radius,
							y=center_h,
							anchor='center')
		self.buttons.append(self.button_1)

		self.button_2 = CircularButton(self.master,100,100,
			color = RED,bg = BG_COLOR, command=self.button2_click)
		self.button_2.place(x=center_w-radius*cos(pi/7),
					 		y=center_h-radius*sin(pi/7),
					 		anchor='center')
		self.buttons.append(self.button_2)

		self.button_3 = CircularButton(self.master,100,100,
			color = RED,bg = BG_COLOR, command=self.button3_click)
		self.button_3.place(x=center_w-radius*cos(2*pi/7),
					 		y=center_h-radius*sin(2*pi/7),
					 		anchor='center')
		self.buttons.append(self.button_3)

		self.button_4 = CircularButton(self.master,100,100,
			color = RED,bg = BG_COLOR, command=self.button4_click)
		self.button_4.place(x=center_w-radius*cos(3*pi/7),
					 		y=center_h-radius*sin(3*pi/7),
					 		anchor='center')
		self.buttons.append(self.button_4)

		self.button_5 = CircularButton(self.master,100,100,
			color = RED,bg = BG_COLOR, command=self.button5_click)
		self.button_5.place(x=center_w-radius*cos(4*pi/7),
					 		y=center_h-radius*sin(4*pi/7),
					 		anchor='center')
		self.buttons.append(self.button_5)

		self.button_6 = CircularButton(self.master,100,100,
			color = RED,bg = BG_COLOR, command=self.button6_click)
		self.button_6.place(x=center_w-radius*cos(5*pi/7),
					 		y=center_h-radius*sin(5*pi/7),
					 		anchor='center')
		self.buttons.append(self.button_6)

		self.button_7 = CircularButton(self.master,100,100,
			color = RED,bg = BG_COLOR, command=self.button7_click)
		self.button_7.place(x=center_w-radius*cos(6*pi/7),
					 		y=center_h-radius*sin(6*pi/7),
					 		anchor='center')
		self.buttons.append(self.button_7)

		self.button_8 = CircularButton(self.master,100,100,
			color = RED,bg = BG_COLOR, command=self.button8_click)
		self.button_8.place(x=center_w-radius*cos(pi),
					 		y=center_h-radius*sin(pi),
					 		anchor='center')
		self.buttons.append(self.button_8)


	# THE GAME METHODS
	def button1_click(self):
		print("|--- button 1 click             |")
		self.check_action(1)

	def button2_click(self):
		print("|--- button 2 click             |")
		self.check_action(2)

	def button3_click(self):
		print("|--- button 3 click             |")
		self.check_action(3)

	def button4_click(self):
		print("|--- button 4 click             |")
		self.check_action(4)

	def button5_click(self):
		print("|--- button 5 click             |")
		self.check_action(5)

	def button6_click(self):
		print("|--- button 6 click             |")
		self.check_action(6)

	def button7_click(self):
		print("|--- button 7 click             |")
		self.check_action(7)

	def button8_click(self):
		print("|--- button 8 click             |")
		self.check_action(8)

	def check_action(self,clicked_button):
		# a. updating game log
		self.game['answer'].append(clicked_button)
		self.game['reinforced'].append(True)
		self.game['time2answer'].append(datetime.datetime.now() - self.round_start_time)
		self.game['frequency'][clicked_button] += 1

		# b.reinforcing the action
		utils.removeButtons(self.buttons)
		self.cur_color = np.array(BG_COLOR)
		self.ref_color = np.array(BG_COLOR) - np.array(GREEN)
		self.reinforce_action()

	def reinforce_action(self):
		# a. calculating the color fade (to green)
		self.cur_color -= (0.1*self.ref_color)
		
		# b. changing background color
		self.main_bg.configure(bg="#%02x%02x%02x" % \
			(int(self.cur_color[0]),int(self.cur_color[1]),int(self.cur_color[2])))

		# c. checking the fade stop
		if (self.ref_color[1] >= 0 and int(self.cur_color[1]) > 200)\
		 or (self.ref_color[1] < 0 and int(self.cur_color[1]) < 200):
			self.master.after(50,self.reinforce_action)
		else:
			# - setting green bg
			self.main_bg.configure(bg="#%02x%02x%02x" % (0,200,0))
			#self.master.after(int(float(self.settings['iti'])*1000),self.replay)
			self.master.after(1*1000,self.replay)

	def replay(self):
		# 1. Writing results in log file

		# 2. Checking replay conditions
		# a. end stage
		if self.check_stage_conditions():
			self.rgb = np.array([0.0,200.0,0.0])
			self.win_txt = tkinter.Label(self.master, bg= "#%02x%02x%02x" % (0, 200, 0), fg = "#%02x%02x%02x" % (0, 200, 0),\
				 text='ATÉ O MOMENTO VOCÊ ACUMULOU '+str(int(self.points.get())+int(self.prev_sc.points.get()))+\
				 ' PONTOS!', font=Font(family='Helvetica', size=16, weight='bold'))
			self.master.after(20,self.fadeResetText)
		# b. keep playing
		else:
			# - setting the round start variable
			self.round_start_time = datetime.datetime.now()
			self.main_bg.configure(bg="#%02x%02x%02x" %\
			 	(int(BG_COLOR[0]),int(BG_COLOR[1]),int(BG_COLOR[2])))

			# - creating the buttons
			self.createButtons(self.center_h, self.center_w, self.radius)

	def check_stage_conditions(self):
		return False

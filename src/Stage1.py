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

class Stage1:

	def __init__(self, master, prev_sc, main_bg):
		# 1. Initializing the necessary variables
		# a. screen and log components
		self.master = master
		self.main_bg = main_bg
		self.update_variables(prev_sc)
		utils.update_screen(self)
		self.sw, self.sh = master.winfo_screenwidth(), master.winfo_screenheight()

		# c. log text
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
		radius = 2*self.sw/3 if self.sw < self.sh else 2*self.sh/3
		center_w, center_h = self.sw/2, 4*self.sh/5
		self.createButtons(center_h, center_w, radius)
		utils.ableButtonsAndMouse(self)

		# b. points counter
		self.points_label = tkinter.Label(self.master, textvariable=self.points, width=3,\
									 bg='white', fg = 'black',\
									 font=Font(family='Helvetica', size=30, weight='bold'),\
									 padx=20,pady=20,bd=4,highlightbackground='black',\
									 highlightthickness=2, relief="solid")
		self.points_label.place(x=center_w,y=center_h,anchor='center')

		# c. loading sound and reset mouse position
		#mixer.init()
		#mixer.music.load('local/default/sfx.wav')
		utils.reset_mouse_position(self)

	def update_variables(self,prev_sc):
		self.points = tkinter.StringVar()
		self.points.set(0)

	def createButtons(self, center_h, center_w,radius):
		print(self.createb_txt)
		self.button_1 = CircularButton(self.master,100,100,(255,0,0))
		self.button_1.place(x=center_w-radius,
							y=center_h,
							anchor='center')
		self.buttons.append(self.button_1)

		self.button_2 = CircularButton(self.master,100,100,(255,0,0))
		self.button_2.place(x=center_w-radius*cos(pi/7),
					 		y=center_h-radius*sin(pi/7),
					 		anchor='center')
		self.buttons.append(self.button_2)

		self.button_3 = CircularButton(self.master,100,100,(255,0,0))
		self.button_3.place(x=center_w-radius*cos(2*pi/7),
					 		y=center_h-radius*sin(2*pi/7),
					 		anchor='center')
		self.buttons.append(self.button_3)

		self.button_4 = CircularButton(self.master,100,100,(255,0,0))
		self.button_4.place(x=center_w-radius*cos(3*pi/7),
					 		y=center_h-radius*sin(3*pi/7),
					 		anchor='center')
		self.buttons.append(self.button_4)

		self.button_5 = CircularButton(self.master,100,100,(255,0,0))
		self.button_5.place(x=center_w-radius*cos(4*pi/7),
					 		y=center_h-radius*sin(4*pi/7),
					 		anchor='center')
		self.buttons.append(self.button_5)

		self.button_6 = CircularButton(self.master,100,100,(255,0,0))
		self.button_6.place(x=center_w-radius*cos(5*pi/7),
					 		y=center_h-radius*sin(5*pi/7),
					 		anchor='center')
		self.buttons.append(self.button_6)

		self.button_7 = CircularButton(self.master,100,100,(255,0,0))
		self.button_7.place(x=center_w-radius*cos(6*pi/7),
					 		y=center_h-radius*sin(6*pi/7),
					 		anchor='center')
		self.buttons.append(self.button_7)

		self.button_8 = CircularButton(self.master,100,100,(255,0,0))
		self.button_8.place(x=center_w-radius*cos(pi),
					 		y=center_h-radius*sin(pi),
					 		anchor='center')
		self.buttons.append(self.button_8)


	# THE GAME METHODS
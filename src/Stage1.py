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
		self.createButtons()
		utils.ableButtonsAndMouse(self)

		# b. points counter
		self.points_label = tkinter.Label(self.master, textvariable=self.points, width=3,\
									 bg='white', fg = 'black',\
									 font=Font(family='Helvetica', size=30, weight='bold'),\
									 padx=20,pady=20,bd=4,highlightbackground='black',\
									 highlightthickness=2, relief="solid")
		self.points_label.place(x=self.sw/2,y=self.sh/2,anchor='center')

		# c. loading sound and reset mouse position
		#mixer.init()
		#mixer.music.load('local/default/sfx.wav')
		utils.reset_mouse_position(self)

	def update_variables(self,prev_sc):
		self.points = tkinter.StringVar()
		self.points.set(0)

	def createButtons(self):
		print(self.createb_txt)
		self.button_n = CircularButton(self.master,100,100,(255,0,0))
		self.button_n.place(x=self.sw/2,y=self.sh/4,anchor='center')
		self.buttons.append(self.button_n)

	# THE GAME METHODS
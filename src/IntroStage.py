# Interface Imports
import tkinter
from tkinter import *
from tkinter import font
from tkinter import LEFT, RIGHT, BOTTOM, TOP, NONE
from tkinter import messagebox, filedialog, StringVar
from tkinter.font import Font

# Protocol, Plots and utils imports
import datetime
import os
import random
import re
import utils

import log
from MyCommons import *
from utils import *
from Screen import Screen

class IntroStage(Screen):

	def __init__(self, master, prev_sc, main_bg):
		# 1. Initilising GUI Components
		super().__init__(master, prev_sc, main_bg,screen_name='IntroStage')
		print(self.nickname,self.start_time,self.group,self.stage)
		self.points = self.prev_sc.points

		# 2. Buttons Functions
		# a. intro text
		if(self.settings['return_click'] == True):
			text = utils.load_text(prev_sc.stage)
			text +=  utils.load_text("Click")
		else:
			text = utils.load_text(prev_sc.stage)
		
		self.text_display = scrolledtext.ScrolledText(self.master, fg = 'black', font = Font(family='Helvetica', size=18),\
									 bg = "#%02x%02x%02x" % (255, 255, 255), insertbackground = 'black',\
									 highlightcolor = "#%02x%02x%02x" % (180,180,180), highlightbackground= "#%02x%02x%02x" % (50,50,50),\
									  bd=0, width =47, height=10, padx=10, pady=10, wrap='word',undo=True)
		self.text_display.insert('insert',text)
		self.text_display.configure(state='disabled')
		self.text_display.place(x=self.sw/2,y=self.sh/2,anchor='center')
		self.widgets.append(self.text_display)

		# b. start button
		if (self.stage == 1):
			self.start_button = \
				create_button(self.master,'AVANÇAR',self.goToStage1,\
					self.sw/2,5*self.sh/6,size=18)
		elif (self.stage == 2):
			self.start_button = \
				create_button(self.master,'AVANÇAR',self.goToStage2,\
					self.sw/2,5*self.sh/6,size=18)
		elif (self.stage == 3):
			self.start_button = \
				create_button(self.master,'AVANÇAR',self.goToStage3,\
					self.sw/2,5*self.sh/6,size=18)
		elif (self.stage == 4):
			self.start_button = \
				create_button(self.master,'AVANÇAR',self.goToStage4,\
					self.sw/2,5*self.sh/6,size=18)
		elif (self.stage == 5):
			self.start_button = \
				create_button(self.master,'AVANÇAR',self.goToStage5,\
					self.sw/2,5*self.sh/6,size=18)
		elif (self.stage == 6):
			self.start_button = \
				create_button(self.master,'AVANÇAR',self.goToStage6,\
					self.sw/2,5*self.sh/6,size=18)

		self.widgets.append(self.start_button)
		self.buttons.append(self.start_button)
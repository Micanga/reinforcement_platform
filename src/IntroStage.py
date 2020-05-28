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

		# 2. Buttons Functions
		# a. intro text
		text = utils.load_text(prev_sc.stage)
		self.text_display = scrolledtext.ScrolledText(master, fg = 'black', font = Font(family='Helvetica', size=18),\
									 bg = "#%02x%02x%02x" % (255, 255, 255), insertbackground = 'black',\
									 highlightcolor = "#%02x%02x%02x" % (180,180,180), highlightbackground= "#%02x%02x%02x" % (50,50,50),\
									  bd=0, width =47, height=10, padx=10, pady=10, wrap='word',undo=True)
		self.text_display.insert('insert',text)
		self.text_display.configure(state='disabled')
		self.text_display.place(x=self.sw/2,y=self.sh/2,anchor='center')

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

		self.widgets.append(self.start_button)
		self.buttons.append(self.start_button)

		# c. creating the result file
		log.create_file(self.nickname,self.start_time)
			
	def create_label_entry(self,label_text,x,y):
		# 1. Creating Entry Label
		label = tkinter.Label(self.master, bg="#%02x%02x%02x" % (255, 255, 255),justify='left',\
			fg = 'black', text=label_text, font=Font(family='Helvetica', size=20))
		label.place(x=x,y=y,anchor='center')

		# 2. Creating the Entry
		entry = tkinter.Entry(self.master, fg = 'black', font = Font(family='Helvetica', size=20),\
									 bg = "#%02x%02x%02x" % (255, 255, 255), insertbackground = 'black',\
									 highlightcolor = "#%02x%02x%02x" % (180,180,180), highlightbackground= "#%02x%02x%02x" % (50,50,50),\
									  bd=0, width = 33, justify='center')
		entry.place(x = x, y = y+50,anchor='center')

		# 3. Returning
		return label,entry
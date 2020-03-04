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

from MyCommons import *
from utils import *
from Screen import Screen

class ChooseExperiment(Screen):

	def __init__(self, master, prev_sc, main_bg):
		# 1. Initilising GUI Components
		# a. screen and log components
		
		super().__init__(master, prev_sc, main_bg,'bg/choose.png')
		self.nickname = self.prev_sc.nickname

		# b. log components
		self.start_log = 		"---------------------------------\n" + \
								"| LOG CHOOSE EXP SCREEN         |\n" + \
								"---------------------------------\n"+\
								"| Nickname Received "+prev_sc.nickname+"\n"
		self.back_txt = 		"| Back Button Pressed           |"
		print(self.start_log)

		# 2. Buttons Functions
		# a. Group Menu
		self.group_label = tkinter.Label(self.master, bg="#%02x%02x%02x" % (255, 255, 255),justify='left',\
			fg = 'black', text='GRUPO', font=Font(family='Helvetica', size=20),
			padx=10,pady=10,bd=4, relief="solid", width=15)
		self.group_label.place(x=self.sw/3,y=self.sh/2-50,anchor='center')
		self.widgets.append(self.group_label)

		group_list = ['1','2','3']
		group_var = StringVar(self.master)
		group_var.set(group_list[0])
		self.group_option = OptionMenu(self.master, group_var, *group_list)
		self.group_option.config(width = 5, 
			font = Font(family='Helvetica', size=18, weight='bold'),
			bd=3, relief="solid")
		self.group_option.place(x=self.sw/3,y=self.sh/2,anchor='center')
		self.widgets.append(self.group_option)
		self.buttons.append(self.group_option)

		# b. Stage Menu
		self.stage_label = tkinter.Label(self.master, bg="#%02x%02x%02x" % (255, 255, 255),justify='left',\
			fg = 'black', text='FASE', font=Font(family='Helvetica', size=20),
			padx=10,pady=10,bd=4, relief="solid", width=15)
		self.stage_label.place(x=2*self.sw/3,y=self.sh/2-50,anchor='center')
		self.widgets.append(self.stage_label)

		stage_list = ['1','2','3','4','5','6','7']
		stage_var = StringVar(self.master)
		stage_var.set(stage_list[0])
		self.stage_option = OptionMenu(self.master, stage_var, *stage_list)
		self.stage_option.config(width = 5, 
			font = Font(family='Helvetica', size=18, weight='bold'),
			bd=3, relief="solid")
		self.stage_option.place(x=2*self.sw/3,y=self.sh/2,anchor='center')
		self.widgets.append(self.stage_option)
		self.buttons.append(self.stage_option)

		# c. Main Label
		self.main_label = tkinter.Label(self.master, bg="#%02x%02x%02x" % (255, 255, 255),justify='left',\
			fg = 'black', text='ESCOLHA O GRUPO E A FASE DO EXPERIMENTO', font=Font(family='Helvetica', size=20),
			padx=10,pady=10)
		self.main_label.place(x=self.sw/2,y=self.sh/4,anchor='center')
		self.widgets.append(self.main_label)

		#start button
		self.start_button = \
			create_button(self.master,'AVANÇAR',self.start_button_click,\
				8*self.sw/10,5*self.sh/6,size=18)
		self.widgets.append(self.start_button)
		self.buttons.append(self.start_button)

		#back button
		self.back_button = \
			create_button(self.master,'VOLTAR',self.goToNickName,\
				2*self.sw/10,5*self.sh/6,size=18)
		self.widgets.append(self.back_button)
		self.buttons.append(self.back_button)
			
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

	def start_button_click(self):
		from IntroStage import IntroStage
		IntroStage(self.master,self,self.main_bg)
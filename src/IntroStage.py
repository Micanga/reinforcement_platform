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
		if(self.stage == 1 or self.stage == 4):
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
			if self.group != 1:
				while(re.search("_G"+str(self.group-1)+"_F2_",self.aco_file) is None):
					if self.settings['choose_aco']:
						self.aco_file = tkinter.filedialog.askopenfilename(title='SELECIONE O ARQUIVO PARA ACOPLAMENTO',\
							filetypes=[("CSV",".csv")],initialdir = "./results/")
						self.aco_file = self.aco_file.split('/')[-1]
					else:
						result_files = os.listdir("./results/")
						selected_files = [filename for filename in result_files if re.search("_G"+str(self.group-1)+"_F2_",filename) is not None]
						self.aco_file = random.choice(selected_files)
						self.aco_file = self.aco_file.split('/')[-1]
					print(self.aco_file)
				
					if re.search("_G"+str(self.group-1)+"_F2_",self.aco_file) is None:
						messagebox.showinfo("Information",\
											'Por favor, selecione um arquivo para ACOPLAMENTO. Este deve corresponder à resultados coletados em experimentos do Grupo '+str(self.group-1)+' Fase 2.\nID: _G'+str(self.group-1)+'_F2_')

			self.start_button = \
				create_button(self.master,'AVANÇAR',self.goToStage1,\
					self.sw/2,5*self.sh/6,size=18)
			self.widgets.append(self.start_button)
			self.buttons.append(self.start_button)

		elif (self.stage == 2):
			self.goToStage2()

		elif (self.stage == 3):
			self.goToStage3()

		elif (self.stage == 4):
			if self.group != 1:
				while(re.search("_G"+str(self.group-1)+"_F5_",self.aco_file) is None):
					if self.settings['choose_aco']:
						self.aco_file = tkinter.filedialog.askopenfilename(title='SELECIONE O ARQUIVO PARA ACOPLAMENTO',\
							filetypes=[("CSV",".csv")],initialdir = "./results/")
						self.aco_file = self.aco_file.split('/')[-1]
					else:
						result_files = os.listdir("./results/")
						selected_files = [filename for filename in result_files if re.search("_G"+str(self.group-1)+"_F5_",filename) is not None]
						self.aco_file = random.choice(selected_files)
						self.aco_file = self.aco_file.split('/')[-1]
				
					if re.search("_G"+str(self.group-1)+"_F5_",self.aco_file) is None:
						messagebox.showinfo("Information",\
											'Por favor, selecione um arquivo para ACOPLAMENTO. Este deve corresponder à resultados coletados em experimentos do Grupo '+str(self.group-1)+' Fase 5.\nID: _G'+str(self.group-1)+'_F5_')

			self.start_button = \
				create_button(self.master,'AVANÇAR',self.goToStage4,\
					self.sw/2,5*self.sh/6,size=18)
			self.widgets.append(self.start_button)
			self.buttons.append(self.start_button)

		elif (self.stage == 5):
			self.goToStage5()
			
		elif (self.stage == 6):
			self.goToStage6()

		

	def ableButtons(self):
		print("| -- enabling the buttons")
		for b in self.buttons:
			b.configure(state="normal")
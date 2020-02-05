# Interface Imports
import tkinter
from tkinter import *
from tkinter import font
from tkinter import LEFT, RIGHT, BOTTOM, TOP, NONE
from tkinter import messagebox, filedialog, StringVar
from tkinter.font import Font

from utils import *
from MyCommons import *

class Menu:

	def __init__(self, master, prev_sc, main_bg):
		# 1. Initilising GUI Components
		# a. screen and log components
		self.master = master
		self.main_bg = main_bg
		self.main_bg.destroy()
		self.sw, self.sh = self.master.winfo_screenwidth(), self.master.winfo_screenheight()

		self.start_log = 		"---------------------------------\n" + \
								"| LOG MENU SCREEN               |\n" + \
								"---------------------------------"
		self.start_txt = 		"| Start Action Button Pressed   |"
		self.settings_txt = 	"| Settings Button pressed       |"
		self.exit_txt = 		"| Exit Button Pressed           |"
		print(self.start_log)

		# b. setting background
		set_bg(self.master,self.main_bg,'bg/main.png')

		# 2. Setting Functions
		self.widgets = []

		# a. Start Button
		self.start_button = \
			create_button(self.master,'JOGAR',self.start_button_click,\
				self.sw/3,self.sh/3,'#f01515')
		self.widgets.append(self.start_button)

		# b. Settings Button
		self.settings_button = \
			create_button(self.master,'CONFIGURAR',self.settings_button_click,\
				2*self.sw/3,self.sh/3,'#2BA1EE')
		self.widgets.append(self.settings_button)

		# c. Exit Button
		self.exit_button = \
			create_button(self.master,'SAIR',self.exit_button_click,\
				self.sw/2,2*self.sh/3,'#37EE2B')
		self.widgets.append(self.exit_button)

	def start_button_click(self):
		print(self.start_txt)

		destroyWidgets(self.widgets)

		#Choose Experiment Screen
		'''
		from ChooseExperiment import ChooseExperiment
		ChooseExperiment(self.master,self,self.main_bg)
		'''

		#Nickname Screen
		from NickName import NickName
		NickName(self.master,self,self.main_bg)


	def settings_button_click(self):
		print(self.settings_txt)

		destroyWidgets(self.widgets)

		from Settings import Settings
		Settings(self.master,self,self.main_bg)

	def exit_button_click(self):
		print(self.exit_txt)

		destroyWidgets(self.widgets)

		self.master.destroy()
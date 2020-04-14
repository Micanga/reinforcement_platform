# Interface Imports
import tkinter
from tkinter import *
from tkinter import font
from tkinter import LEFT, RIGHT, BOTTOM, TOP, NONE
from tkinter import messagebox, filedialog, StringVar
from tkinter.font import Font

from utils import *
from MyCommons import *

from Screen import Screen

class Menu(Screen):

	def __init__(self, master, prev_sc, main_bg):
		# 1. Initializing the necessary variables
		# a. initializing the screen
		super().__init__(master, prev_sc, main_bg,'bg/main.png')

		# b. log text
		self.start_log = 		"---------------------------------\n" + \
								"| LOG STAGE 1 PLAY SCREEN       |\n" + \
								"---------------------------------"
		self.createb_txt =		"|--- creating buttons           |"
		self.timeout_txt = 		"| Time Out                      |"
		self.finish_txt = 		"| Stage Finished                |"
		print(self.start_log)

		# 2. Setting the screen buttons and widgets
		# a. Start Button
		start_button = \
			create_button(self.master,'JOGAR',self.goToNickName,\
				self.sw/3,self.sh/3,'#f01515')
		self.widgets.append(start_button)
		self.buttons.append(start_button)

		# b. Settings Button
		settings_button = \
			create_button(self.master,'CONFIGURAR',self.goToSettings,\
				2*self.sw/3,self.sh/3,'#2BA1EE')
		self.widgets.append(settings_button)
		self.buttons.append(settings_button)

		# c. Exit Button
		exit_button = \
			create_button(self.master,'SAIR',self.goToExit,\
				self.sw/2,2*self.sh/3,'#37EE2B')
		self.widgets.append(exit_button)
		self.buttons.append(exit_button)

# Interface Imports
import tkinter
from tkinter import *
from tkinter import font
from tkinter import LEFT, RIGHT, BOTTOM, TOP, NONE
from tkinter import messagebox, filedialog, StringVar
from tkinter.font import Font

from utils import *

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
		# a. Start Button
		self.start_button = \
			self.create_button('JOGAR',self.start_button_click,\
				self.sw/3,self.sh/3,'#f01515')

		# b. Settings Button
		self.settings_button = \
			self.create_button('CONFIGURAR',self.settings_button_click,\
				2*self.sw/3,self.sh/3,'#2BA1EE')

		# c. Exit Button
		self.exit_button = \
			self.create_button('SAIR',self.exit_button_click,\
				self.sw/2,2*self.sh/3,'#37EE2B')

	def create_button(self,text,func,x,y,color='#1E1E1E'):
		button = Button(self.master, text = text,
			font = Font(family='Helvetica', size=36, weight='bold'),
			fg = 'white', bg = color, 
			anchor = 'center', compound = 'center', 
			command = func,
			highlightbackground='#1E1E1E',
			highlightthickness = 0, 
			bd = 5, padx=0, pady=0, height=2, width=13)
		button.place(x = x, y = y, anchor= 'center')
		return button

	def start_button_click(self):
		print(self.start_txt)

		self.destroyWidgets()

		from ChooseExperiment import ChooseExperiment
		ChooseExperiment(self.master,self,self.main_bg)

	def settings_button_click(self):
		print(self.settings_txt)

		self.destroyWidgets()

		from Settings import Settings
		Settings(self.master,self,self.main_bg)

	def exit_button_click(self):
		print(self.exit_txt)

		self.destroyWidgets()

		self.master.destroy()

	def destroyWidgets(self):
		self.start_button.destroy()
		self.settings_button.destroy()
		self.exit_button.destroy()
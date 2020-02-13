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


class Menu():

	def __init__(self, master, prev_sc, main_bg):
		# 1. Initilising GUI Components
		# a. screen and log components
		MenuScreen = Screen(master, prev_sc, main_bg)

		# b. setting background
		set_bg(MenuScreen.master,MenuScreen.main_bg,'bg/main.png')

		# a. Start Button
		MenuScreen.start_button = \
			create_button(MenuScreen.master,'JOGAR',MenuScreen.goToNickName,\
				MenuScreen.sw/3,MenuScreen.sh/3,'#f01515')
		MenuScreen.widgets.append(MenuScreen.start_button)

		# b. Settings Button
		MenuScreen.settings_button = \
			create_button(MenuScreen.master,'CONFIGURAR',MenuScreen.goToSettings,\
				2*MenuScreen.sw/3,MenuScreen.sh/3,'#2BA1EE')
		MenuScreen.widgets.append(MenuScreen.settings_button)
		MenuScreen.buttons.append(MenuScreen.settings_button)

		# c. Exit Button
		MenuScreen.exit_button = \
			create_button(MenuScreen.master,'SAIR',MenuScreen.goToExit,\
				MenuScreen.sw/2,2*MenuScreen.sh/3,'#37EE2B')
		MenuScreen.widgets.append(MenuScreen.exit_button)
		MenuScreen.buttons.append(MenuScreen.exit_button)


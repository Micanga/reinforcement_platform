# Imports
from MyCommons import *
from Screen import Screen
import utils

class Stage1(Screen):

	def __init__(self, master, prev_sc, main_bg):
		self.AUTO = True
		# 1. Initializing the necessary variables
		# a. initializing the screen
		super().__init__(master, prev_sc, main_bg)
		self.update_variables()
		self.game[-1]['frequency'] = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0}
		self.game[-1]['points'] = 0

		# b. log text
		self.start_log = 		"---------------------------------\n" + \
								"| LOG STAGE 1 PLAY SCREEN       |\n" + \
								"---------------------------------"
		self.createb_txt =		"|--- creating buttons           |"
		self.timeout_txt = 		"| Time Out                      |"
		self.finish_txt = 		"| Stage Finished                |"
		print(self.start_log)

		# 2. Setting the screen buttons and widgets
		# a. buttons
		self.radius = 2*self.sw/3 if self.sw < self.sh else 2*self.sh/3
		self.center_w, self.center_h = self.sw/2, 4*self.sh/5
		self.createButtons(self.center_h, self.center_w, self.radius)
		utils.ableButtonsAndMouse(self)

		# b. points counter
		self.points = tkinter.StringVar()
		self.points.set(0)
		self.createPointCounter()

		# c. sound effects
		self.load_sfx()

		# d. auto-play
		if self.AUTO:
			self.auto_play()

	# THE STAGE METHODS
	def check_stage_end_conditions(self):
		# if the number of blocks is greather than 16, finish the stage
		if self.number_of_blocks() > 16:
			return True
		# else keep playing
		return False

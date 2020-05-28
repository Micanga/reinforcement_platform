# Imports
from MyCommons import *
from Screen import Screen
import utils

class Stage1(Screen):

	def __init__(self, master, prev_sc, main_bg):
		self.AUTO = False
		# 1. Initializing the necessary variables
		super().__init__(master, prev_sc, main_bg,screen_name='Stage 1')
		self.init_variables()

		# 2. Setting the screen buttons and widgets
		# a. buttons
		self.createButtons(self.center_h, self.center_w, self.radius)
		utils.ableButtonsAndMouse(self)

		# b. points counter
		self.createPointCounter()

		# c. sound effects
		self.load_sfx()

		# d. auto-play
		if self.AUTO:
			self.auto_play()

	# THE STAGE METHODS
	def check_stage_end_conditions(self):
		# if the number of blocks is greather than the min of blocks
		# and the average IRT is less then the IRT threshold, finish the stage
		if self.number_of_blocks() >= self.settings['min_blocks']\
		and self.averageIRT() < self.settings['IRT_threshold']:
			return True
		# else keep playing
		return False

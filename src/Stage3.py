# Imports
from MyCommons import *
from Screen import Screen
import utils

class Stage3(Screen):

	def __init__(self, master, prev_sc, main_bg):
		self.AUTO = False
		# 1. Initializing the necessary variables
		super().__init__(master, prev_sc, main_bg,screen_name='Stage 3')
		self.init_variables()

		# 2. Setting the screen buttons and widgets
		# a. buttons
		self.createButtons(self.center_h, self.center_w, self.radius)
		utils.ableButtonsAndMouse(self)

		# b. points counter
		self.createPointCounter()

		# c. sound effects
		self.load_sfx()

		

		blocksS1 = self.getAllBlocks(self.group,self.stage-1) #(stage 1 for stage 3) or (stage 4 for stage 6) 
		blocksS2 = self.getAllBlocks(self.group,self.stage-2) #(stage 2 for stage 3) or (stage 5 for stage 6) 	
		blocksS3 = self.settings['max_blocks'] - (len(blocksS1) +  len(blocksS2)) # number of blocks from stage 3 or stage 6
		
		print("Numbers blocks of Stage3 ")
		print(blocksS3)
		print(self.game)

		# d. auto-play
		if self.AUTO:
			self.auto_play()
		
		#print(self.game)

	# THE STAGE METHODS
	def check_stage_end_conditions(self):

		# if the number of blocks is the numbers block remaining
		if self.number_of_blocks() == blocksS3:
			return True
		# else keep playing
		return False

	def conditionalReinforce(self):
		#VI (auto aco)
		print("This is conditionalReforce of Stage3")
		
		return (sum(self.game[-1]['frequency'].values()) in self.reinforced_clicks)



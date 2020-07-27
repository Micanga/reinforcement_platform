# Imports
from MyCommons import *
from Screen import Screen
import utils
from datetime import timedelta

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
		self.blocksS3 = self.settings['max_blocks'] - (len(blocksS1) +  len(blocksS2)) # number of blocks from stage 3 or stage 6
		

		stageForReinforce = self.stage - 1

		blocksForReinforce = []
		self.dateTimeReinforce = []
		self.isFirstReinforce = True

		
		#get all the blocks from the stage 2 or 5
		for block in self.game:
			if block['group'] == self.group and block['stage'] == stageForReinforce:
				blocksForReinforce.append(block)


		#for all blocks
		for block in blocksForReinforce:
			print(block)
			#get the indice for the clicks that have been reinforced
			res = [i for i, val in enumerate(block['reinforced']) if val]

			#select the datetimes
			for i in res:
				self.dateTimeReinforce.append(block['time2answer'][i])

		
			
		# d. auto-play
		if self.AUTO:
			self.auto_play()
		
		#print(self.game)

	# THE STAGE METHODS
	def check_stage_end_conditions(self):

		# if the number of blocks is the numbers block remaining
		if self.number_of_blocks() == self.blocksS3:
			return True
		# else keep playing
		return False

	def conditionalReinforce(self):
		#print(type(self))
		if(self.isFirstReinforce == True):
	
			#dateTimeReinforce[0] is after to the acctually click
			if(self.dateTimeReinforce[0] < self.game[-1]['time2answer'][-1]):
				self.isFirstReinforce = False
			else:

				return False

		if(self.isFirstReinforce == False):
			if(len(self.dateTimeReinforce) > 0):
				

				accumalator = timedelta(0,0,0)
				#dateTimeReinforce[0] is before to the acctually click
				while(len(self.dateTimeReinforce) > 0 and (self.dateTimeReinforce[0] + accumalator) < (self.game[-1]['time2answer'][-1])):
					accumalator += self.dateTimeReinforce[0]
					self.dateTimeReinforce.pop(0)

				return True

			else:
				return False

		

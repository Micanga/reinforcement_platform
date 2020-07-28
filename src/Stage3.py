# Imports
from MyCommons import *
from Screen import Screen
import utils
from datetime import timedelta
import log
import numpy as np

class Stage3(Screen):

	def __init__(self, master, prev_sc, main_bg):
		self.AUTO = True

		# 1. Initializing the necessary variables
		super().__init__(master, prev_sc, main_bg,screen_name='Stage 3')
		self.init_variables()

		# 2. creating the result file
		log.create_file(self.nickname,self.group,self.stage,self.start_time)

		# 2. Setting the screen buttons and widgets
		# a. buttons
		self.createButtons(self.center_h, self.center_w, self.radius)
		utils.ableButtonsAndMouse(self)

		# b. points counter
		self.createPointCounter()

		# c. sound effects
		self.load_sfx()

		self.aco_file = None
		self.reinforce_index = 0

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

		self.allClicks = []
		sumClicks = 0
		for block in blocksForReinforce:
			#get the index for the clicks that have been reinforced
			res = [i for i, val in enumerate(block['reinforced']) if val]
			#select the datetimes
			for i in res:
				self.dateTimeReinforce.append(block['time2answer'][i])
				sumClicks += i
				self.allClicks.append(sumClicks)

		self.setReinforcedClicks()
			
		# d. auto-play
		if self.AUTO:
			self.auto_play()

	def nextStage(self):
		myReturnMenuPopUp(self,'Parabéns! Você terminou o experimento!\nPor favor, contacte o aplicador para\nreceber futuras instruções. :)')

	# THE STAGE METHODS
	def check_stage_end_conditions(self):
		# if the number of blocks is the numbers block remaining
		if self.number_of_blocks() == self.blocksS3:
			return True
		# else keep playing
		return False

	def setReinforcedClicks(self,offset=0):
		if self.group == 1 or self.group == 3: # applying the VR scheme [G1]
			self.reinforced_clicks = np.cumsum([time.total_seconds() + offset for time in self.dateTimeReinforce])
		else:
			self.reinforced_clicks = np.array(self.allClicks) + offset
		print(self.reinforced_clicks)
		
	def conditionalReinforce(self):
		if (self.group == 1 or self.group == 3):
			time2ans_cum = np.cumsum([time.total_seconds() for time in self.game[-1]['time2answer']])[-1]
			if self.reinforce_index > len(self.reinforced_clicks) - 1 or\
			time2ans_cum > self.reinforced_clicks[-1]:
				self.reinforce_index = 0
				self.setReinforcedClicks()
				return False
			else:
				if self.reinforced_clicks[self.reinforce_index] <= time2ans_cum <= self.reinforced_clicks[self.reinforce_index+1]:
					self.reinforce_index += 1
					return True
				else:
					if time2ans_cum > self.reinforced_clicks[self.reinforce_index+1]:
						self.reinforce_index += 1
					return False
		else:
			if len(self.game[-1]['reinforced']) + 1 > self.reinforced_clicks[-1]:
				self.setReinforcedClicks()
				return False
			else:
				return any(len(self.game[-1]['reinforced']) + 1 == self.reinforced_clicks)

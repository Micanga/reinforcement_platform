# Imports
from MyCommons import *
from Screen import Screen
import utils
from datetime import timedelta
import log
import numpy as np

class Stage3(Screen):

	def __init__(self, master, prev_sc, main_bg):
		self.AUTO = False

		# 1. Initializing the necessary variables
		# a. GUI variables
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
		# a. choosing the file to aco
		if self.aco_file is None:
			self.aco_file = self.nickname+'_G'+str(self.group)+'_F'+str(self.stage -1)+\
				'_'+self.start_time.strftime("%d-%m-%Y_%Hh%Mm%Ss")+'.csv'
			print('ACO FILE:',self.aco_file)
			
		# b. defining the reinforcement condition
		if self.group == 1 or self.group == 3: # applying the VI(auto-aco) scheme [G1 and G3]
			counter, self.reinforced_clicks = 0, []
			with open("./results/"+self.aco_file) as ref_file:
				for line in ref_file:
					reinf_flag = line.split(';')[0]
					cum_time = line.split(';')[7]
					if counter != 0 and reinf_flag == 'SIM':
						self.reinforced_clicks.append(float(cum_time) + offset)
					counter += 1

		else: # applying the VR(auto-aco) scheme [G2]
			counter, self.reinforced_clicks = 0, []
			with open("./results/"+self.aco_file) as ref_file:
				for line in ref_file:
					reinf_flag = line.split(';')[0]
					if counter != 0 and reinf_flag == 'SIM':
						self.reinforced_clicks.append(counter + offset)
					counter += 1
		print(self.reinforced_clicks)
	
	#check this function for other blocks (frequency is acumulating )
	def conditionalReinforce(self):
		# checking the reinforcement for group 1 and 3 [VI (auto-aco)]
		if self.group == 1 or self.group == 3: 
			time2ans_cum = np.cumsum([time.total_seconds() for g in self.game if g['stage'] == self.game[-1]['stage'] for time in g['time2answer'] ] )[-1]
			if self.reinforce_index >= len(self.reinforced_clicks) - 1 or\
			time2ans_cum > self.reinforced_clicks[-1]:
				self.reinforce_index = 0
				self.setReinforcedClicks(time2ans_cum)
				return False
			else:
				if self.reinforced_clicks[self.reinforce_index] <= time2ans_cum <= self.reinforced_clicks[self.reinforce_index+1]:
					self.reinforce_index += 1
					return True
				else:
					if time2ans_cum > self.reinforced_clicks[self.reinforce_index+1]:
						self.reinforce_index += 1
					return False
		# checking the reinforcement for group 2 [VR (auto-aco)]
		else:
			if sum(self.game[-1]['frequency'].values()) > self.reinforced_clicks[-1]:
				self.setReinforcedClicks(sum(self.game[-1]['frequency'].values()))
				return False
			else:

				return (sum(self.game[-1]['frequency'].values()) in self.reinforced_clicks)
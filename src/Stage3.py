# Imports
from MyCommons import *
from Screen import Screen
import utils
from datetime import timedelta
import log
import numpy as np

class Stage3(Screen):

	def __init__(self, master, prev_sc, main_bg):
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

		#####
		# OFFSET
		#####
		if self.test:
			self.aco_file = '28MARCOteste1_G1_F2_28-03-2021_13h22m19s.csv'
		else:
			self.aco_file = self.nickname+'_G'+str(self.group)+'_F'+str(self.stage -1)+\
					'_'+self.start_time.strftime("%d-%m-%Y_%Hh%Mm%Ss")+'.csv'
				
		# - collecting all answers from stage 2
		with open("./results/"+self.aco_file) as ref_file:
			counter , reinf_flags, time_vector_stage2 = 0, [], []
			for line in ref_file:
				if counter != 0:
					reinf_flags.append(line.split(';')[0])
					time_vector_stage2.append(float(line.split(';')[7]))
				counter += 1
				
		self.offset_reinforce = float(time_vector_stage2[-1]) 
		if len(time_vector_stage2) > 60:
			i1 = len(reinf_flags[0:len(reinf_flags)-60]) +\
			 reinf_flags[len(reinf_flags)-60:len(reinf_flags)].index('SIM')
			self.start_static_rounds = float(time_vector_stage2[-1])  +\
			 float(time_vector_stage2[i1]) - float(time_vector_stage2[-61])
		else:
			self.start_static_rounds = float(time_vector_stage2[-1])  +\
			 float(time_vector_stage2[reinf_flags.index('SIM')])
		print('STATIC STARTS AT',self.start_static_rounds)
		
		#################
		blocksS1 = self.getAllBlocks(self.group,self.stage-1) #(stage 1 for stage 3) or (stage 4 for stage 6) 
		blocksS2 = self.getAllBlocks(self.group,self.stage-2) #(stage 2 for stage 3) or (stage 5 for stage 6) 
		self.blocksS3 = 60 - (len(blocksS1) +  len(blocksS2)) # number of blocks from stage 3 or stage 6
		self.setReinforcedClicks(offset=0)
			
		# reseting the mouse
		if self.settings['return_click']:
			utils.reset_mouse_position(self)
			
		# d. auto-play
		if self.test:
			self.auto_play()

	def nextStage(self):
		myReturnMenuPopUp(self,'Parabéns! Você terminou o experimento!\nPor favor, contacte o aplicador para\nreceber futuras instruções. :)')

	# THE STAGE METHODS
	def check_stage_end_conditions(self):
		# if the number of blocks is the numbers block remaining
		if self.number_of_blocks() == self.blocksS3:
			return True
		# else keep playing
		else:
			return False

	def setReinforcedClicks(self,offset=0):
		# a. choosing the file to aco
		if self.aco_file is None:
			self.aco_file = self.nickname+'_G'+str(self.group)+'_F'+str(self.stage -1)+\
				'_'+self.start_time.strftime("%d-%m-%Y_%Hh%Mm%Ss")+'.csv'
			print('ACO FILE:',self.aco_file)
			
		# b. defining the reinforcement condition
		if self.group == 1 or self.group == 3: # applying the VI(auto-aco) scheme [G1 and G3]
			counter, negative_offset = 0, 0
			reinf_flags, self.reinforced_clicks = [], []

			# - collecting all answers from stage 2
			with open("./results/"+self.aco_file) as ref_file:
				for line in ref_file:
					if counter != 0:
						reinf_flags.append(line.split(';')[0])
						cum_time = line.split(';')[7]
						self.reinforced_clicks.append(float(cum_time))
					counter += 1

			# - splitting 6 last blocks for reinforce
			time_vector_stage3 = np.cumsum([time.total_seconds() for g in self.game \
				if g['stage'] == self.game[-1]['stage'] for time in g['time2answer'] ])
			time2ans_cum = time_vector_stage3[-1] if len(time_vector_stage3) > 0 else 0
			time2ans_cum +=  (datetime.datetime.now() - self.round_start_time).total_seconds()

			if self.start_static_rounds == np.inf:
				print('||| estabilidade ativada |||')
				if len(self.reinforced_clicks) > 60:
					negative_offset = self.reinforced_clicks[len(self.reinforced_clicks)-61]
					self.reinforced_clicks = self.reinforced_clicks[len(self.reinforced_clicks)-60:len(self.reinforced_clicks)]
					reinf_flags = reinf_flags[len(reinf_flags)-60:len(reinf_flags)]

			# - setting reinforcement only
			for i in range(len(reinf_flags)-1,-1,-1):
				if reinf_flags[i] == 'NAO':
					del self.reinforced_clicks[i]

			print('NEG:',negative_offset,'LEN',len(self.reinforced_clicks))
			print('>',self.reinforced_clicks)

			# - calculating the reinforcment with offset
			for i in range(len(self.reinforced_clicks)):
				self.reinforced_clicks[i] += (offset - negative_offset)

			print('>>',self.reinforced_clicks)
			
		else: # applying the VR(auto-aco) scheme [G2]
			counter, self.reinforced_clicks = 0, []
			with open("./results/"+self.aco_file) as ref_file:
				for line in ref_file:
					reinf_flag = line.split(';')[0]
					if counter != 0 and reinf_flag == 'SIM':
						self.reinforced_clicks.append(counter + offset)
					counter += 1
	
	#check this function for other blocks (frequency is acumulating )
	def conditionalReinforce(self):
		# checking the reinforcement for group 1 and 3 [VI (auto-aco)]
		if self.group == 1 or self.group == 3: 
			# - calculating the cum time for stage 3
			time_vector_stage3 = np.cumsum([time.total_seconds() for g in self.game \
				if g['stage'] == self.game[-1]['stage'] for time in g['time2answer'] ])
			time2ans_cum = time_vector_stage3[-1] if len(time_vector_stage3) > 0 else 0
			time2ans_cum +=  (datetime.datetime.now() - self.round_start_time).total_seconds()
			
			# - verifying the start of the static rounds
			if self.start_static_rounds < time2ans_cum:
				self.start_static_rounds = np.inf

				self.reinforce_index = 0
				self.setReinforcedClicks(offset=self.offset_reinforce)
				self.offset_reinforce = self.reinforced_clicks[-1]

			# - checking the reinforce
			positive_reinforce = False
			if self.reinforce_index < len(self.reinforced_clicks):
				if self.reinforced_clicks[self.reinforce_index] <= time2ans_cum:
					while self.reinforce_index < len(self.reinforced_clicks) and \
					 self.reinforced_clicks[self.reinforce_index] <= time2ans_cum:
						self.reinforce_index += 1
					positive_reinforce = True

			# - checking the reinforce overlap
			while self.reinforce_index == len(self.reinforced_clicks):
				self.start_static_rounds = np.inf

				self.reinforce_index = 0
				self.setReinforcedClicks(offset=self.offset_reinforce)
				self.offset_reinforce = self.reinforced_clicks[-1]

				while self.reinforce_index < len(self.reinforced_clicks) and \
				self.reinforced_clicks[self.reinforce_index] <= time2ans_cum:
					self.reinforce_index += 1	

			return positive_reinforce

		# checking the reinforcement for group 2 [VR (auto-aco)]
		else:
			if sum(self.game[-1]['frequency'].values()) > self.reinforced_clicks[-1]:
				self.setReinforcedClicks(sum(self.game[-1]['frequency'].values()))
				return False
			else:

				return (sum(self.game[-1]['frequency'].values()) in self.reinforced_clicks)
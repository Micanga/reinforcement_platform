import numpy as np
import os
import random
import re
import tkinter
from tkinter import *

import datetime

import log
import utils

from Screen import Screen

class Stage2(Screen):
	
	def __init__(self, master, prev_sc, main_bg):
		# 1. Initializing the necessary variables
		# a. GUI variables
		super().__init__(master, prev_sc, main_bg,screen_name='Stage 2')
		self.init_variables()

		# 2. creating the result file
		log.create_file(self.nickname,self.group,self.stage,self.start_time)

		# 2. Setting the screen buttons and widgets
		# a. interface components
		self.createButtons(self.center_h, self.center_w, self.radius)
		utils.ableButtonsAndMouse(self)

		# b. points counter
		self.createPointCounter()

		# c. sound effects
		self.load_sfx()
		self.reinforce_index = 0

		# d. set the offset
		# - verifying the aco file
		if self.test:
			self.aco_file = 'G1S1aco13_G1_F2_13-05-2021_21h03m47s.csv'

		self.set_offset()

		# d. reinforce vectors
		self.VR5_index = 0
		self.reinforced_clicks = []
		self.setReinforcedClicks()	
		self.aco_finished = False if self.group == 2 or self.group == 3 else True

		# reseting the mouse
		if self.settings['return_click']:
			utils.reset_mouse_position(self)

		# d. auto-play
		if self.test:
			self.auto_play()

	def nextStage(self):
		txt = "| Going to Stage 3 Screen"
		print(txt)

		self.stage = 3
		from IntroStage import IntroStage
		IntroStage(self.master,self,self.main_bg)

	def set_offset(self):
		# - collecting all answers from stage 2
		if self.group == 1:
			self.offset_reinforce = 0
			self.start_static_rounds = np.inf

		elif self.group == 2:
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

		else:
			counter = 0
			with open("./results/"+self.aco_file) as ref_file:
				for line in ref_file:
					counter += 1

			self.offset_reinforce = counter -1
			self.start_static_rounds = np.inf

	#check this function for other blocks (frequency is acumulating )
	def conditionalReinforce(self):
		# checking the reinforcement for group 1 [VR-5]
		if self.group == 1:
			current_click = sum(self.game[-1]['frequency'].values())
			if current_click > self.reinforced_clicks[-1]:
				self.setReinforcedClicks(offset=current_click-1)
				return (current_click in self.reinforced_clicks)
			else:
				return (current_click in self.reinforced_clicks)
		# checking the reinforcement for group 2 [VI (aco)]
		elif self.group == 2:
			time_vector_stage2 = np.cumsum([time.total_seconds() for g in self.game \
				if g['stage'] == self.game[-1]['stage'] for time in g['time2answer'] ])
			time2ans_cum = time_vector_stage2[-1] if len(time_vector_stage2) > 0 else 0
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
		# checking the reinforcement for group 3 [VR (aco)]
		else:
			if sum(self.game[-1]['frequency'].values()) > self.reinforced_clicks[-1]:
				self.setReinforcedClicks(sum(self.game[-1]['frequency'].values()))
				return False
			else:
				return (sum(self.game[-1]['frequency'].values()) in self.reinforced_clicks)

	# THE STAGE METHODS
	def check_stage_end_conditions(self): 
		# if the number of blocks is greather than the min of blocks
		# and the average IRT is less then the IRT threshold, finish the stage
		if self.aco_finished:
			if self.number_of_blocks() >= self.settings['min_blocks'] \
			and self.averageIRT() < self.settings['IRT_threshold']:
				return True
		# else keep playing
		return False

	def setReinforcedClicks(self,offset=0):
		print("Reinforced CLick")
		self.aco_finished = True
		if self.group == 1: # applying the VR scheme [G1]
			if self.VR5_index == 0:
				self.VR5 = [[5, 1, 3, 2, 4, 1, 17, 7, 1, 10],[7, 1, 4, 1, 2, 10, 5, 3, 17, 1],\
					[2, 1, 17, 5, 1, 7, 1, 3, 10, 4],[1, 2, 1, 4, 7, 17, 10, 3, 5, 1]]

			self.reinforced_clicks = self.VR5[self.VR5_index]
			self.reinforced_clicks = np.array(np.cumsum(self.reinforced_clicks)) # accumulated sum of list VR5 without replacement
			self.reinforced_clicks += offset # addition of offset clicks
			self.VR5_index = (self.VR5_index+1) % 4

		else:
			# a. choosing the file to aco
			print('ACO FILE:',self.aco_file)
			
			# b. defining the reinforcement condition
			if self.group == 2: # applying the VI(aco) scheme [G2]
				counter, negative_offset = 0, 0
				reinf_flags, self.reinforced_clicks = [], []

				# - collecting all answers from stage 5
				with open("./results/"+self.aco_file) as ref_file:
					for line in ref_file:
						if counter != 0:
							reinf_flags.append(line.split(';')[0])
							cum_time = line.split(';')[7]
							self.reinforced_clicks.append(float(cum_time))
						counter += 1

				# - splitting 6 last blocks for reinforce
				time_vector_stage2 = np.cumsum([time.total_seconds() for g in self.game \
					if g['stage'] == self.game[-1]['stage'] for time in g['time2answer'] ])
				time2ans_cum = time_vector_stage2[-1] if len(time_vector_stage2) > 0 else 0
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

			else: # applying the VR(aco) scheme [G3]
				counter, self.reinforced_clicks = 0, []
				print(self.offset_reinforce, sum(self.game[-1]['frequency'].values()),self.aco_file)
				if self.offset_reinforce > 60 and sum(self.game[-1]['frequency'].values()) > 60:
					with open("./results/"+self.aco_file) as ref_file:
						for line in ref_file:
							reinf_flag = line.split(';')[0]
							if counter > (self.offset_reinforce-60) and reinf_flag == 'SIM':
								self.reinforced_clicks.append(counter - (self.offset_reinforce-59) + offset)
							counter += 1
				else:
					with open("./results/"+self.aco_file) as ref_file:
						for line in ref_file:
							reinf_flag = line.split(';')[0]
							if counter != 0 and reinf_flag == 'SIM':
								self.reinforced_clicks.append(counter + offset)
							counter += 1
				print(self.reinforced_clicks)
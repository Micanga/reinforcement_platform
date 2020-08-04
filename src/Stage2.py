import numpy as np
import os
import random
import re
import tkinter
from tkinter import *

import log
import utils

from Screen import Screen

class Stage2(Screen):
	
	def __init__(self, master, prev_sc, main_bg):
		self.AUTO = True
		
		# 1. Initializing the necessary variables
		# a. GUI variables
		super().__init__(master, prev_sc, main_bg,screen_name='Stage 2')
		self.init_variables()

		# b. reinforce vectors
		self.VR5 = [5, 1, 3, 1, 2, 10, 1, 4, 7, 17]
		
		# 2. creating the result file
		log.create_file(self.nickname,self.group,self.stage,self.start_time)

		# a. interface components
		self.createButtons(self.center_h, self.center_w, self.radius)
		utils.ableButtonsAndMouse(self)

		# b. points counter
		self.createPointCounter()

		# c. sound effects
		self.load_sfx()

		self.reinforced_clicks = []
		self.reinforce_index = 0
		self.setReinforcedClicks()
		
		# d. auto-play
		if self.AUTO:
			self.auto_play()

	def nextStage(self):
		txt = "| Going to Stage 3 Screen"
		print(txt)

		self.stage = 3
		from IntroStage import IntroStage
		IntroStage(self.master,self,self.main_bg)

	#check this function for other blocks (frequency is acumulating )
	def conditionalReinforce(self):
		# checking the reinforcement for group 1 [VR-5]
		if self.group == 1:
			current_click = sum(self.game[-1]['frequency'].values())
			if current_click > self.reinforced_clicks[-1]:
				self.setReinforcedClicks(offset=current_click)
				return False
			else:
				return (current_click in self.reinforced_clicks)
		# checking the reinforcement for group 2 [VI (aco)]
		elif self.group == 2:
			time2ans_cum = np.cumsum([time.total_seconds() for g in self.game if g['stage'] == self.game[-1]['stage'] for time in g['time2answer'] ] )[-1]
			if self.reinforce_index > len(self.reinforced_clicks) - 1 or\
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
		# checking the reinforcement for group 3 [VR (aco)]
		else:
			if sum(self.game[-1]['frequency'].values()) > self.reinforced_clicks[-1]:
				self.setReinforcedClicks(sum(self.game[-1]['frequency'].values()))
				return False
			else:
				return any(sum(self.game[-1]['frequency'].values()) == self.reinforced_clicks)

	# THE STAGE METHODS
	def check_stage_end_conditions(self): 
		# if the number of blocks is greather than the min of blocks
		# and the average IRT is less then the IRT threshold, finish the stage
		if self.number_of_blocks() >= self.settings['min_blocks']\
		and self.averageIRT() < self.settings['IRT_threshold']:
			return True
		# else keep playing
		return False

	def setReinforcedClicks(self,offset=0):
		print("Reinforced CLick")
		if self.group == 1: # applying the VR scheme [G1]
			self.reinforced_clicks = random.sample(self.VR5,5) # five numbers of list VR5 without replacement
			self.reinforced_clicks = np.array(np.cumsum(self.reinforced_clicks)) # accumulated sum of list VR5 without replacement
			self.reinforced_clicks += offset # addition of offset clicks

		else:
			# a. choosing the file to aco
			print('ACO FILE:',self.aco_file)
			
			# b. defining the reinforcement condition
			if self.group == 2: # applying the VI(aco) scheme [G2]
				counter, self.reinforced_clicks = 0, []
				with open("./results/"+self.aco_file) as ref_file:
					for line in ref_file:
						reinf_flag = line.split(';')[0]
						cum_time = line.split(';')[7]
						if counter != 0 and reinf_flag == 'SIM':
							self.reinforced_clicks.append(float(cum_time) + offset)
						counter += 1

			else: # applying the VR(aco) scheme [G3]
				counter, self.reinforced_clicks = 0, []
				with open("./results/"+self.aco_file) as ref_file:
					for line in ref_file:
						reinf_flag = line.split(';')[0]
						if counter != 0 and reinf_flag == 'SIM':
							self.reinforced_clicks.append(counter + offset)
						counter += 1
		print(self.reinforced_clicks)
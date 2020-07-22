import numpy as np
import os
import random
import re
import tkinter
from tkinter import *
from utils import *

from Screen import Screen

class Stage2(Screen):
	def __init__(self, master, prev_sc, main_bg):
		self.AUTO = True
		
		# 1. Initializing the necessary variables
		# a. common variables
		super().__init__(master, prev_sc, main_bg,screen_name='Stage 1')
		self.init_variables()
		self.load_sfx()

		# b. reinforce vectors
		self.VR5 = [1, 1, 1, 2, 3, 4, 5, 7, 10, 17]
		self.VR20 = [1, 3, 6, 9, 12, 16, 21, 28, 38, 66]

		# c. interface components
		self.createButtons(self.center_h, self.center_w, self.radius)
		self.createPointCounter()
		self.setReinforcedClicks()

	#check this function for other blocks (frequency is acumulating )
	def conditionalReinforce(self):
		current_click = sum(self.game[-1]['frequency'].values())
		if current_click > self.reinforced_clicks[-1]:
			self.setReinforcedClicks(offset=current_click)
			return False
		else:
			return (current_click in self.reinforced_clicks)

	# THE STAGE METHODS
	def check_stage_end_conditions(self): 
		# if the number of blocks is greather than the min of blocks
		# and the average IRT is less then the IRT threshold, finish the stage
		if self.number_of_blocks() >= self.settings['min_blocks']\
		and self.averageIRT() < self.settings['IRT_threshold']:
			print(self.game)
			return True
		# else keep playing
		return False

	def setReinforcedClicks(self,offset=0):
		if self.group == 1: # applying the VR scheme [G1]
			self.reinforced_clicks = random.sample(self.VR5,5) # five numbers of list VR5 without replacement
			self.reinforced_clicks = np.array(np.cumsum(self.reinforced_clicks)) # accumulated sum of list VR5 without replacement
			self.reinforced_clicks += offset # addition of offset clicks

		else:
			# a. choosing the file to aco
			if self.settings['choose_aco']:
				aco_file = tkinter.filedialog.askopenfilename(initialdir = "./results/")
			else:
				result_files = os.listdir("./results/")
				selected_files = [filename for filename in result_files if re.search("_G"+str(self.group-1)+"_F2_",filename) is not None]
				aco_file = random.choice(selected_files)
			
			exit(1)
			# b. defining the reinforcement condition
			if self.group == 2: # applying the VI(aco) scheme [G2]
				self.reinforced_clicks = []
			else: # applying the VR(aco) scheme [G3]
				self.reinforced_clicks = []


	def fadeNextStage(self):
		txt = "| Going to Stage 3 Screen"
		print(txt)

		# Nickname Screen
		self.stage = 3
		from IntroStage import IntroStage
		IntroStage(self.master,self,self.main_bg)
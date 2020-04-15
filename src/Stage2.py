import tkinter
from tkinter import *
from utils import *
from Screen import Screen
import numpy as np

MIN_BLOCOS = 3


class Stage2(Screen):
	def __init__(self, master, prev_sc, main_bg):
		self.AUTO = True
		
		super().__init__(master, prev_sc, main_bg)

		self.VR5 = [1, 1, 1, 2, 3, 4, 5, 7, 10, 17]
		self.VR20 = [1, 1, 1, 2, 3, 4, 5, 7, 10, 17]

		self.load_sfx()
		self.update_variables()

		self.createButtons(self.center_h, self.center_w, self.radius)
		self.createPointCounter()
		self.setReinforcedClicks()

	#check this function for other blocks (frequency is acumulating )
	def conditionalReinforce(self):
		print("This is conditionalReforce of Stage2")
		return (sum(self.game[-1]['frequency'].values()) in self.reinforced_clicks)


		# THE STAGE METHODS
	def check_stage_end_conditions(self): 

		# MIN BLOCKS + 2 -> first object in array is a standard and the last has added by replay
		# len(self.game[-1]['reinforced']) == 0 means that you just started a new block
		if len(self.game) >= MIN_BLOCOS+2 and len(self.game[-1]['reinforced']) == 0: 

			for i in self.game:
				print(i)

			firstId = len(self.game) - MIN_BLOCOS - 1 
			lastId = len(self.game) - 1 # the last block added but NOT USED TO MAKE MEAN

			time2ReinforcedAnswer = [] # array with all the time

			for i in  range (firstId,lastId):
				idAnswerReinforced = [j for j, val in enumerate(self.game[i]['reinforced']) if (val == True)] 

				for j in  idAnswerReinforced:
					time2ReinforcedAnswer.append(self.game[i]['time2answer'][j])
					

			
		return False
		#self.averageIRT()

	def setReinforcedClicks(self):
		self.reinforced_clicks = random.sample(self.VR5,5) # five numbers of list VR5 without replacement
		print("|selectedVR5  "+ str(self.reinforced_clicks)  + "	 |")
		self.reinforced_clicks = np.cumsum(self.reinforced_clicks) 
		print("|reinforcedVR5 "+ str(self.reinforced_clicks)  + "   |") # accumulated sum of list VR5 without replacement
		
	


       
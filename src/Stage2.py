import tkinter
from tkinter import *
from utils import *
from StageScreen import StageScreen
import numpy as np

class Stage2(StageScreen):
	def __init__(self, master, prev_sc, main_bg):
		super().__init__(master, prev_sc, main_bg)

		self.reinforced_clicks = random.sample(self.VR5,5)
		print(self.reinforced_clicks) # five numbers of list VR5 without replacement
		self.reinforced_clicks = np.cumsum(self.reinforced_clicks) # accumulated sum of list VR5 without replacement
		print(self.reinforced_clicks)

	def conditionalReforce(self):
		print("This is conditionalReforce of Stage2")
		return sum(self.game['frequency'].values()) in self.reinforced_clicks


       
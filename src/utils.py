# INTERFACE AND SETTINGS
import tkinter
from tkinter import *
from tkinter import font
from tkinter import LEFT, RIGHT, BOTTOM, TOP, NONE
from tkinter import messagebox, filedialog, StringVar
from tkinter.font import Font

from copy import deepcopy
import datetime
import random
import re
import os

ENCODE = 'utf-8'

# GUI
def set_bg(master,main_bg,path):
	from PIL import Image, ImageTk
	image = Image.open(path)
	img_copy = image.copy()

	bg_img = ImageTk.PhotoImage(image)
	sw, sh = master.winfo_screenwidth(), master.winfo_screenheight()
	image = img_copy.resize((sw, sh), Image.ANTIALIAS)
	bg_img = ImageTk.PhotoImage(image)

	main_bg = tkinter.Label(master, image=bg_img)
	main_bg.image= bg_img
	main_bg.place(x=sw/2,y=sh/2,relwidth=1,relheight=1,anchor='center')
	return main_bg

def update_screen(cur_sc,bg_color=[255.0,255.0,255.0]):
	#cur_sc.main_bg.destroy()
	cur_sc.main_bg = tkinter.Label(cur_sc.master, \
	 bg= "#%02x%02x%02x" % (int(bg_color[0]),int(bg_color[1]),int(bg_color[2])))
	cur_sc.main_bg.place(x=0,y=0,relwidth=1,relheight=1)

def ableButtons(buttons):
	#print("| -- enabling the buttons")
	for b in buttons:
		b.configure(state="normal")

def disableButtons(buttons):
	#print("| -- disabing the buttons")
	for b in buttons:
		b.configure(state="disabled")

def disableMouse(cur_sc):
	#print("| -- disabing the mouse")
	cur_sc.master.configure(cursor='none')

def ableMouse(cur_sc):
	#print("| -- enabling the mouse")
	cur_sc.master.configure(cursor='')

def ableButtonsAndMouse(cur_sc):
	ableButtons(cur_sc.buttons)
	cur_sc.master.configure(cursor='')

def disableButtonsAndMouse(cur_sc):
	disableButtons(cur_sc.buttons)
	cur_sc.master.configure(cursor='none')

def reset_mouse_position(cur_sc):
	if cur_sc.settings['game_mode'] == 'Múltipla Escolha':
		cur_sc.master.event_generate('<Motion>', warp=True,\
		x=cur_sc.center_w, y=cur_sc.center_h)
	else:
		cur_sc.master.event_generate('<Motion>', warp=True,\
		x=cur_sc.sw/2, y=cur_sc.sh/2)

def removeButtons(buttons):
	#print("| -- destroying  the buttons")
	for b in buttons:
		b.destroy()
	buttons = []

def destroyWidgets(widgets):
	#print("| -- destroying  the widgets")
	for w in widgets:
		w.destroy()
	widgets = []

'''
def getPage(master, prev_sc, main_bg, pathNextPage):
	from 
'''
# LOAD
def load_text(fname):
	
	text = ""
	with open('local/default/'+str(fname)+'.txt',encoding=ENCODE) as default_text:
		for line in default_text:
			text += line
	print("| -- default text loaded."+fname)
	return text

# MATH
from math import log2, fabs

def U(ref_freq):
	freq = {}
	for a in freq:
		freq[a] = ref_freq[a]+1

	if sum([freq[f] for f in freq]) < 11:
		return 1.0
		
	number_of_actions = len(freq)
	rf = [RF(seq,freq) for seq in freq]
	return -sum([(rf[i]*log2(rf[i])) for i in range(number_of_actions)])/log2(number_of_actions)

def Threshold(seq,freq,combinations,reinforced):
	return FRP(seq,freq,reinforced)/\
	 sum([FRP(x,freq,reinforced) for x in combinations])

def FRP(seq,freq,reinforced):
	return RF(seq,freq) if not reinforced\
		else RF(seq,freq)*0.95

def RF(seq,freq):
	return freq[seq]/sum([freq[x] for x in freq])

def Stability(game,n):
	time_vector = [game[i-n]['block_time'] for i in range(n)]

	time_var = [(fabs(time_vector[i].total_seconds() - time_vector[i-1].total_seconds())/\
		time_vector[i].total_seconds()) for i in range(len(time_vector))]
	return(time_var)

def ReinfStability(vector, block_len, threshold):
	if len(vector) < (3*int(block_len)):
		return float(threshold)

	reinf = []
	for i in range(0,3):
		reinf.append(sum([vector[j] \
			for j in range(-(3-i)*int(block_len),-(2-i)*int(block_len))]))

	value = [(fabs(reinf[i] - reinf[i-1])/reinf[i]) for i in [0,1,2]]
	check = [(fabs(reinf[i] - reinf[i-1])/reinf[i]) <= threshold for i in [0,1,2]]

	return(check[0] and check[1] and check[2])

# CHECK
def is_int(string):
	if re.match('^\s*[0-9]+\s*$',string) is not None:
		return True
	else:
		return False

def is_float(string):
	if re.match('^\s*[0-9]+.[0-9]+\s*$',string) is not None:
		return True
	else:
		return False
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

# RESULT
def write_rheader(nickname,start_time):
	result_file = open('results/'+nickname+'_'+\
		start_time.strftime("%Y%m%d_%H%M%S")+".csv","w")
	result_file.write(\
		'Fase;'+\
		'Tentativa;'+\
		'Sequencia;'+\
		'Tempo de Resposta;'+\
		'Frequencia;'+\
		'Limiar;'+\
		'Pontuação Atual;'+\
		'Pontuação Acumulada;'+\
		'# Bloco;'+\
		'Tempo do Bloco;'+\
		'Estabilidade na Taxa de Respostas (%);'+\
	 	'Indice U;'+\
	 	'Tentativas Reforçadas (%);'+\
	 	'Acertos de Memoria'+\
	 	'\n')
	result_file.close()

def write_result(index,game,fill=True,memory=False):
	# 2. Saving the results on the result file
	result_file = open('results/'+game.nickname+'_'+\
		game.start_time.strftime("%Y%m%d_%H%M%S")+".csv","a")

	if memory:
		threshold = ''
		u_value = ''
		game.clicks = game.clicks[0:-1]
	else:
		threshold = str(Threshold(game.clicks,game.frequency,game.combinations,True))

		if not fill:
			u_freq = deepcopy(game.total_frequency)
			u_freq[game.clicks] += 1 #frequency calculated later
			u_value = str(U(u_freq))

	if re.match('^4-[a-zA-Z\s]*$',index) is None:
		total_points = int(game.points.get())+int(game.prev_sc.points.get())
	else:
		total_points = int(game.points.get())+int(game.global_points.get())

	result_file.write(\
		index+';'+\
		str(game.repeat)+';'+\
		str(game.clicks)+';'+\
		str((datetime.datetime.now() -\
		 game.round_start_time).total_seconds())+';'+\
		str(game.frequency)+';'+\
		threshold+';'+\
		str(game.points.get())+';'+\
		str(total_points)+';'\
		)

	if fill:
		result_file.write(\
		';'+\
		';'+\
		';'+\
		';'+\
		';')
	else:
		result_file.write(\
		str(len(game.blocks))+';'+\
		str(game.blocks[-1][1])+';'+\
		str(Stability(game.blocks,float(game.settings['stability'])))+';'+\
		u_value+';'+\
		str(sum(game.reinforcement)/len(game.reinforcement))+';')

	if memory:
		result_file.write(\
		str(game.memo_accuracy)+\
		'\n')
	else:
		result_file.write(\
		'\n')

	result_file.close()

# LOAD
def load_settings():
	print("| -- loading settings...        |")
	# 1. Initializing dictionary and checking existent files
	previous_settings = {}
	saved_settings = [name for name in os.listdir('local/settings/')]
	saved_settings.sort()

	# 2. If exists saved files, open it; otherwise, open default.
	if len(saved_settings) > 0:
		with open('local/settings/'+saved_settings[-1]) as prev_file:
			for line in prev_file:
				data = line.split(',')
				previous_settings[data[0]] = data[1][:-1]
			print("| -- custom settings loaded.    |")
	else:
		with open('local/default/settings.csv') as default_settings:
			for line in default_settings:
				data = line.split(',')
				previous_settings[data[0]] = data[1][:-1]
			print("| -- default settings loaded.   |")

	# 3. Returning the settings
	return previous_settings

def load_images(experiment,correct_img=None,answer=None):
	print("| -- loading right and left img |")
	right_image, left_image, right_txt, left_txt = None, None, None, None
	# 1. Loading left image
	saved_left = [name for name in os.listdir('local/left/')]
	saved_left.sort()

	# 2. Loading right image
	saved_right = [name for name in os.listdir('local/right/')]
	saved_right.sort()

	# 3. Experiment Img building
	if experiment == 1:
		if len(saved_left) > 0:
			left_image = tkinter.PhotoImage(file='local/left/'+saved_left[-1])
			print("| -- custom left img loaded.    |")
		else:
			left_image = tkinter.PhotoImage(file='local/default/left.png')
			print("| -- default left img loaded.   |")

		if len(saved_right) > 0:
			right_image = tkinter.PhotoImage(file='local/right/'+saved_right[-1])
			print("| -- custom right imeg loaded.  |")
		else:
			right_image = tkinter.PhotoImage(file='local/default/right.png')
			print("| -- default right img loaded.  |")

	elif experiment == 2:
		# a. defing img seq
		seq, strseq = [], ''
		fakeseq, strfseq = [], ''
		for a in answer:
			if a == 'E':
				strseq += 'E'
				if len(saved_left) > 0:
					seq.append('local/left/'+saved_left[-1])
				else:
					seq.append('local/default/left.png')
			else:
				strseq += 'D'
				if len(saved_right) > 0:
					seq.append('local/right/'+saved_right[-1])
				else:
					seq.append('local/default/right.png')

		strfseq = strseq
		while strfseq == strseq:
			strfseq = ''
			fakeseq = []
			for i in range(len(answer)):
				if random.uniform(0,1) < 0.5:
					strfseq += 'E'
					if len(saved_left) > 0:
						fakeseq.append('local/left/'+saved_left[-1])
					else:
						fakeseq.append('local/default/left.png')
				else:
					strfseq += 'D'
					if len(saved_right) > 0:
						fakeseq.append('local/right/'+saved_right[-1])
					else:
						fakeseq.append('local/default/right.png')


		# b. building correct img
		import sys
		from PIL import Image
		images = [Image.open(i) for i in seq]
		widths, heights = zip(*(i.size for i in images))
		print(images,widths,heights)

		total_width = sum(widths)
		max_height = max(heights)

		new_im = Image.new('RGB', (total_width, max_height),'white')

		x_offset = 0
		for im in images:
			new_im.paste(im, (x_offset,0))
			x_offset += im.size[0]

		new_im.save('local/imgseq/'+strseq+'.png')

		# c. building incorrect img
		images = [Image.open(i) for i in fakeseq]
		widths, heights = zip(*(i.size for i in images))
		print(images,widths,heights)

		total_width = sum(widths)
		max_height = max(heights)

		new_im = Image.new('RGB', (total_width, max_height),'white')

		x_offset = 0
		for im in images:
			new_im.paste(im, (x_offset,0))
			x_offset += im.size[0]

		new_im.save('local/imgseq/'+strfseq+'.png')

		# d. openning imgs
		if correct_img == 'E':
			left_txt = strseq
			left_image = tkinter.PhotoImage(file='local/imgseq/'+strseq+'.png')
			right_image = tkinter.PhotoImage(file='local/imgseq/'+strfseq+'.png')
			right_txt = strfseq
		else:
			left_txt = strfseq
			left_image = tkinter.PhotoImage(file='local/imgseq/'+strfseq+'.png')
			right_image = tkinter.PhotoImage(file='local/imgseq/'+strseq+'.png')
			right_txt = strseq

	elif experiment == 3:
		# a. defing img seq
		seq, strseq = [], ''
		fakeseq, strfseq = [], ''

		ref_answer = []
		for i in range(4):
			ref_answer.append(answer[0][i])
		for i in range(4):
			ref_answer.append(answer[1][i])

		for a in ref_answer:
			if a == 'E':
				strseq += 'E'
				if len(saved_left) > 0:
					seq.append('local/left/'+saved_left[-1])
				else:
					seq.append('local/default/left.png')
			else:
				strseq += 'D'
				if len(saved_right) > 0:
					seq.append('local/right/'+saved_right[-1])
				else:
					seq.append('local/default/right.png')

		strfseq = strseq
		while strfseq == strseq:
			strfseq = ''
			fakeseq = []
			for i in range(8):
				if random.uniform(0,1) < 0.5:
					strfseq += 'E'
					if len(saved_left) > 0:
						fakeseq.append('local/left/'+saved_left[-1])
					else:
						fakeseq.append('local/default/left.png')
				else:
					strfseq += 'D'
					if len(saved_right) > 0:
						fakeseq.append('local/right/'+saved_right[-1])
					else:
						fakeseq.append('local/default/right.png')

		print(ref_answer,seq,fakeseq)
		# b. building correct img
		import sys
		from PIL import Image
		images = [Image.open(i) for i in seq]
		widths, heights = zip(*(i.size for i in images))
		print(images,widths,heights)

		total_width = int(sum(widths)/2)
		max_height = int(2*max(heights))
		print(total_width, max_height)
		new_im = Image.new('RGB', (total_width, max_height),'white')

		x_offset = 0
		y_offset = 0
		for i in range(len(images)):
			if i == 4:
				x_offset = 0
				y_offset += images[i].size[1]
			new_im.paste(images[i], (x_offset,y_offset))
			x_offset += images[i].size[0]

		new_im.save('local/imgseq/'+strseq+'.png')

		# c. building incorrect img
		images = [Image.open(i) for i in fakeseq]
		widths, heights = zip(*(i.size for i in images))
		print(images,widths,heights)

		total_width = int(sum(widths)/2)
		max_height = int(2*max(heights))

		new_im = Image.new('RGB', (total_width, max_height),'white')

		x_offset = 0
		y_offset = 0
		for i in range(len(images)):
			if i == 4:
				x_offset = 0
				y_offset += images[i].size[1]
			new_im.paste(images[i], (x_offset,y_offset))
			x_offset += images[i].size[0]
		new_im.save('local/imgseq/'+strfseq+'.png')

		# d. openning imgs
		if correct_img == 'E':
			left_txt = strseq
			left_image = tkinter.PhotoImage(file='local/imgseq/'+strseq+'.png')
			right_image = tkinter.PhotoImage(file='local/imgseq/'+strfseq+'.png')
			right_txt = strfseq
		else:
			left_txt = strfseq
			left_image = tkinter.PhotoImage(file='local/imgseq/'+strfseq+'.png')
			right_image = tkinter.PhotoImage(file='local/imgseq/'+strseq+'.png')
			right_txt = strseq
	else:
		print(':: experiment number error ::utils::load_images::120+:: exit 1 ::')
		exit(1)

	return left_image,right_image,left_txt,right_txt

def load_joker():
	print("| -- loading joker image...     |")
	# 1. Loading joker image
	saved = [name for name in os.listdir('local/joker/')]
	saved.sort()
	if len(saved) > 0:
		joker_image = tkinter.PhotoImage(file='local/joker/'+saved[-1])
		print("| -- custom joker loaded.       |")
	else:
		joker_image = tkinter.PhotoImage(file='local/default/joker.png')
		print("| -- default joker loaded.      |")

	return joker_image, 'JOKER', 'JOKER'

def load_text(stage):
	print("| -- loading text...            |")
	text = ""
	saved_texts = [name for name in os.listdir('local/texts/stage'+str(stage)+'/')]
	saved_texts.sort()
	if len(saved_texts) > 0:
		with open('local/texts/stage'+str(stage)+'/'+saved_texts[-1],encoding='latin-1') as prev_file:
			for line in prev_file:
				text += line[:-1]
		print("| -- custom text loaded.        |")
	else:
		with open('local/default/stage'+str(stage)+'.txt',encoding='latin-1') as default_text:
			for line in default_text:
				text += line[:-1]
		print("| -- default text loaded.       |")

	return text

def reset_play1(master, prev_sc, main_bg):
	from Play1 import Play1
	Play1(master,prev_sc,main_bg)

def reset_play2(master, prev_sc, main_bg):
	from Play2 import Play2
	Play2(master,prev_sc,main_bg)
	
def reset_play3(master, prev_sc, main_bg):
	from Play3 import Play3
	Play3(master,prev_sc,main_bg)

def shuffleStages():
	stages = []
	possibilities = [[2,3,4],[3,2,4],[3,4,2]]
	shuffle_idx = [0,1,2]

	for i in range(0,10):
		# reseting idx list
		if len(shuffle_idx) == 0:
			shuffle_idx = [0,1,2]

		# sampling an idx
		if len(shuffle_idx) == 1:
			idx = shuffle_idx[0]
		else:
			idx = random.sample(shuffle_idx,1)[0]

		# saving the stage order
		stages.append(possibilities[idx][0])
		stages.append(possibilities[idx][1])
		stages.append(possibilities[idx][2])

		# removing from the list
		shuffle_idx.remove(idx)

	return stages

# MATH
from math import log2, fabs

def U(freq):
	rf = [RF(seq,freq) for seq in freq]
	return -sum([(rf[i]*log2(rf[i])) for i in range(0,16)])/log2(16)

def Threshold(seq,freq,combinations,reinforced):
	return FRP(seq,freq,reinforced)/\
	 sum([FRP(x,freq,reinforced) for x in combinations])

def FRP(seq,freq,reinforced):
	return RF(seq,freq) if not reinforced\
		else RF(seq,freq)*0.95

def RF(seq,freq):
	return freq[seq]/sum([freq[x] for x in freq])

def Stability(vector,threshold):
	if len(vector) < 3:
		return 1

	time = [vector[i][1] for i in [-3,-2,-1]]
	check = [(fabs(time[i] - time[i-1])/time[i]) <= threshold for i in [0,1,2]]

	return(check[0] and check[1] and check[2])

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
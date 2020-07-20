import sys
from utils import *
import numpy as np

def create_file(nickname,group,stage,start_time):
	filename = nickname+'_G'+str(group)+'_F'+str(stage)+\
		'_'+start_time.strftime("%d-%m-%Y_%Hh%Mm%Ss")
	write_header(filename)

def write_header(filename):
	result_file = open('results/'+filename+".csv","w")
	result_file.write(\
	 	'Indice U'+\
		'Frequencia Absoluta;'+\
		'Frequencia Percentual;'+\
		'Proporção de Alternacoes;'+\
		'Tempo para Resposta;'+\
		'Taxa de Respostas;'+\
		'Desvio Padrao da Taxa de Respostas;'+\
		'\n')
	result_file.close()

def write_round(game,nickname,group,stage,start_time):
	filename = nickname+'_G'+str(group)+'_F'+str(stage)+\
		'_'+start_time.strftime("%d-%m-%Y_%Hh%Mm%Ss")
	result_file = open('results/'+filename+".csv","a")

	# setting the variables
	index_U = str(U(game[-1]['frequency']))
	abs_freq = str(game[-1]['frequency'])

	percent_freq = {}
	for action in game[-1]['frequency']:
		percent_freq[action] = game[-1]['frequency'][action] /  sum([game[-1]['frequency'][a] for a in game[-1]['frequency'] ])
	percent_freq = str(percent_freq)

	change_prop = str('VERIFICAR MEDIDA')
	time2ans = str(game[-1]['time2answer'][-1])
	
	answer_rate = str(sum([game[-1]['frequency'][a] for a in game[-1]['frequency']])/\
		(sum([time.total_seconds() for time in game[-1]['time2answer']])/60.0))
	
	#dev_time2ans += r['time2answer'].total_seconds()
	#dev_time2ans = str(np.sqrt((sum((game[-1]['time2answer']/60) - float(mean_time2ans))**2)/len(game[-1]['time2answer'])))
	dev_time2ans = str(0.0)

	# writting
	result_file.write(\
		index_U + ';' +\
		abs_freq + ';' + \
		percent_freq + ';' + \
		change_prop + \
		time2ans + ';' +\
		answer_rate + ';' +\
		dev_time2ans + ';' +\
		'\n')

	result_file.close()

def calculate_total_points(game):
	total_points = 0
	for g in game:
		total_points += int(g['points'])
	return total_points

def calculate_reinforce_percent(game):
	reinforced = 0
	total_actions = len(game[-1]['reinforced'])
	for r in game[-1]['reinforced']:
		if r == True:
			reinforced += 1
	return 100*float(reinforced)/float(total_actions)
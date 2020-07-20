import sys
from utils import *

def create_file(nickname,group,stage,start_time):
	filename = nickname+'_G'+str(group)+'_F'+str(stage)+\
		'_'+start_time.strftime("%d-%m-%Y_%Hh%Mm%Ss")
	write_header(filename)

def write_header(filename):
	result_file = open('results/'+filename+".csv","w")
	result_file.write(\
	 	'# Grupo'+\
		'# Fase;'+\
		'Acao;'+\
		'Tempo de Resposta;'+\
		'Reinforco;'+\
		'Frequencia;'+\
		'Pontuação Atual;'+\
		'Pontuação Acumulada;'+\
		'# Bloco;'+\
		'Tempo do Bloco;'+\
	 	'Tentativas Reforçadas (%);'+\
		'Estabilidade na Taxa de Respostas (%);'+\
	 	'Indice U'+\
	 	'\n')
	result_file.close()

def write_round(game,nickname,group,stage,start_time):
	filename = nickname+'_G'+str(group)+'_F'+str(stage)+\
		'_'+start_time.strftime("%d-%m-%Y_%Hh%Mm%Ss")
	result_file = open_file('results/'+filename+".csv","a")

	result_file.write(\
		str(game[-1]['group']) + ';' +\
		str(game[-1]['stage']) + ';' +\
		str(game[-1]['answer'][-1]) + ';' +\
		str(game[-1]['time2answer'][-1]) + ';' +\
		str(game[-1]['reinforced'][-1]) + ';' + \
		str(game[-1]['frequency']) + ';' + \
		str(game[-1]['points']) + ';' + \
		str(calculate_total_points(game)) + ';' + \
		';' + \
		';' + \
		';' + \
		';' + \
		';' + \
		'\n'
	)

	result_file.close()

def write_result(game,nickname,group,stage,start_time):
	filename = nickname+'_G'+str(group)+'_F'+str(stage)+\
		'_'+start_time.strftime("%d-%m-%Y_%Hh%Mm%Ss")
	result_file = open('resultszz'+filename+".csv","a")

	result_file.write(\
		str(game[-1]['group']) + ';' +\
		str(game[-1]['stage']) + ';' +\
		str(game[-1]['answer'][-1]) + ';' +\
		str(game[-1]['time2answer'][-1]) + ';' +\
		str(game[-1]['reinforced'][-1]) + ';' + \
		str(game[-1]['frequency']) + ';' + \
		str(game[-1]['points']) + ';' + \
		str(calculate_total_points(game)) + ';' + \
		str(len(game) - 1) + ';' + \
		str(game[-1]['block_time']) + ';' + \
		str(calculate_reinforce_percent(game)) + ';')

	if len(game) >= 3 + 1:
		result_file.write(\
			str(Stability(game,3)) + ';' + \
			str(U(game[-1]['frequency'])) + ';' + \
			'\n'
		)
	else:
		result_file.write(\
			';' + \
			';' + \
			'\n'
		)

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
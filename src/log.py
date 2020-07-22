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
		'Reforço Positivo?'+\
		'Acao'+\
	 	'Indice U'+\
		'Frequencia Absoluta;'+\
		'Frequencia Percentual;'+\
		'Proporção de Alternacoes;'+\
		'Tempo para Resposta;'+\
		'Tempo para Resposta Acumulado;'+\
		'Taxa de Respostas;'+\
		'Desvio Padrao da Taxa de Respostas;'+\
		'ITR medio;'+\
		'IMR;'+\
		'IMR (desvio padrao);'+\
		'NRR;'+\
		'NRR (desvio padrao)'+\
		'pALTref;'+\
		'pALTresp;'+\
		'DFRO;'+\
		'DFRO Percentual;'+\
		'QMR;'+\
		'QMN'+\
	'\n')
	result_file.close()

def write_round(game,nickname,group,stage,start_time):
	filename = nickname+'_G'+str(group)+'_F'+str(stage)+\
		'_'+start_time.strftime("%d-%m-%Y_%Hh%Mm%Ss")
	result_file = open('results/'+filename+".csv","a")

	# setting the variables
	reinforced = 'SIM' if game[-1]['reinforced'][-1] else 'NAO'
	action = str(game[-1]['answer'][-1])
	index_U = str(U(game[-1]['frequency']))
	abs_freq = str(game[-1]['frequency'])

	percent_freq = {}
	total_answers = sum([game[-1]['frequency'][a] for a in game[-1]['frequency']])
	for a in game[-1]['frequency']:
		percent_freq[a] = game[-1]['frequency'][a] / total_answers
	percent_freq = str(percent_freq)

	change_prop = str('VERIFICAR MEDIDA')

	time2ans = str(game[-1]['time2answer'][-1])
	time2ans_cum = str(np.cumsum([time.total_seconds() for time in game[-1]['time2answer']])[-1])
	total_time = sum([time.total_seconds() for time in game[-1]['time2answer']])/60.0

	answer_rate = str(total_answers/total_time)
	mean_time2ans = (total_time/total_answers)
	dev_time2ans = 0.0
	for time in game[-1]['time2answer']:
		dev_time2ans += ((time.total_seconds()/60.0) - mean_time2ans)**2
	dev_time2ans =  str((dev_time2ans)/len(game[-1]['time2answer']))


	last_reinforce, imr_array, imr = 0, [], 0
	for i in range(len(game[-1]['reinforced'])):
		if game[-1]['reinforced'][i] == True:
			imr_array.append(sum([float(time.total_seconds()/60.0) for time in game[-1]['time2answer'][last_reinforce:i+1]]))
			imr += imr_array[-1]
			last_reinforce = i+1
	imr = '' if game[-1]['reinforced'].count(True) == 0 else str(imr/float(game[-1]['reinforced'].count(True)))

	imr_std = str(np.std(imr_array))

	nrr = '' if game[-1]['reinforced'].count(True) == 0 else str(len(game[-1]['reinforced'])/float(game[-1]['reinforced'].count(True)))
	nrr_std = str(np.std(game[-1]['reinforced']))

	ALTref = [1 if game[-1]['reinforced'][i] == True and i > 0 and game[-1]['answer'][i] != game[-1]['answer'][i-1] else 0 for i in range(len(game[-1]['reinforced']))]
	ALTref = sum(ALTref)
	pALTref = '' if game[-1]['reinforced'].count(True) == 0 else  str(ALTref/float(game[-1]['reinforced'].count(True)))

	ALT_count = [1 if i > 0 and game[-1]['answer'][i] != game[-1]['answer'][i-1] else 0 for i in range(len(game[-1]['reinforced']))]
	ALT_count = sum(ALT_count)
	pALTresp = '' if ALT_count == 0 else  str(ALTref/ALT_count)

	DFRO, pDFRO = {}, {}
	for a in game[-1]['frequency']:
		DFRO[a] = 0.0
	
	for i in range(len(game[-1]['reinforced'])):
		DFRO[game[-1]['answer'][i]] += 1 if game[-1]['reinforced'][i] == True else 0

	for a in game[-1]['frequency']:
		pDFRO[a] = 0 if game[-1]['reinforced'].count(True) == 0 else DFRO[a]/game[-1]['reinforced'].count(True)

	# writting
	result_file.write(\
		str(reinforced) + ';' +\
		action + ';' +\
		index_U + ';' +\
		abs_freq + ';' + \
		percent_freq + ';' + \
		change_prop + ';' +\
		time2ans + ';' +\
		time2ans_cum + ';' +\
		answer_rate + ';' +\
		dev_time2ans + ';' +\
		str(1/float(answer_rate)) + ';' +\
		imr + ';' +\
		imr_std + ';' +\
		nrr + ';' +\
		nrr_std + ';' +\
		pALTref + ';' +\
		pALTresp + ';' +\
		str(DFRO) + ';' +\
		str(pDFRO) + ';' +\
		'QMR;'+\
		'QMN'+\
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
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
		'Reforço Positivo?;'+\
		'Acao;'+\
	 	'Indice U;'+\
		'Frequencia Absoluta;'+\
		'Frequencia Percentual;'+\
		'Proporcao de Alternacoes;'+\
		'Tempo para Resposta (s);'+\
		'Tempo para Resposta Acumulado (s);'+\
		'Taxa de Respostas (por minuto);'+\
		'Desvio Padrao da Taxa de Respostas;'+\
		'ITR medio;'+\
		'Intervalos sem reforço (consecutivos);'+\
		'IMR (médio);'+\
		'IMR (desvio padrao);'+\
		'NRR (médio);'+\
		'NRR (desvio padrao);'+\
		'pALTref;'+\
		'pALTresp;'+\
		'DFRO;'+\
		'DFRO Percentual;'+\
		'QMR;'+\
		'QMN'+\
	'\n')
	result_file.close()

def getAllBlocks(game,group,stage):
        blocks = []
        for i in range(len(game)):
            if game[i]['group'] == group and game[i]['stage'] == stage:
                blocks.append(i)
        return blocks

def write_round(game,nickname,group,stage,start_time):
	filename = nickname+'_G'+str(group)+'_F'+str(stage)+\
		'_'+start_time.strftime("%d-%m-%Y_%Hh%Mm%Ss")

	# support variables
	stage_ids = getAllBlocks(game,group,stage)
	total_answers = sum([game[-1]['frequency'][a] for a in game[-1]['frequency']])
	total_time_min = sum([time.total_seconds() for i in stage_ids for time in game[i]['time2answer'] ])/60.0

	actions_ts  = [game[i]['answer'][j]      for i in stage_ids for j in range(len(game[i]['answer']))]
	reinf_ts    = [game[i]['reinforced'][j]  for i in stage_ids for j in range(len(game[i]['reinforced']))]
	time2ans_ts = [game[i]['time2answer'][j] for i in stage_ids for j in range(len(game[i]['time2answer']))]

	total_alts = sum([1 if actions_ts[i] != actions_ts[i-1] else 0 for i in range(1,len(actions_ts))])
	total_reinf_alts = sum([1 if actions_ts[i] != actions_ts[i-1] and reinf_ts[i] else 0 for i in range(1,len(actions_ts))])

	last_reinf, imr_array = 0, []
	for i in range(len(reinf_ts)):
		if reinf_ts[i]:
			imr_array.append(sum([float(time.total_seconds()/60.0) for time in time2ans_ts[last_reinforce:i+1]]))
			last_reinforce = i+1
	
	total_reinf_actions = sum(reinf_ts)

	line_count,ansrate_array = 0, []	
	with open('results/'+filename+".csv","r") as result_file:
		for line in result_file:
			if line_count != 0:
				data = line.split(';')
				ansrate_array.append(float(data[8]))
			line_count += 1

	# log variables
	#'Reforço Positivo?;'+\
	reinforced = 'SIM' if game[-1]['reinforced'][-1] else 'NAO'
	#'Acao;'+\
	action = str(game[-1]['answer'][-1])
	#'Indice U;'+\
	index_U = str(U(game[-1]['frequency']))
	#'Frequencia Absoluta;'+\
	abs_freq = str(game[-1]['frequency'])
	#'Frequencia Percentual;'+\
	percent_freq = {}
	for a in game[-1]['frequency']:
		percent_freq[a] = game[-1]['frequency'][a] / total_answers
	percent_freq = str(percent_freq)
	#'Proporção de Alternacoes;'+\
	change_prop = '' if total_answers == 0 else str(float(total_alts)/float(total_answers))
	#'Tempo para Resposta (s);'+\
	time2ans = str(game[-1]['time2answer'][-1].total_seconds())
	#'Tempo para Resposta Acumulado (s);'+\
	time2ans_cum = str(np.cumsum([time.total_seconds() for i in stage_ids for time in game[i]['time2answer'] ] )[-1])
	#'Taxa de Respostas (por minuto);'+\
	answer_rate = str(total_answers/float(total_time_min))
	#'Desvio Padrao da Taxa de Respostas;'+\
	ansrate_array.append(float(answer_rate))
	dev_ansrate =  str(np.std(ansrate_array))
	#'ITR medio;'+\
	itr = str(1/float(answer_rate))
		
	i, isr = -1, 0
	while reinf_ts[i] == False:
		isr += 1
		i   -= 1

	#'IMR;'+\
	imr = '' if total_reinf_actions == 0 else str(sum(imr_array)/float(total_reinf_actions))
	#'IMR (desvio padrao);'+\
	imr_std = str(np.std(imr_array))
	#'NRR;'+\
	nrr = '' if total_reinf_actions == 0 else str(total_answers/float(total_reinf_actions))
	#'NRR (desvio padrao);'+\
	nrr_std = str(np.std(reinf_ts))
	#'pALTref;'+\
	pALTref = '' if total_reinf_actions == 0 else  str(int(total_reinf_alts)/float(total_reinf_actions))
	#'pALTresp;'+\
	pALTresp = '' if total_alts == 0 else  str(int(total_reinf_alts)/float(total_alts))
	#'DFRO e DFRO Percentual;'+\
	DFRO, pDFRO = {}, {}
	for a in game[-1]['frequency']:
		DFRO[a] = 0.0
	
	for i in stage_ids:
		for j in range(len(game[i]['answer'])):
			DFRO[game[i]['answer'][j]] += 1 if game[i]['reinforced'][j] == True else 0

	for a in game[-1]['frequency']:
		pDFRO[a] = 0 if total_reinf_actions == 0 else DFRO[a]/float(total_reinf_actions)
	#'QMR e QMN'+\
	QMR, QMN, last_click = {}, {}, {}
	for a in game[-1]['frequency']:
		QMR[a] = []
		QMN[a] = []
		last_click[a] = -1

	answer_seq = []
	for i in stage_ids:
		for j in range(len(game[i]['answer'])):
			answer_seq.append((game[i]['answer'][j],(game[i]['reinforced'][j])))
	
	for i in range(len(answer_seq)):
		a = answer_seq[i][0]
		r = answer_seq[i][1]

		if last_click[a] != -1:
			if r:
				QMR[a].append(i-last_click[a])
			else:
				QMN[a].append(i-last_click[a])
		last_click[a] = i

	for a in game[-1]['frequency']:
		QMR[a] = np.mean(QMR[a])
		QMN[a] = np.mean(QMN[a])
	QMR = str(QMR)
	QMN = str(QMN)

	# writting
	result_file = open('results/'+filename+".csv","a")
	result_file.write(\
		reinforced + ';' +\
		action + ';' +\
		index_U + ';' +\
		abs_freq + ';' + \
		percent_freq + ';' + \
		change_prop + ';' +\
		time2ans + ';' +\
		time2ans_cum + ';' +\
		answer_rate + ';' +\
		dev_ansrate + ';' +\
		itr + ';' +\
		str(isr) + ';' +\
		imr + ';' +\
		imr_std + ';' +\
		nrr + ';' +\
		nrr_std + ';' +\
		pALTref + ';' +\
		pALTresp + ';' +\
		str(DFRO) + ';' +\
		str(pDFRO) + ';' +\
		QMR + ';' +\
		QMN +\
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
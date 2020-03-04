def write_header(nickname,start_time):
	result_file = open('results/'+nickname+'_'+\
		start_time.strftime("%Y%m%d_%H%M%S")+".csv","w")
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
	 	'Indice U;'+\
	 	'\n')
	result_file.close()

def write_round(game,filename):
	result_file = open('results/'+filename+".csv","a")

	result_file.write(\
		str(game[-1]['group']) + ';' +\
		str(game[-1]['stage']) + ';' +\
		str(game[-1]['answer'][-1]) + ';' +\
		str(game[-1]['time2answer'][-1]) + ';' +\
		str(game[-1]['reinforce'][-1]) + ';' + \
		str(game[-1]['frequency']) + ';' + \
		str(game[-1]['points'][-1]) + ';' + \
		str(game[-1]['total_points'][1]) + ';' + \
		';' + \
		';' + \
		';' + \
		';' + \
		';' + \
		'\n'
	)

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
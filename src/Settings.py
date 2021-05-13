# Imports
from MyCommons import *
from Screen import Screen
from utils import is_int, is_float, disableButtons

class Settings(Screen):

	def __init__(self, master, prev_sc, main_bg):
		# 1. Initializing the necessary variables
		super().__init__(master, prev_sc, main_bg,'bg/settings.png','Settings')
		print(self.settings)

		# 2. Setting the screen buttons and widgets
		#======================================================
		# SETTINGS BUTTONS
		#======================================================
		# a. actions_per_block button
		self.apb_label, self.apb_entry = \
			self.create_setting_field('Ações por bloco:',self.sw/4,self.sh/7)
		self.apb_entry.insert(END, str(self.settings['actions_per_block']))
		self.widgets.append(self.apb_label)
		self.buttons.append(self.apb_entry)

		# b. min_blocks button
		self.minb_label, self.minb_entry = \
			self.create_setting_field('Minimo de Blocos por Fase:',self.sw/4,2*self.sh/7)
		self.minb_entry.insert(END, str(self.settings['min_blocks']))
		self.widgets.append(self.minb_label)
		self.buttons.append(self.minb_entry)

		# c. max_blocks button
		self.maxb_label, self.maxb_entry = \
			self.create_setting_field('Máximo de Blocos por Fase:',self.sw/4,3*self.sh/7)
		self.maxb_entry.insert(END, str(self.settings['max_blocks']))
		self.widgets.append(self.maxb_label)
		self.buttons.append(self.maxb_entry)

		# d. IRT_threshold button
		self.irt_label, self.irt_entry = \
			self.create_setting_field('Limiar IRT:',self.sw/4,4*self.sh/7)
		self.irt_entry.insert(END, str(self.settings['IRT_threshold']))
		self.widgets.append(self.irt_label)
		self.buttons.append(self.irt_entry)

		# e. return click
		self.check_label, self.check_button, self.check_var = \
			self.create_setting_field('Deseja habilitar clique de retorno?',3*self.sw/4,self.sh/7,type_='check')
		self.check_var.set(self.settings['return_click'])
		self.check_button.var = self.check_var
		self.widgets.append(self.check_label)
		self.buttons.append(self.check_button)

		# f. enable file selection (for aco) button
		self.aco_label, self.aco_button, self.aco_var = \
			self.create_setting_field('Deseja selecionar o arquivo de ACO?',3*self.sw/4,2*self.sh/7,type_='check')
		self.aco_var.set(self.settings['choose_aco'])
		self.aco_button.var = self.aco_var
		self.widgets.append(self.aco_label)
		self.buttons.append(self.aco_button)

		
		# f. enable file selection (for aco) button
		self.fade_label, self.fade_button, self.fade_var = \
			self.create_setting_field('Habilitar tela de início de fase?',3*self.sw/4,3*self.sh/7,type_='check')
		self.fade_var.set(self.settings['fade_flag'])
		self.fade_button.var = self.fade_var
		self.widgets.append(self.fade_label)
		self.buttons.append(self.fade_button)

		# g. game mode selection
		self.game_mode_label, self.game_mode_buttons, self.game_mode_var = \
			self.create_setting_field('Qual modo de jogo deseja iniciar?',3*self.sw/4,4*self.sh/7,type_='switch',
										opt_args=['Múltipla Escolha','Posição Radial'])
		self.game_mode_var.set(self.settings['game_mode'])
		self.widgets.append(self.game_mode_label)
		for button in self.game_mode_buttons:
			self.buttons.append(button)

		#======================================================
		# SAVE AND BACK BUTTON
		#======================================================
		self.save_button = \
			create_button(self.master,'SALVAR',self.save_func,\
				8*self.sw/10,5*self.sh/6,size=18)
		self.buttons.append(self.save_button)

		self.back_button = \
			create_button(self.master,'VOLTAR',self.goToMenu,\
				2*self.sw/10,5*self.sh/6,size=18)
		self.buttons.append(self.back_button)

	def create_setting_field(self,text,x,y,type_='entry',opt_args=None):
		# 1. Creating Entry Label
		print("| -- creating labels nickname	|")
		label = tkinter.Label(self.master, bg="#%02x%02x%02x" % (255, 255, 255),justify='left',\
			fg = 'black', text=text, font=Font(family='Helvetica', size=20))
		label.place(x=x,y=y,anchor='center')

		# 2. Creating the Entry
		if type_ == 'entry':
			entry = tkinter.Entry(self.master, fg = 'black', font = Font(family='Helvetica', size=20),\
										bg = "#%02x%02x%02x" % (255, 255, 255), insertbackground = 'black',\
										highlightcolor = "#%02x%02x%02x" % (180,180,180),\
										 highlightbackground= "#%02x%02x%02x" % (50,50,50),\
										bd=2, width = 33, relief="solid", justify='center')
			entry.place(x = x, y = y+50,anchor='center')
			
			return label,entry

		elif type_ == 'check':
			check_var = tkinter.IntVar()
			tkimage_off = tkinter.PhotoImage(file='local/default/off_icon.png')
			tkimage_on = tkinter.PhotoImage(file='local/default/on_icon.png')
			entry = tkinter.Checkbutton(self.master, image=tkimage_off, compound='center',background='white',\
			 highlightcolor = 'white', highlightbackground= 'white', var=check_var,highlightthickness=-1,\
			 selectimage=tkimage_on,relief='flat',overrelief='flat',offrelief='flat',bd=-1,padx=-1,pady=-1,indicatoron=False)
			entry.image = tkimage_off
			entry.selectimage = tkimage_on
			entry.place(x = x, y = y+60,anchor='center')

			return label,entry, check_var

		elif type_ == 'switch':
			switch_variable = tkinter.StringVar(value=opt_args[0])
			buttons = []
			for option in opt_args:
				buttons.append(tkinter.Radiobutton(self.master, text=option, variable=switch_variable, selectcolor="#%02x%02x%02x" % (0, 180, 0),
					indicatoron=False, value=option, width=18, fg = 'black', font = Font(family='Helvetica', size=20), borderwidth = 8,\
					bg = "#%02x%02x%02x" % (180, 180, 180), relief='raised'))
			for i in range(len(buttons)):
				buttons[i].place(x = x, y = y+((i+1)*60),anchor='center')

			return label, buttons, switch_variable
		else:
			exit(1)

	def save_func(self):
		# action per block check
		if not is_int(self.apb_entry.get()):
			self.errorPopUp('Valor para \"Ações por bloco\" inválido.\n'+\
					'O valor deve ser um número inteiro,\n maior que zero e não vazio.\n')
			return None

		if not int(self.apb_entry.get()) > 0:
			self.errorPopUp('Valor para \"Ações por bloco\" inválido.\n'+\
					'O valor deve ser um número inteiro,\n maior que zero e não vazio.\n')
			return None
		
		# min blocks check
		if not is_int(self.minb_entry.get()):
			self.errorPopUp('Valor para \"Mínimo de Bloco por Fase\" inválido.\n'+\
					'O valor deve ser um número inteiro,\n maior que zero e não vazio.\n')
			return None

		if not int(self.minb_entry.get()) > 0:
			self.errorPopUp('Valor para \"Mínimo de Bloco por Fase\" inválido.\n'+\
					'O valor deve ser um número inteiro,\n maior que zero e não vazio.\n')
			return None

		# max blocks check
		if not is_int(self.maxb_entry.get()):
			self.errorPopUp('Valor para \"Máximo de Bloco por Fase\" inválido.\n'+\
					'O valor deve ser um número inteiro,\n maior que zero e não vazio.\n')
			return None

		if not int(self.maxb_entry.get()) > 0:
			self.errorPopUp('Valor para \"Máximo de Bloco por Fase\" inválido.\n'+\
					'O valor deve ser um número inteiro,\n maior que zero e não vazio.\n')
			return None

		# irt check
		if not is_float(self.irt_entry.get()):
			self.errorPopUp('Valor para \"Limiar IRT\" inválido.\n'+\
					'O valor deve ser um número decimal,\n entre 0 e 1 e não vazio.\n')
			return None

		if not float(self.irt_entry.get()) >= 0\
		or not float(self.irt_entry.get()) <= 1:
			self.errorPopUp('Valor para \"Limiar IRT\" inválido.\n'+\
					'O valor deve ser um número decimal, entre 0 e 1\n e não vazio.\n')
			return None

		self.settings['actions_per_block'] = int(self.apb_entry.get())
		self.settings['min_blocks'] = int(self.minb_entry.get())
		self.settings['max_blocks'] = int(self.maxb_entry.get())
		self.settings['IRT_threshold'] = float(self.irt_entry.get())
		self.settings['return_click'] = self.check_var.get()
		self.settings['choose_aco'] = self.aco_var.get()
		self.settings['fade_flag'] = self.fade_var.get()
		self.settings['game_mode'] = self.game_mode_var.get()
		
		self.goToMenu()


	def errorPopUp(self,text):
		disableButtons(self.buttons)
		myPopUp(self,text)

	def ableButtons(self):
		print("| -- enabling the buttons	   |")
		for b in self.buttons:
			b.configure(state="normal")
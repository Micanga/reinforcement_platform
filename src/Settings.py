# Imports
from MyCommons import *
from Screen import Screen
from utils import is_int, is_float, disableButtons

class Settings(Screen):

	def __init__(self, master, prev_sc, main_bg):
		# 1. Initializing the necessary variables
		# a. initializing the screen
		super().__init__(master, prev_sc, main_bg,'bg/settings.png')

		# b. log text
		self.start_log = 		"---------------------------------\n" + \
								"| LOG STAGE 1 PLAY SCREEN	   |\n" + \
								"---------------------------------"
		self.createb_txt =		"|--- creating buttons		   |"
		self.timeout_txt = 		"| Time Out					  |"
		self.finish_txt = 		"| Stage Finished				|"
		print(self.start_log)

		# 2. Setting the screen buttons and widgets
		# a. actions_per_block button
		self.apb_label, self.apb_entry = \
			self.create_setting_field('Ações por bloco:',self.sw/2,self.sh/6)
		self.apb_entry.insert(END, str(self.settings['actions_per_block']))
		self.widgets.append(self.apb_label)
		self.buttons.append(self.apb_entry)

		# b. min_blocks button
		self.minb_label, self.minb_entry = \
			self.create_setting_field('Minimo de Blocos por Fase:',self.sw/2,2*self.sh/6)
		self.minb_entry.insert(END, str(self.settings['min_blocks']))
		self.widgets.append(self.minb_label)
		self.buttons.append(self.minb_entry)

		# c. max_blocks button
		self.maxb_label, self.maxb_entry = \
			self.create_setting_field('Máximo de Blocos por Fase:',self.sw/2,3*self.sh/6)
		self.maxb_entry.insert(END, str(self.settings['max_blocks']))
		self.widgets.append(self.maxb_label)
		self.buttons.append(self.maxb_entry)

		# d. IRT_threshold button
		self.irt_label, self.irt_entry = \
			self.create_setting_field('Limiar IRT:',self.sw/2,4*self.sh/6)
		self.irt_entry.insert(END, str(self.settings['IRT_threshold']))
		self.widgets.append(self.irt_label)
		self.buttons.append(self.irt_entry)

		# e. save button
		self.save_button = \
			create_button(self.master,'SALVAR',self.save_func,\
				8*self.sw/10,5*self.sh/6,size=18)
		self.buttons.append(self.save_button)

		# f. back button
		self.back_button = \
			create_button(self.master,'VOLTAR',self.goToMenu,\
				2*self.sw/10,5*self.sh/6,size=18)
		self.buttons.append(self.back_button)

	def create_setting_field(self,text,x,y):
		# 1. Creating Entry Label
		print("| -- creating labels nickname	|")
		label = tkinter.Label(self.master, bg="#%02x%02x%02x" % (255, 255, 255),justify='left',\
			fg = 'black', text=text, font=Font(family='Helvetica', size=20))
		label.place(x=x,y=y,anchor='center')

		# 2. Creating the Entry
		entry = tkinter.Entry(self.master, fg = 'black', font = Font(family='Helvetica', size=20),\
									bg = "#%02x%02x%02x" % (255, 255, 255), insertbackground = 'black',\
									highlightcolor = "#%02x%02x%02x" % (180,180,180), highlightbackground= "#%02x%02x%02x" % (50,50,50),\
									bd=0, width = 33, justify='center')
		entry.place(x = x, y = y+50,anchor='center')

		# 3. Returning
		return label,entry

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
		
		self.goToMenu()


	def errorPopUp(self,text):
		disableButtons(self.buttons)
		myPopUp(self,text)

	def ableButtons(self):
		print("| -- enabling the buttons	   |")
		for b in self.buttons:
			b.configure(state="normal")
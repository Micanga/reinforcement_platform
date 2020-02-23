# Interface Imports
import tkinter
from tkinter import *
from tkinter import font
from tkinter import LEFT, RIGHT, BOTTOM, TOP, NONE
from tkinter import messagebox, filedialog, StringVar
from tkinter.font import Font

# Utils Imports
import datetime
import os
import re
import time
from MyCommons import *
import utils

class Settings:

	def __init__(self, master, prev_sc, main_bg):
		self.buttons, self.widgets = [], []

		# 1. Initilising GUI Components
		# a. screen and log components
		self.master = master
		self.main_bg = main_bg
		self.main_bg.destroy()
		sw, sh = self.master.winfo_screenwidth(), self.master.winfo_screenheight()

		self.start_log = 		"---------------------------------\n" + \
								"| LOG SETTINGS SCREEN           |\n" + \
								"---------------------------------"
		self.disabled_txt = 	"| -- disabling the buttons      |"
		self.abled_txt = 		"| -- enabling the buttons       |"
		self.destroy_txt = 		"| -- destroying the screen      |"
		self.back_txt = 		"| Back Action Button Pressed    |"
		self.save_txt =		 	"| Save Action Button Pressed    |"
		print(self.start_log)

		# b. setting background
		utils.set_bg(self.master,self.main_bg,'bg/settings.png')

		# c. title and settings background
		self.settings_bg = tkinter.Frame(self.master,width=int(4*sw/5),height=int(4*sh/5),bg="#%02x%02x%02x" % (220, 220, 220))
		self.settings_bg.pack_propagate(0) # Stops child widgets of label_frame from resizing it
		self.settings_bg.place(x=sw/10,y=sh/10)

		self.settings_label = tkinter.Label(master, bg="#%02x%02x%02x" % (220, 220, 220),\
									 fg = 'black', text='CONFIGURAÇÕES:',\
									 font=Font(family='Helvetica', size=24, weight='bold'))
		self.settings_label.place(x=sw/10,y=sh/10)

		# . Back Button
		self.back_button = Button(master, anchor = 'center', compound = 'center', 
									text = 'VOLTAR',font = Font(family='Helvetica', size=18, weight='bold'),
									bg = "#%02x%02x%02x" % (30, 30, 30), fg = 'white',
									command = self.back_button_click,
									highlightthickness = 0, 
									bd = 0, padx=0,pady=0,height=2,width=13)
		self.back_button.place(x = sw/10, y = 8*sh/10)
		self.buttons.append(self.back_button)
		self.widgets.append(self.back_button)

		# . Save Button
		self.save_button = Button(master, anchor = 'center', compound = 'center', 
									text = 'SALVAR',font = Font(family='Helvetica', size=18, weight='bold'),
									bg = "#%02x%02x%02x" % (30, 30, 30), fg = 'white',
									command = self.save_button_click,
									highlightthickness = 0, 
									bd = 0, padx=0,pady=0,height=2,width=13)
		self.save_button.place(x = 9*sw/10, y = 8*sh/10,anchor='ne')
		self.buttons.append(self.save_button)
		self.widgets.append(self.save_button)

		# 3. Loading the previous settings and images

	def back_button_click(self):
		print(self.back_txt)

		self.destroyWidgets()

		from Menu import Menu
		Menu(self.master,self,self.main_bg)

	def save_button_click(self):
		print(self.save_txt)

		# 1. Checking the entries
		if not self.intCheck(self.max_time_entry.get(),'Tempo Máximo','90'):
			return None
		elif not self.floatCheck(self.iri_entry.get(),'IRI','0.5'):
			return None
		elif not self.floatCheck(self.stability_entry.get(),'Estabilidade','0.2','1'):
			return None
		elif not self.floatCheck(self.threshold_entry.get(),'Limiar','0.2','1'):
			return None
		elif not self.floatCheck(self.preinf_entry.get(),'Acurácia','1.0','1'):
			return None
		elif not self.floatCheck(self.screen_entry.get(),'ITI','1.5'):
			return None
		elif not self.intCheck(self.block_entry1.get(),'número Mínimo de Blocos (Fase 1)','10'):
			return None
		elif not self.intCheck(self.block_entry2.get(),'número Mínimo de Blocos (Fase 2)','10'):
			return None
		elif not self.intCheck(self.block_entry3.get(),'número Mínimo de Blocos (Fase 3)','15'):
			return None
		elif not self.intCheck(self.points_entry.get(),'Pontos por Acerto','10'):
			return None
		elif not self.floatCheck(self.u_entry.get(),'Limiar U','1.0','1'):
			return None
		if not self.intCheck(self.min_memo_entry.get(),'Mínimo de Acertos em Memória','80'):
			return None

		# 2. Saving Settings
		time = datetime.datetime.now()
		save_file = open('local/settings/'+time.strftime("%Y%m%d_%H%M%S")+".csv","w")
		save_file.write('max_time,'+self.max_time_entry.get()+"\n")
		save_file.write('iri,'+self.iri_entry.get()+"\n")
		save_file.write('stability,'+self.stability_entry.get()+"\n")
		save_file.write('threshold,'+self.threshold_entry.get()+"\n")
		save_file.write('preinf,'+self.preinf_entry.get()+"\n")
		save_file.write('iti,'+self.screen_entry.get()+"\n")
		save_file.write('blocks1,'+self.block_entry1.get()+"\n")
		save_file.write('blocks2,'+self.block_entry2.get()+"\n")
		save_file.write('blocks3,'+self.block_entry3.get()+"\n")
		save_file.write('points,'+self.points_entry.get()+"\n")
		save_file.write('u_threshold,'+self.u_entry.get()+"\n")
		save_file.write('min_memo,'+self.min_memo_entry.get()+"\n")
		save_file.close()

		# 3. Destroying screen
		self.destroyWidgets()

		# 4. Returning to Menu
		from Menu import Menu
		Menu(self.master,self,self.main_bg)

	def intCheck(self,value,name,eg='10'):
		if re.match("^$",value) is not None:
			self.disableButtons()
			myPopUp(self,'Valor para '+name+' Vazio!\nPor favor, informe um valor válido.')
			return False
		if re.match("^\d+$",value) is None:
			self.disableButtons()
			myPopUp(self,'Valor para '+name+' Inválido!\nPor favor, entre com um valor decimal válido.\nExemplo: '+eg)
			return False
		return True

	def floatCheck(self,value,name,eg='0.5',max_value=99999):
		if re.match("^$",value) is not None:
			self.disableButtons()
			myPopUp(self,'Valor para '+name+' Vazio!\nPor favor, informe um valor válido.')
			return False
		if re.match("^\d*[.]{0,1}\d*$",value) is None:
			self.disableButtons()
			myPopUp(self,'Valor para '+name+' Inválido!\nPor favor, entre com um valor decimal válido.\nExemplo: '+str(eg))
			return False
		if float(value) > float(max_value): 
			self.disableButtons()
			myPopUp(self,'Valor para '+name+' Inválido!\nPor favor, entre com um valor entre 0 e '+str(max_value)+'.')
			return False
		return True

	def ableButtons(self):
		print(self.abled_txt)
		self.back_button.configure(state="normal")
		self.save_button.configure(state="normal")

	def disableButtons(self):
		print(self.disabled_txt)
		self.back_button.configure(state="disabled")
		self.save_button.configure(state="disabled")

	def destroyWidgets(self):
		print(self.destroy_txt)
		self.settings_bg.destroy()
		self.settings_label.destroy() 

		self.back_button.destroy()
		self.save_button.destroy()
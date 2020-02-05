import tkinter
from tkinter import *
from MyCommons import *
from utils import *

class NickName:

    def __init__(self, master, prev_sc, main_bg):

        self.master = master
        self.main_bg = main_bg
		#self.main_bg.destroy()
        self.sw, self.sh = self.master.winfo_screenwidth(), self.master.winfo_screenheight()

        self.start_log = "---------------------------------\n" + \
						 "| NickName Register Screen      |\n" + \
						 "---------------------------------"

        self.start_txt = "| Choose Experiment Screen   |"

        print(self.start_log)   

        self.back_txt = 		"| Back Button Pressed |"

        # 2. Buttons Functions
        self.widgets = []
        self.buttons = []
        self.experiment = "teste 44 "

        self.nickname_label, self.nickname_entry = \
			self.create_label_entry('Digite seu apelido para o experimento '+\
				str(self.experiment)+':',self.sw/2,self.sh/3)

        self.widgets.append(self.nickname_label)

        self.back_button = \
			create_button(self.master,'VOLTAR',self.back_button_click,\
				self.sw/10,5*self.sh/6,size=18)
        
        self.widgets.append(self.back_button)
        self.buttons.append(self.back_button)

        self.start_button = \
			create_button(self.master,'Go',self.start_button_click,\
				self.sw/2,5*self.sh/6,size=18)
        
        self.widgets.append(self.start_button)
        self.buttons.append(self.start_button)
        


    def back_button_click(self):
        print(self.back_txt)
        destroyWidgets(self.widgets)

        from Menu import Menu
        Menu(self.master,self,self.main_bg)      

    def start_button_click(self):

        self.nickname = self.nickname_entry.get()
        print("| Sending Nickname: " + self.nickname + "       |")
        print("| Start Button clicked           |")
        destroyWidgets(self.widgets)

        from ChooseExperiment import ChooseExperiment
        ChooseExperiment(self.master,self,self.main_bg)

    def create_label_entry(self,label_text,x,y):
        # 1. Creating Entry Label
        print("| -- creating labels nickname   |")
        label = tkinter.Label(self.master, bg="#%02x%02x%02x" % (255, 255, 255),justify='left',\
            fg = 'black', text=label_text, font=Font(family='Helvetica', size=20))
        label.place(x=x,y=y,anchor='center')

		# 2. Creating the Entry
        entry = tkinter.Entry(self.master, fg = 'black', font = Font(family='Helvetica', size=20),\
								    bg = "#%02x%02x%02x" % (255, 255, 255), insertbackground = 'black',\
								    highlightcolor = "#%02x%02x%02x" % (180,180,180), highlightbackground= "#%02x%02x%02x" % (50,50,50),\
								    bd=0, width = 33, justify='center')
        entry.place(x = x, y = y+50,anchor='center')

		# 3. Returning
        return label,entry
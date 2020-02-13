import tkinter
from tkinter import *
from MyCommons import *
from utils import *
from Screen import Screen

class NickName(Screen):

    def __init__(self, master, prev_sc, main_bg):

        super().__init__(master, prev_sc, main_bg)
        self.experiment = "Teste 2"

        #label and text inout
        self.nickname_label, self.nickname_entry = \
			self.create_label_entry('Digite seu apelido para o experimento '+\
				str(self.experiment)+':',self.sw/2,self.sh/3)

        self.widgets.append(self.nickname_label)

        #start button
        self.start_button = \
			create_button(self.master,'Go',self.start_button_click,\
				self.sw/2,5*self.sh/6,size=18)

        #back button
        self.back_button = \
			create_button(self.master,'VOLTAR',self.goToMenu,\
				self.sw/10,5*self.sh/6,size=18)
        
    def start_button_click(self):
        if not self.nicknameCheck():
            return None

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

    def nicknameCheck(self):
        if re.match("^$",self.nickname_entry.get()) is not None:
            disableButtons(self.buttons)
            myPopUp(self,'Você precisa de um Apelido!\nPor favor, digite um apelido para você!')
            return False
        if re.match("^[a-zA-Z0-9]+$",self.nickname_entry.get()) is None:
            disableButtons(self.buttons)
            myPopUp(self,'Seu Apelido não pode conter espaços\nou caracteres especiais!\nPor favor, digite um apelido válido!')
            return False
        return True

    def ableButtons(self):
        print("| -- enabling the buttons       |")
        for b in self.buttons:
            b.configure(state="normal")
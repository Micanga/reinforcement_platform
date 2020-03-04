import inspect
import tkinter
from tkinter import *
from utils import *

class Screen:

    def __init__(self, master, prev_sc, main_bg, bg_img=None):
        start = "---------------------------------\n" + \
				"| New Screen                     |\n" + \
				"---------------------------------" 
        print(start)

        # a. setting screen components
        if prev_sc is not None:   
            self.destroyAll(prev_sc)

        self.master = master
        self.main_bg = main_bg
        self.prev_sc = prev_sc
        self.sw, self.sh = self.master.winfo_screenwidth(), self.master.winfo_screenheight()

        # b. setting background
        if bg_img is not None:
            self.main_bg = set_bg(self.master,self.main_bg,bg_img)
        elif self.main_bg is not None:
            self.main_bg.destroy()

        # c. initialising screen variables
        self.widgets = []
        self.buttons = []

        # d. maintaing game main variables
        attributes = [i for i in dir(self.prev_sc) if not inspect.ismethod(i)]

        if 'nickname' in attributes:
            self.nickname = self.prev_sc.nickname
        else:
            self.nickname = None
        if 'start_time' in attributes:
            self.start_time = self.prev_sc.start_time
        else:
            self.start_time = None
        if 'group' in attributes:
            self.group = self.prev_sc.group
        else:
            self.group = None
        if 'stage' in attributes:
            self.stage = self.prev_sc.stage
        else:
            self.stage = None

    def destroyAll(self,prev_sc):
        clean_log = "| Cleaning Last Screen           |"
        print(clean_log)
        
        #destroying everything from the previous screen
        destroyWidgets(prev_sc.widgets)
        removeButtons(prev_sc.buttons)

    def goToStage1(self):
        txt =  "| Going to Stage 1 Screen        |"    
        print(txt)

        #Nickname Screen
        from Stage1 import Stage1
        Stage1(self.master, self, self.main_bg)

    def goToNickName(self):
        txt = 	"| Going to Nickname Screen       |"	
        print(txt)

        #Nickname Screen
        from NickName import NickName
        NickName(self.master, self, self.main_bg)
       
    def goToSettings(self):
        txt = 	"| Going to Settings Screen      |"	
        print(txt)

        from Settings import Settings
        Settings(self.master, self, self.main_bg)

    def goToMenu(self):
        txt = 	"| Going to Menu Screen           |"	
        print(txt)

        from Menu import Menu
        Menu(self.master, self, self.main_bg)
        
    def goToExit(self):
        self.master.destroy()
        
        exit_log = "| Exit Button Pressed            |"
        print(exit_log)
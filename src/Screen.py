import tkinter
from tkinter import *
from utils import *

class Screen:

    def __init__(self, master, prev_sc, main_bg):
        start = "---------------------------------\n" + \
				"| New Screen                     |\n" + \
				"---------------------------------" 

        print(start)

        if prev_sc is not None:   
            self.destroyAll(prev_sc)

        self.master = master
        self.main_bg = main_bg
        self.prev_sc = prev_sc
        self.main_bg.destroy()
        self.sw, self.sh = self.master.winfo_screenwidth(), self.master.winfo_screenheight()

        self.widgets = []
        self.buttons = []

    def destroyAll(self,prev_sc):
        print("| Cleaning Last Screen           |")
        
        #destroying everything from the previous screen
        destroyWidgets(prev_sc.widgets)
        removeButtons(prev_sc.buttons)

    def goToNickName(self):
        settings_txt = 	"| Going to Settings Screen      |"	
        print(settings_txt)
        #Nickname Screen
        from NickName import NickName
        NickName(self.master, self, self.main_bg)
       
    def goToSettings(self):
        settings_txt = 	"| Going to Settings Screen      |"	
        print(settings_txt)
        from Settings import Settings
        Settings(self.master, self, self.main_bg)
        settings_txt = 	"| Settings Button pressed       |"	
        print(settings_txt)

    def goToMenu(self):
        settings_txt = 	"| Going to Menu Screen          |"	
        print(settings_txt)
        from Menu import Menu
        Menu(self.master, self, self.main_bg)
        
    def goToExit(self):
        self.master.destroy()
        exit_log = "| Exit Button Pressed           |"
        print(start_log)
import tkinter
from tkinter import *
from tkinter import font
from tkinter import LEFT, RIGHT, BOTTOM, TOP, NONE
from tkinter import messagebox, filedialog, StringVar
from tkinter.font import Font
import tkinter.scrolledtext as scrolledtext

import datetime
import os
	
def multFunc(*funcs):
    def multFunc(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return multFunc

def disable_event():
	pass

class myPopUp:

	def __init__(self,cur_screen,text):
		# 1. Initializing and configuring
		self.cur_popup = tkinter.Toplevel()
		sw = (self.cur_popup.winfo_screenwidth() - 800)/2
		sh = (self.cur_popup.winfo_screenheight() - 600)/2
		self.cur_popup.configure(bg= "#%02x%02x%02x" % (255, 255, 255))
		self.cur_popup.protocol("WM_DELETE_WINDOW", disable_event)
		self.cur_popup.resizable(width = False,height = False)
		self.cur_popup.geometry("+%d+%d" % (sw+175,sh+100))

		# 2. Writting the text
		self.pop_text = tkinter.Label(self.cur_popup, text = text, fg = 'black',\
											 anchor = 'center', justify='center',
											font = Font(family='Helvetica', size=14, weight='bold'), bg = "#%02x%02x%02x" % (255, 255, 255), 
											borderwidth=0,padx=10,pady=10)
		self.pop_text.grid(row=0, column=0)
		
		# 3. Setting the OK button
		self.ok_button = Button(self.cur_popup, anchor = 'center',
									bg = "#%02x%02x%02x" % (200, 200, 200), fg = 'black', text= 'OK',
									font = Font(family='Helvetica', size=14, weight='bold'),highlightcolor='black',
									command = multFunc(cur_screen.ableButtons,self.cur_popup.destroy),
									highlightthickness = 0, activebackground = "#%02x%02x%02x" % (230, 230, 230),
									bd = 1, padx=5,pady=5,height=1,width=4)
		self.ok_button.grid(row=1, column=0)

		# 4. Settig the Final Space
		self.space = tkinter.Label(self.cur_popup, bg= "#%02x%02x%02x" % (255, 255, 255))
		self.space.grid(row=2,column=0)

class myTextBox:

	def __init__(self,cur_screen,text,stage):
		# 1. Initializing and configuring
		self.cur_popup = tkinter.Toplevel()
		sw = (self.cur_popup.winfo_screenwidth() - 800)/2
		sh = (self.cur_popup.winfo_screenheight() - 600)/2
		self.cur_popup.configure(bg= "#%02x%02x%02x" % (255, 255, 255))
		self.cur_popup.protocol("WM_DELETE_WINDOW", disable_event)
		self.cur_popup.resizable(width = False,height = False)
		self.cur_popup.geometry("+%d+%d" % (sw+175,sh+100))

		# 2. Writting the text
		self.stage = stage
		self.pop_title = tkinter.Label(self.cur_popup, text = text, fg = 'black',\
											 anchor = 'center', justify='center',
											font = Font(family='Helvetica', size=14, weight='bold'), bg = "#%02x%02x%02x" % (255, 255, 255), 
											borderwidth=0,padx=10,pady=10)
		self.pop_title.grid(row=0, column=2)

		# 2. Writting the text
		text = ""
		saved_texts = [name for name in os.listdir('local/texts/stage'+str(stage)+'/')]
		saved_texts.sort()
		print("Saved texts:",saved_texts)
		if len(saved_texts) > 0:
			with open('local/texts/stage'+str(stage)+'/'+saved_texts[-1],encoding='latin-1') as prev_file:
				for line in prev_file:
					text += line[:-1]
		else:
			with open('local/default/stage'+str(stage)+'.txt',encoding='latin-1') as default_text:
				for line in default_text:
					text += line[:-1]

		print('Previous text:',text)

		self.pop_text = scrolledtext.ScrolledText(self.cur_popup, fg = 'black', font = Font(family='Helvetica', size=14),\
									 bg = "#%02x%02x%02x" % (255, 255, 255), insertbackground = 'black',\
									 highlightcolor = "#%02x%02x%02x" % (180,180,180), highlightbackground= "#%02x%02x%02x" % (50,50,50),\
									  bd=0, width =35, height=10, wrap='word')
		self.pop_text.insert('insert',text)
		self.pop_text.grid(row=1, column=1,columnspan=3)
		
		# 4. Setting the OK button
		self.back_button = Button(self.cur_popup, anchor = 'center',
									bg = "#%02x%02x%02x" % (200, 200, 200), fg = 'black', text= 'VOLTAR',
									font = Font(family='Helvetica', size=14, weight='bold'),highlightcolor='black',
									command = multFunc(cur_screen.ableButtons,self.cur_popup.destroy),
									highlightthickness = 0, activebackground = "#%02x%02x%02x" % (230, 230, 230),
									bd = 1, padx=5,pady=5,height=1,width=8)
		self.back_button.grid(row=3, column=1)


		self.save_button = Button(self.cur_popup, anchor = 'center',
									bg = "#%02x%02x%02x" % (200, 200, 200), fg = 'black', text= 'SALVAR',
									font = Font(family='Helvetica', size=14, weight='bold'),highlightcolor='black',
									command = multFunc(cur_screen.ableButtons,self.save_text,self.cur_popup.destroy),
									highlightthickness = 0, activebackground = "#%02x%02x%02x" % (230, 230, 230),
									bd = 1, padx=5,pady=5,height=1,width=8)
		self.save_button.grid(row=3, column=3)

		# 5. Settig the Spaces
		self.space1 = tkinter.Label(self.cur_popup, text="\t", bg= "#%02x%02x%02x" % (255, 255, 255))
		self.space1.grid(row=0,column=0)
		self.space2 = tkinter.Label(self.cur_popup, text="\t", bg= "#%02x%02x%02x" % (255, 255, 255))
		self.space2.grid(row=0,column=4)
		self.space3 = tkinter.Label(self.cur_popup, bg= "#%02x%02x%02x" % (255, 255, 255))
		self.space3.grid(row=2,column=0)
		self.space3 = tkinter.Label(self.cur_popup, bg= "#%02x%02x%02x" % (255, 255, 255))
		self.space3.grid(row=4,column=0)

	def save_text(self):
		time = datetime.datetime.now()
		save_file = open('local/texts/stage'+str(self.stage)+'/'+\
			time.strftime("%Y%m%d_%H%M%S")+".txt","w")
		save_file.write(self.pop_text.get("1.0","end")+"\n")
		save_file.close()

class myReturnMenuPopUp:

	def __init__(self,cur_screen,text):
		# 1. Initializing and configuring
		self.cur_popup = tkinter.Toplevel()
		sw = (self.cur_popup.winfo_screenwidth() - 800)/2
		sh = (self.cur_popup.winfo_screenheight() - 600)/2
		self.cur_popup.configure(bg= "#%02x%02x%02x" % (255, 255, 255))
		self.cur_popup.protocol("WM_DELETE_WINDOW", disable_event)
		self.cur_popup.resizable(width = False,height = False)
		self.cur_popup.geometry("+%d+%d" % (sw+175,sh+100))

		# 2. Writting the text
		self.pop_text = tkinter.Label(self.cur_popup, text = text, fg = 'black',\
											 anchor = 'center', justify='center',
											font = Font(family='Helvetica', size=14, weight='bold'), bg = "#%02x%02x%02x" % (255, 255, 255), 
											borderwidth=0,padx=10,pady=10)
		self.pop_text.grid(row=0, column=0)
		
		# 3. Setting the OK button
		self.ok_button = Button(self.cur_popup, anchor = 'center',
									bg = "#%02x%02x%02x" % (200, 200, 200), fg = 'black', text= 'OK',
									font = Font(family='Helvetica', size=14, weight='bold'),highlightcolor='black',
									command = multFunc(cur_screen.ableButtons, cur_screen.goMenu, self.cur_popup.destroy),
									highlightthickness = 0, activebackground = "#%02x%02x%02x" % (230, 230, 230),
									bd = 1, padx=5,pady=5,height=1,width=4)
		self.ok_button.grid(row=1, column=0)

		# 4. Settig the Final Space
		self.space = tkinter.Label(self.cur_popup, bg= "#%02x%02x%02x" % (255, 255, 255))
		self.space.grid(row=2,column=0)

class myFailPopUp:

	def __init__(self,cur_screen,text):
		# 1. Initializing and configuring
		self.cur_popup = tkinter.Toplevel()
		sw = (self.cur_popup.winfo_screenwidth() - 800)/2
		sh = (self.cur_popup.winfo_screenheight() - 600)/2
		self.cur_popup.configure(bg= "#%02x%02x%02x" % (255, 255, 255))
		self.cur_popup.protocol("WM_DELETE_WINDOW", disable_event)
		self.cur_popup.resizable(width = False,height = False)
		self.cur_popup.geometry("+%d+%d" % (sw+175,sh+100))

		# 2. Writting the text
		self.pop_text = tkinter.Label(self.cur_popup, text = text, fg = 'black',\
											 anchor = 'center', justify='center',
											font = Font(family='Helvetica', size=14, weight='bold'), bg = "#%02x%02x%02x" % (255, 255, 255), 
											borderwidth=0,padx=10,pady=10)
		self.pop_text.grid(row=0, column=0)
		
		# 3. Setting the OK button
		self.ok_button = Button(self.cur_popup, anchor = 'center',
									bg = "#%02x%02x%02x" % (200, 200, 200), fg = 'black', text= 'OK',
									font = Font(family='Helvetica', size=14, weight='bold'),highlightcolor='black',
									command = multFunc(cur_screen.goMenu, self.cur_popup.destroy),
									highlightthickness = 0, activebackground = "#%02x%02x%02x" % (230, 230, 230),
									bd = 1, padx=5,pady=5,height=1,width=4)
		self.ok_button.grid(row=1, column=0)

		# 4. Settig the Final Space
		self.space = tkinter.Label(self.cur_popup, bg= "#%02x%02x%02x" % (255, 255, 255))
		self.space.grid(row=2,column=0)
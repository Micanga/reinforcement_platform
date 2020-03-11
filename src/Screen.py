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
            self.main_bg = set_bg(self.master, self.main_bg, bg_img)
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

    def destroyAll(self, prev_sc):
        clean_log = "| Cleaning Last Screen           |"
        print(clean_log)

        # destroying everything from the previous screen
        destroyWidgets(prev_sc.widgets)
        removeButtons(prev_sc.buttons)

    # Starting a game Screen

    def createButtons(self, center_h, center_w, radius):
                # print(self.createb_txt)
        self.button_1 = CircularButton(self.master, 100, 100,
                                       color=RED, bg=BG_COLOR, command=self.button1_click)
        self.button_1.place(x=center_w-radius,
                            y=center_h,
                            anchor='center')
        self.buttons.append(self.button_1)

        self.button_2 = CircularButton(self.master, 100, 100,
                                       color=RED, bg=BG_COLOR, command=self.button2_click)
        self.button_2.place(x=center_w-radius*cos(pi/7),
                            y=center_h-radius*sin(pi/7),
                            anchor='center')
        self.buttons.append(self.button_2)

        self.button_3 = CircularButton(self.master, 100, 100,
                                       color=RED, bg=BG_COLOR, command=self.button3_click)
        self.button_3.place(x=center_w-radius*cos(2*pi/7),
                            y=center_h-radius*sin(2*pi/7),
                            anchor='center')
        self.buttons.append(self.button_3)

        self.button_4 = CircularButton(self.master, 100, 100,
                                       color=RED, bg=BG_COLOR, command=self.button4_click)
        self.button_4.place(x=center_w-radius*cos(3*pi/7),
                            y=center_h-radius*sin(3*pi/7),
                            anchor='center')
        self.buttons.append(self.button_4)

        self.button_5 = CircularButton(self.master, 100, 100,
                                       color=RED, bg=BG_COLOR, command=self.button5_click)
        self.button_5.place(x=center_w-radius*cos(4*pi/7),
                            y=center_h-radius*sin(4*pi/7),
                            anchor='center')
        self.buttons.append(self.button_5)

        self.button_6 = CircularButton(self.master, 100, 100,
                                       color=RED, bg=BG_COLOR, command=self.button6_click)
        self.button_6.place(x=center_w-radius*cos(5*pi/7),
                            y=center_h-radius*sin(5*pi/7),
                            anchor='center')
        self.buttons.append(self.button_6)

        self.button_7 = CircularButton(self.master, 100, 100,
                                       color=RED, bg=BG_COLOR, command=self.button7_click)
        self.button_7.place(x=center_w-radius*cos(6*pi/7),
                            y=center_h-radius*sin(6*pi/7),
                            anchor='center')
        self.buttons.append(self.button_7)

        self.button_8 = CircularButton(self.master, 100, 100,
                                       color=RED, bg=BG_COLOR, command=self.button8_click)
        self.button_8.place(x=center_w-radius*cos(pi),
                            y=center_h-radius*sin(pi),
                            anchor='center')
        self.buttons.append(self.button_8)

        def button1_click(self):
            print("|--- button 1 click             |")
            self.check_action(1)

        def button2_click(self):
            print("|--- button 2 click             |")
            self.check_action(2)

        def button3_click(self):
            print("|--- button 3 click             |")
            self.check_action(3)

        def button4_click(self):
            print("|--- button 4 click             |")
            self.check_action(4)

        def button5_click(self):
            print("|--- button 5 click             |")
            self.check_action(5)

        def button6_click(self):
            print("|--- button 6 click             |")
            self.check_action(6)

        def button7_click(self):
            print("|--- button 7 click             |")
            self.check_action(7)

        def button8_click(self):
            print("|--- button 8 click             |")
            self.check_action(8)

    def conditionalReforce(self):
        print("This is the standard conditionalReforce")
        return TRUE

    def check_action(self, clicked_button):
        # a. updating game log
        self.game['answer'].append(clicked_button)
        self.game['reinforced'].append(True)
        self.game['time2answer'].append(
            datetime.datetime.now() - self.round_start_time)
        self.game['frequency'][clicked_button] += 1

        # b.reinforcing the action

        print(self.conditionalReforce)

        if self.conditionalReforce():
            removeButtons(self.buttons)
            self.cur_color = np.array(BG_COLOR)
            self.ref_color = np.array(BG_COLOR) - np.array(GREEN)
            self.positive_reinforce_action()
        else:
            print(sum(self.game['frequency'].values()))

    def positive_reinforce_action(self):
        # a. calculating the color fade (to green)
        self.cur_color -= (0.1*self.ref_color)

        # b. changing background color
        self.main_bg.configure(bg="#%02x%02x%02x" %
                               (int(self.cur_color[0]), int(self.cur_color[1]), int(self.cur_color[2])))

        # c. checking the fade stop
        if (self.ref_color[1] >= 0 and int(self.cur_color[1]) > 200)\
                or (self.ref_color[1] < 0 and int(self.cur_color[1]) < 200):
            self.master.after(50, self.positive_reinforce_action)
        else:
            # - setting green bg
            self.main_bg.configure(bg="#%02x%02x%02x" % (0, 200, 0))
            # self.points.set(int(self.points.get())+int(self.settings['points']))
            # self.master.after(int(float(self.settings['iti'])*1000),self.replay)
            self.points.set(int(self.points.get())+10)
            self.master.after(1*1000, self.replay)

    # Going to another Screen

    def goToStage1(self):
        txt = "| Going to Stage 1 Screen        |"
        print(txt)

        # Nickname Screen
        from Stage1 import Stage1
        Stage1(self.master, self, self.main_bg)

    def goToNickName(self):
        txt = "| Going to Nickname Screen       |"
        print(txt)

        # Nickname Screen
        from NickName import NickName
        NickName(self.master, self, self.main_bg)

    def goToSettings(self):
        txt = "| Going to Settings Screen      |"
        print(txt)

        from Settings import Settings
        Settings(self.master, self, self.main_bg)

    def goToMenu(self):
        txt = "| Going to Menu Screen           |"
        print(txt)

        from Menu import Menu
        Menu(self.master, self, self.main_bg)

    def goToExit(self):
        self.master.destroy()

        exit_log = "| Exit Button Pressed            |"
        print(exit_log)

from tkinter import *
from tkinter import ttk

import time

class UI_VideoRender():

    progress_bar_pos = [5,1]

    margin_1_pos = [0,0]
    margin_2_pos = [0,1000]
    margin_3_pos = [2,0]
    margin_4_pos = [4,0]
    margin_5_pos = [6,0]
    margin_6_pos = [8,0]

    UI_window = Widget
    
    def __init__(self, master):
        self.UI_window = master

    def open_main(self):
        self.place_widgets()
        self.create_margins()

    def create_progress_bar(self):
        render_progress = ttk.Progressbar(self.UI_window, orient=HORIZONTAL, length = 1000, mode='determinate')
        return render_progress

    def place_widgets(self):
        self.progress_bar = self.create_progress_bar()
        self.progress_bar.grid(row=self.progress_bar_pos[0], column=self.progress_bar_pos[1])
        self.run_calculations()

    def set_progress_value(self, curr, max):
        progress_perc = int (curr/max * 100)
        self.progress_bar['value'] = progress_perc
        # self.UI_window.update_idletasks()
        time.sleep(0.1)

    def estimate_calc_time(self):
        some_timer_value = 100
        return some_timer_value

    def run_calculations(self):
        timer = self.estimate_calc_time()
        for x in range(timer):
            self.set_progress_value(x, timer)
        return None

    def create_margins(self):
        Label(self.UI_window, text="  ").grid(row=self.margin_1_pos[0], column=self.margin_1_pos[1])
        Label(self.UI_window, text="  ").grid(row=self.margin_2_pos[0], column=self.margin_2_pos[1])
        Label(self.UI_window, text="  ").grid(row=self.margin_3_pos[0], column=self.margin_3_pos[1])
        Label(self.UI_window, text="  ").grid(row=self.margin_4_pos[0], column=self.margin_4_pos[1])
        Label(self.UI_window, text="  ").grid(row=self.margin_5_pos[0], column=self.margin_5_pos[1])
        Label(self.UI_window, text="  ").grid(row=self.margin_6_pos[0], column=self.margin_6_pos[1])
        return None
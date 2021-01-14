from tkinter import *

from UI_Setter import UI_Setter

class UI_MainScreen():
    
    margin_1_pos = [0,0]
    margin_2_pos = [0,1000]
    margin_3_pos = [2,2]
    margin_4_pos = [4,4]
    margin_5_pos = [6,6]
    margin_6_pos = [8,8]
    margin_7_pos = [10,10]

    btn_params = [40, 4, 3]
    disparity_map_btn_pos = [1,1]
    video_render_btn_pos = [3,1]
    point_cloud_btn_pos = [5,1]
    reconstruction_btn_pos = [7,1]
    visualiser_btn_pos = [9,1]
    test_area_btn_pos = [9,1]

    exit_btn_pos = [99,1]

    UI_window = Widget
    
    def __init__(self, master):
        self.UI_window = master

    def open_main(self):
        self.place_widgets()
        self.create_margins()

    def place_widgets(self):
        UI_setter = UI_Setter(self.UI_window)
        Button(self.UI_window, text="Disparity Map", width=self.btn_params[0], height=self.btn_params[1], bd=self.btn_params[2],
        command = lambda: UI_setter.open_disp_map()).grid(row=self.disparity_map_btn_pos[0], column=self.disparity_map_btn_pos[1])
        Button(self.UI_window, text="Stereo Video Render", width=self.btn_params[0], height=self.btn_params[1], bd=self.btn_params[2], state = "disabled",
        command = lambda: UI_setter.open_video_render()).grid(row=self.video_render_btn_pos[0], column=self.video_render_btn_pos[1])
        Button(self.UI_window, text="Point Cloud (Coming Soon)", width=self.btn_params[0], height=self.btn_params[1], bd=self.btn_params[2], state = "disabled",
        command = lambda: UI_setter.open_point_cloud()).grid(row=self.point_cloud_btn_pos[0], column=self.point_cloud_btn_pos[1])
        Button(self.UI_window, text="Reconstruction (Coming Soon)", width=self.btn_params[0], height=self.btn_params[1], bd=self.btn_params[2], state = "disabled",
        command = lambda: UI_setter.open_reconstruction()).grid(row=self.reconstruction_btn_pos[0], column=self.reconstruction_btn_pos[1])
        # Button(self.UI_window, text="Visualiser (Coming Soon)", width=self.btn_params[0], height=self.btn_params[1], bd=self.btn_params[2], state = "disabled",
        # command = lambda: UI_setter.open_visualiser()).grid(row=self.visualiser_btn_pos[0], column=self.visualiser_btn_pos[1])
        Button(self.UI_window, text="Test Area", width=self.btn_params[0], height=self.btn_params[1], bd=self.btn_params[2],
        command = lambda: UI_setter.open_test_area()).grid(row=self.test_area_btn_pos[0], column=self.test_area_btn_pos[1])

        Button(self.UI_window, text="Exit", width=self.btn_params[0], height=self.btn_params[1], bd=self.btn_params[2],
        command = lambda: self._quit()).grid(row=self.exit_btn_pos[0], column=self.exit_btn_pos[1], sticky = S)

    def create_margins(self):
        Label(self.UI_window, text="      ").grid(row=self.margin_1_pos[0], column=self.margin_1_pos[1])
        Label(self.UI_window, text="  ").grid(row=self.margin_2_pos[0], column=self.margin_2_pos[1])
        Label(self.UI_window, text="  ").grid(row=self.margin_3_pos[0], column=self.margin_3_pos[1])
        Label(self.UI_window, text="  ").grid(row=self.margin_4_pos[0], column=self.margin_4_pos[1])
        Label(self.UI_window, text="  ").grid(row=self.margin_5_pos[0], column=self.margin_5_pos[1])
        Label(self.UI_window, text="  ").grid(row=self.margin_6_pos[0], column=self.margin_6_pos[1])
        Label(self.UI_window, text="  ").grid(row=self.margin_7_pos[0], column=self.margin_7_pos[1])
        
    def _quit(self):
        # plt.close('all')
        self.UI_window.quit()
        self.UI_window.destroy()


    
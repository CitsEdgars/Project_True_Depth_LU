from tkinter import *

from UI_DisparityMap import UI_DisparityMap
from UI_Rectification import UI_Rectification
from UI_PointCloud import UI_PointCloud
from UI_Visualizer import UI_Visualizer
from UI_Rconstruction import UI_Reconstruction
from UI_VideoRender import UI_VideoRender
from UI_TestArea import UI_TestArea


class UI_Setter():
    UI_window = Widget

    def __init__(self, master):
        self.UI_window = master

    def reset_UI(self):
        for widget in self.UI_window.winfo_children():
            widget.destroy()

    def open_test_area(self):
        self.reset_UI()
        test_area = UI_TestArea(self.UI_window)
        test_area.open_main()

    def open_rectification(self):
        self.reset_UI()
        rectification = UI_Rectification(self.UI_window)
        rectification.open_main()

    def open_disp_map(self):
        self.reset_UI()
        disp_win = UI_DisparityMap(self.UI_window)
        disp_win.open_main()

    def open_point_cloud(self):
        self.reset_UI()
        pnt_cld = UI_PointCloud(self.UI_window)
        pnt_cld.open_main()
    
    def open_reconstruction(self):
        self.reset_UI()
        reconstruction = UI_Reconstruction(self.UI_window)
        reconstruction.open_main()

    def open_video_render(self):
        self.reset_UI()
        video_render = UI_VideoRender(self.UI_window)
        video_render.open_main()

    def open_visualizer(self):
        self.reset_UI()
        reconstruction = UI_Visualizer(self.UI_window)
        reconstruction.open_main()
from tkinter import *
import numpy.core.multiarray
import cv2

from UI_Manager import UI_Manager
from UI_DisparityMap import UI_DisparityMap


# App properties
GUI_dimensions = "1265x590"
GUI_title = "True Sight"

root = Tk()
GUI_interface = UI_Manager(master = root, size = GUI_dimensions, name = GUI_title)
GUI_interface.position_app(root)
GUI_interface.set_up_menu(root)
GUI_interface.open_main()




# root.resizable(0,0)
root.mainloop()
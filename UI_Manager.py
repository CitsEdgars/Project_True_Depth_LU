from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile, asksaveasfile
from PIL import Image, ImageTk

from FileManager import FileManager
from UI_MainScreen import UI_MainScreen
from UI_Setter import UI_Setter


class UI_Manager():
    UI_window = Widget

    def __init__(self, master, name, size):
        master.title(name)
        master.geometry(size)
        self.UI_window = Frame(master)
        self.UI_window.pack(fill = "both", expand = 1) #initial launch
        
    def place_GUI(self, master):
        windowWidth = master.winfo_reqwidth()
        windowHeight = master.winfo_reqheight()
        positionRight = int(master.winfo_screenwidth()/12 - windowWidth/2) #- 1675  #On the other screen
        positionDown = int(master.winfo_screenheight()/9 - windowHeight/2) + 175
        master.geometry("+{}+{}".format(positionRight, positionDown))

    def position_app(self, master):
        self.place_GUI(master)

    def reset_UI(self):
        for widget in self.UI_window.winfo_children():
            widget.destroy()

    def open_main(self):
        self.reset_UI()
        main = UI_MainScreen(self.UI_window)
        main.open_main()

    def _quit(self, master):
        # plt.close('all')
        master.quit()
        master.destroy()

    def return_dimensions(self, master):
        coordinates_top_left = master.winfo_geometry()
        print("Something has been done.\n")
        print("New size and coordinates: " + coordinates_top_left)

    def set_up_menu(self, master):
        top_menu = Menu(master)
        master.config(menu=top_menu)
        file_menu = Menu(top_menu)
        edit_menu = Menu(top_menu)
        help_menu = Menu(top_menu)
        ui_s = UI_Setter(self.UI_window)
        top_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Main menu", command=lambda: self.open_main())
        file_menu.add_command(label="Disparity map", command=lambda: ui_s.open_disp_map())
        # file_menu.add_command(label="New static sample", command=lambda rt = self.UI_window: self.return_dimensions(rt))
        # file_menu.add_command(label="New motion sample", command=lambda rt = self.UI_window: self.return_dimensions(rt))
        # file_menu.add_command(label="Select motion feed", command=lambda rt = self.UI_window: self.return_dimensions(rt))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=lambda rt = master: self._quit(rt))

        top_menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Edit static sample", command=lambda rt = self.UI_window: self.return_dimensions(rt))
        # edit_menu.add_command(label="Edit motion sample", command=lambda rt = self.UI_window: self.return_dimensions(rt))

        top_menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Instructions", command=lambda rt = self.UI_window: self.return_dimensions(rt))
        help_menu.add_command(label="Check coordinates", command=lambda rt = self.UI_window: self.return_dimensions(rt))
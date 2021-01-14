from tkinter import *
from tkinter import filedialog, ttk
import cv2
from PIL import Image, ImageTk
from fractions import gcd

from FileManager import FileManager
from DisparityManager import DisparityManager

class UI_DisparityMap:
    # dimensions in form of (width,height)
    placeholder_size = [315,480]
    resize_dimensions_UI_pictures = [300,450]
    
    left_im_frame_pos = [0,1]
    right_im_frame_pos = [0,3]
 
    img_frames_frame_pos = [0,1]
    disp_slider_frame_pos = [0,5]
    disp_button_frame_pos = [2,1]

    map_frames_frame_pos = [0,1]
    disp_val_frame_pos = [0,4]
    secondary_btn_frame_pos = [2,1]
    
    left_pic_btn_pos = [0,1]
    right_pic_btn_pos = [0,3]
    load_settings_btn_pos = [0,5]
    save_settings_btn_pos = [0,7]
    calculate_btn_pos = [0,9]

    back_btn_pos = [0,1]
    save_map_btn_pos = [0,3]
    load_map_btn_pos = [0,5]
    load_matrix_btn = [0,7]
    save_depth_btn = [0,9]
    save_rgbd_btn = [0,11]

    btn_margin_1_pos = [0,0]
    btn_margin_2_pos = [0,2]
    btn_margin_3_pos = [0,4]
    btn_margin_4_pos = [0,6]
    btn_margin_5_pos = [0,8]
    btn_margin_6_pos = [0,10]

    margin_1_pos = [0,0]
    margin_2_pos = [0,1000]
    margin_3_pos = [3,2]
    margin_4_pos = [0,2]

    P1_pos = [0,0,1]
    P2_pos = [1,0,1]
    preFilterCap_pos = [2,0,1]
    min_disp_pos = [3,0,1]
    max_disp_pos = [4,0,1]
    block_size_pos = [5,0,1]
    uniquenessRatio_pos = [6,0,1]
    speckleWindowSize_pos = [7,0,1]
    speckleRange_pos = [8,0,1]
    disp12MaxDiff_pos = [9,0,1]

    coord_x_pos = [0,0,1]
    coord_y_pos = [2,0,1]
    disp_val_pos = [4,0,1]
    depth_val_pos = [6,0,1]
    curr_matrix_pos = [8,0,1]

    def __init__(self, master):
        self.UI_window = master
        self.disparity_window = ttk.Notebook(self.UI_window)
        self.disparity_window.pack(pady = 3, padx = 3)
        self.disparity_settings = Frame(self.disparity_window)
        self.disparity_map = Frame(self.disparity_window)
        self.disparity_settings.pack(fill = "both", expand = 1)
        self.disparity_map.pack(fill = "both", expand = 1)
        self.disparity_window.add(self.disparity_settings, text = "  Disparity settings  ")
        self.disparity_window.add(self.disparity_map, text = "  Disparity map results  ")

        self.dm = DisparityManager(0,0,0,0,0,0,0,0,0,-1)      #TO-DO load settings
        self.fm = FileManager()

    def open_main(self):
        self.place_widgets()
        self.create_margins()

    def create_UI_image_frame(self):
        image_frame = Frame(self.disparity_settings, padx = 5, pady = 10)
        self.left_img_frame = LabelFrame(image_frame, text = "Left Channel", width = self.placeholder_size[0], height = self.placeholder_size[1])
        self.right_img_frame = LabelFrame(image_frame, text = "Right Channel", width = self.placeholder_size[0], height = self.placeholder_size[1])
        self.pack_channel_frames()
        return image_frame

    def pack_channel_frames(self):
        self.left_img_frame.grid(row = self.left_im_frame_pos[0], column = self.left_im_frame_pos[1])
        self.right_img_frame.grid(row = self.right_im_frame_pos[0], column = self.right_im_frame_pos[1])
        self.left_img_frame.pack_propagate(False)
        self.right_img_frame.pack_propagate(False)

    def init_sliders(self, master):
        P1_label = Label(master, text="P1: ").grid(row=self.P1_pos[0], column=self.P1_pos[1], sticky=E)
        P2_label = Label(master, text="P2: ").grid(row=self.P2_pos[0], column=self.P2_pos[1], sticky=E)
        preFilterCap_label = Label(master, text="Pre-filter cap: ").grid(row=self.preFilterCap_pos[0], column=self.preFilterCap_pos[1], sticky=E)
        min_disp_label = Label(master, text="Min display: ").grid(row=self.min_disp_pos[0], column=self.min_disp_pos[1], sticky=E)
        max_disp_label = Label(master, text="Max display: ").grid(row=self.max_disp_pos[0], column=self.max_disp_pos[1], sticky=E)
        block_size_label = Label(master, text="Block size: ").grid(row=self.block_size_pos[0], column=self.block_size_pos[1], sticky=E)
        uniquenessRatio_label = Label(master, text="Uniqueness ratio: ").grid(row=self.uniquenessRatio_pos[0], column=self.uniquenessRatio_pos[1], sticky=E)
        speckleWindowSize_label = Label(master, text="Speckle Window size: ").grid(row=self.speckleWindowSize_pos[0], column=self.speckleWindowSize_pos[1], sticky=E)
        speckleRange_label = Label(master, text="Speckle range: ").grid(row=self.speckleRange_pos[0], column=self.speckleRange_pos[1], sticky=E)
        disp12MaxDiff_label = Label(master, text="Display 12 Max difference: ").grid(row=self.disp12MaxDiff_pos[0], column=self.disp12MaxDiff_pos[1], sticky=E)

        self.P1_slider = Scale(master, from_=0, to=10, orient=HORIZONTAL, sliderlength=20, length=400, command=self.dm.update_P1)
        self.P2_slider = Scale(master, resolution = 2, from_=0, to=40, orient=HORIZONTAL, sliderlength=20, length=400, command=self.dm.update_P2)
        self.preFilterCap_slider = Scale(master, from_=0, to=10, orient=HORIZONTAL, sliderlength=20, length=400, command=self.dm.update_preFilterCap)
        self.min_disp_slider = Scale(master, resolution = 2, from_=0, to=64, orient=HORIZONTAL, sliderlength=20, length=400, command=self.dm.update_min_disp)
        self.max_disp_slider = Scale(master, tickinterval = 32, resolution = 2, from_=16, to=408, orient=HORIZONTAL, sliderlength=20, length=400, command=self.dm.update_max_disp)
        self.block_size_slider = Scale(master, resolution = 1, from_=1, to=15, orient=HORIZONTAL, sliderlength=20, length=400, command=self.dm.update_blockSize)
        self.uniquenessRatio_slider = Scale(master, from_=0, to=15, orient=HORIZONTAL, sliderlength=20, length=400, command=self.dm.update_uniquenessRatio)
        self.speckleWindowSize_slider = Scale(master, from_=0, to=200, orient=HORIZONTAL, sliderlength=20, length=400, command=self.dm.update_speckleWindowSize)
        self.speckleRange_slider = Scale(master, from_=0, to=10, orient=HORIZONTAL, sliderlength=20, length=400, command=self.dm.update_speckleRange)
        self.disp12MaxDiff_slider = Scale(master, from_=-1, to=20, orient=HORIZONTAL, sliderlength=20, length=400, command=self.dm.update_disp12MaxDiff)
        
    def update_and_set_sliders(self):
        self.P1_slider.set(self.dm.P1)
        self.P2_slider.set(self.dm.P2)
        self.preFilterCap_slider.set(self.dm.preFilterCap)
        self.min_disp_slider.set(self.dm.min_disp)
        self.max_disp_slider.set(self.dm.max_disp)
        self.block_size_slider.set(self.dm.blockSize)
        self.uniquenessRatio_slider.set(self.dm.uniquenessRatio)
        self.speckleWindowSize_slider.set(self.dm.speckleWindowSize)
        self.speckleRange_slider.set(self.dm.speckleRange)
        self.disp12MaxDiff_slider.set(self.dm.disp12MaxDiff)

        self.P1_slider.grid(row=self.P1_pos[0], column=self.P1_pos[2], sticky=W)
        self.P2_slider.grid(row=self.P2_pos[0], column=self.P2_pos[2], sticky=W)
        self.preFilterCap_slider.grid(row=self.preFilterCap_pos[0], column=self.preFilterCap_pos[2], sticky=W)
        self.min_disp_slider.grid(row=self.min_disp_pos[0], column=self.min_disp_pos[2], sticky=W)
        self.max_disp_slider.grid(row=self.max_disp_pos[0], column=self.max_disp_pos[2], sticky=W)
        self.block_size_slider.grid(row=self.block_size_pos[0], column=self.block_size_pos[2], sticky=W)
        self.uniquenessRatio_slider.grid(row=self.uniquenessRatio_pos[0], column=self.uniquenessRatio_pos[2], sticky=W)
        self.speckleWindowSize_slider.grid(row=self.speckleWindowSize_pos[0], column=self.speckleWindowSize_pos[2], sticky=W)
        self.speckleRange_slider.grid(row=self.speckleRange_pos[0], column=self.speckleRange_pos[2], sticky=W)
        self.disp12MaxDiff_slider.grid(row=self.disp12MaxDiff_pos[0], column=self.disp12MaxDiff_pos[2], sticky=W)

    def pack_sliders(self):
        slider_frame = Frame(self.disparity_settings) #TO-DO
        self.init_sliders(slider_frame)
        self.update_and_set_sliders()
        return slider_frame

    def init_buttons(self, master):
        button_padding = [30,5]
        self.left_picture_load = Button(master, text="Load left channel", command=lambda channel = "left": self.open_channel(channel), padx=button_padding[0], pady=button_padding[1])
        self.right_picture_load = Button(master, text="Load right channel", command=lambda channel = "right": self.open_channel(channel), padx=button_padding[0], pady=button_padding[1])
        self.load_disp_settings = Button(master, text="Load disparity settings", command=lambda: self.load_settings(), padx=button_padding[0], pady=button_padding[1])
        self.save_disp_settings = Button(master, text="Save disparity settings", command=lambda: self.save_settings(), padx=button_padding[0], pady=button_padding[1])
        self.calculate = Button(master, text="Calculate ->", command=lambda x = 1: self.calculate_disp_map(x), padx=button_padding[0], pady=button_padding[1])
    
    def set_button_panel(self, master):
        self.left_picture_load.grid(row = self.left_pic_btn_pos[0], column = self.left_pic_btn_pos[1], columnspan = 1)
        self.right_picture_load.grid(row = self.right_pic_btn_pos[0], column = self.right_pic_btn_pos[1], columnspan = 1)
        self.load_disp_settings.grid(row = self.load_settings_btn_pos[0], column = self.load_settings_btn_pos[1], columnspan = 1)
        self.save_disp_settings.grid(row = self.save_settings_btn_pos[0], column = self.save_settings_btn_pos[1], columnspan = 1)
        self.calculate.grid(row = self.calculate_btn_pos[0], column = self.calculate_btn_pos[1], columnspan = 1)
        Label(master, text="                                 ").grid(row=self.btn_margin_1_pos[0], column=self.btn_margin_1_pos[1])
        Label(master, text="                                     ").grid(row=self.btn_margin_2_pos[0], column=self.btn_margin_2_pos[1])
        Label(master, text="                                        ").grid(row=self.btn_margin_3_pos[0], column=self.btn_margin_3_pos[1])
        Label(master, text="  ").grid(row=self.btn_margin_4_pos[0], column=self.btn_margin_4_pos[1])
        Label(master, text="  ").grid(row=self.btn_margin_5_pos[0], column=self.btn_margin_5_pos[1])
        Label(master, text="  ").grid(row=self.btn_margin_6_pos[0], column=self.btn_margin_6_pos[1])
     
    def pack_buttons(self):
        button_frame = Frame(self.disparity_settings) #TO-DO
        self.init_buttons(button_frame)
        self.set_button_panel(button_frame)
        return button_frame

    def init_disp_map(self):
        disp_map_frame = Frame(self.disparity_map, padx = 5, pady = 10)
        self.disp_map_frame = LabelFrame(disp_map_frame, text = "Disparity Map", width = self.placeholder_size[0], height = self.placeholder_size[1])
        self.depth_map_frame = LabelFrame(disp_map_frame, text = "Corresponding Depth Map", width = self.placeholder_size[0], height = self.placeholder_size[1])
        Label(disp_map_frame, text="        ").grid(row=self.margin_4_pos[0], column=self.margin_4_pos[1])
        self.pack_map_frames()
        return disp_map_frame

    def pack_map_frames(self):
        self.disp_map_frame.grid(row = self.left_im_frame_pos[0], column = self.left_im_frame_pos[1])
        self.depth_map_frame.grid(row = self.right_im_frame_pos[0], column = self.right_im_frame_pos[1])
        self.disp_map_frame.pack_propagate(False)
        self.depth_map_frame.pack_propagate(False)

    def init_disp_depth_values(self):
        disp_values_frame = Frame(self.disparity_map, padx = 5, pady = 10)
        label_font_settings = ("", 9, "")
        pad_x = 10
        pad_y = 10
        Label(disp_values_frame, text="Coordinate X: ", font = label_font_settings, pady = pad_y).grid(row=self.coord_x_pos[0], column=self.coord_x_pos[1], sticky=E)
        Label(disp_values_frame, text="Coordinate Y: ", font = label_font_settings, pady = pad_y).grid(row=self.coord_y_pos[0], column=self.coord_y_pos[1], sticky=E)
        Label(disp_values_frame, text="Disparity value: ", font = label_font_settings, pady = pad_y).grid(row=self.disp_val_pos[0], column=self.disp_val_pos[1], sticky=E)
        Label(disp_values_frame, text="Depth value: ", font = label_font_settings, pady = pad_y).grid(row=self.depth_val_pos[0], column=self.depth_val_pos[1], sticky=E)
        Label(disp_values_frame, text="Currently using: ", font = label_font_settings, pady = pad_y).grid(row=self.curr_matrix_pos[0], column=self.curr_matrix_pos[1], sticky=E)
        Label(disp_values_frame, text="  ", font = label_font_settings, padx = pad_x, pady = pad_y).grid(row=self.coord_x_pos[0]+1, column=self.coord_x_pos[1]+1)
        Label(disp_values_frame, text="  ", font = label_font_settings, padx = pad_x, pady = pad_y).grid(row=self.coord_y_pos[0]+1, column=self.coord_y_pos[1]+1)
        Label(disp_values_frame, text="  ", font = label_font_settings, padx = pad_x, pady = pad_y).grid(row=self.disp_val_pos[0]+1, column=self.disp_val_pos[1]+1)
        Label(disp_values_frame, text="  ", font = label_font_settings, padx = pad_x, pady = pad_y).grid(row=self.depth_val_pos[0]+1, column=self.depth_val_pos[1]+1)
        Label(disp_values_frame, text="  ", font = label_font_settings, padx = pad_x, pady = pad_y).grid(row=self.curr_matrix_pos[0]+1, column=self.curr_matrix_pos[1]+1)
        self.coord_x = Label(disp_values_frame, text="N/A", font = label_font_settings, padx = pad_x, pady = pad_y)
        self.coord_y = Label(disp_values_frame, text="N/A", font = label_font_settings, padx = pad_x, pady = pad_y)
        self.disp_val = Label(disp_values_frame, text="N/A", font = label_font_settings, padx = pad_x, pady = pad_y)
        self.depth_val = Label(disp_values_frame, text="N/A", font = label_font_settings, padx = pad_x, pady = pad_y)
        self.transf_matrix = Label(disp_values_frame, text="N/A", font = label_font_settings, padx = pad_x, pady = pad_y)
        self.pack_disp_depth_values()
        return disp_values_frame

    def pack_disp_depth_values(self):
        self.coord_x.grid(row=self.coord_x_pos[0], column=self.coord_x_pos[2], sticky=W)
        self.coord_y.grid(row=self.coord_y_pos[0], column=self.coord_y_pos[2], sticky=W)
        self.disp_val.grid(row=self.disp_val_pos[0], column=self.disp_val_pos[2], sticky=W) 
        self.depth_val.grid(row=self.depth_val_pos[0], column=self.depth_val_pos[2], sticky=W) 
        self.transf_matrix.grid(row=self.curr_matrix_pos[0], column=self.curr_matrix_pos[2], sticky=W) 
   
    def init_secondary_buttons(self, master):
        button_padding = [30,5]
        self.back = Button(master, text="<- Back", command=lambda mode = 0: self.window_switch_btn_function(mode), padx=button_padding[0], pady=button_padding[1])
        self.save_map = Button(master, text="Save the disparity map", command=lambda: self.open_channel, padx=button_padding[0], pady=button_padding[1])
        self.load_disp_map = Button(master, text="Load another disparity map", command=lambda: self.open_channel, padx=button_padding[0], pady=button_padding[1])
        self.load_disp_depth_matrix = Button(master, text="Load disparity-depth matrix", command=lambda: self.open_channel, padx=button_padding[0], pady=button_padding[1])
        self.save_Depth = Button(master, text="Save depth map", command=lambda: self.open_channel(), padx=button_padding[0], pady=button_padding[1])
        self.save_RGBD = Button(master, text="Save RGBD Image", command=lambda: self.open_channel(), padx=button_padding[0], pady=button_padding[1])

    def set_secondary_button_panel(self, master):
        self.back.grid(row = self.back_btn_pos[0], column = self.back_btn_pos[1], columnspan = 1)
        self.save_map.grid(row = self.save_map_btn_pos[0], column = self.save_map_btn_pos[1], columnspan = 1)
        self.load_disp_map.grid(row = self.load_map_btn_pos[0], column = self.load_map_btn_pos[1], columnspan = 1)
        self.load_disp_depth_matrix.grid(row = self.load_matrix_btn[0], column = self.load_matrix_btn[1], columnspan = 1)
        self.save_Depth.grid(row = self.save_depth_btn[0], column = self.save_depth_btn[1], columnspan = 1)
        self.save_RGBD.grid(row = self.save_rgbd_btn[0], column = self.save_rgbd_btn[1], columnspan = 1)
        Label(master, text="  ").grid(row=self.btn_margin_1_pos[0], column=self.btn_margin_1_pos[1])
        Label(master, text="  ").grid(row=self.btn_margin_2_pos[0], column=self.btn_margin_2_pos[1])
        Label(master, text="  ").grid(row=self.btn_margin_3_pos[0], column=self.btn_margin_3_pos[1])
        Label(master, text="  ").grid(row=self.btn_margin_4_pos[0], column=self.btn_margin_4_pos[1])
        Label(master, text="  ").grid(row=self.btn_margin_5_pos[0], column=self.btn_margin_5_pos[1])
        Label(master, text="  ").grid(row=self.btn_margin_6_pos[0], column=self.btn_margin_6_pos[1])

    def pack_secondary_buttons(self):
        button_frame = Frame(self.disparity_map)
        self.init_secondary_buttons(button_frame)
        self.set_secondary_button_panel(button_frame)
        return button_frame
        
    def place_widgets(self):
        sliders = self.pack_sliders()
        sliders.grid(row=self.disp_slider_frame_pos[0], column=self.disp_slider_frame_pos[1])
        primary_buttons = self.pack_buttons()
        primary_buttons.grid(row=self.disp_button_frame_pos[0], column=self.disp_button_frame_pos[1], columnspan = 5)
        channel_frames = self.create_UI_image_frame()
        channel_frames.grid(row=self.img_frames_frame_pos[0], column=self.img_frames_frame_pos[1], columnspan = 3)

        map_frames = self.init_disp_map()
        map_frames.grid(row=self.map_frames_frame_pos[0], column=self.map_frames_frame_pos[1], sticky=E)
        disparity_depth_values = self.init_disp_depth_values()
        disparity_depth_values.grid(row=self.disp_val_frame_pos[0], column=self.disp_val_frame_pos[1], sticky=W)
        secondary_buttons = self.pack_secondary_buttons()
        secondary_buttons.grid(row=self.secondary_btn_frame_pos[0], column=self.secondary_btn_frame_pos[1], columnspan = 6, sticky=W+E)

    def create_margins(self):
        Label(self.disparity_settings, text="  ").grid(row=self.margin_1_pos[0], column=self.margin_1_pos[1])
        Label(self.disparity_settings, text="  ").grid(row=self.margin_2_pos[0], column=self.margin_2_pos[1])
        Label(self.disparity_settings, text="  ").grid(row=self.margin_3_pos[0], column=self.margin_3_pos[1])
        # Label(self.disparity_settings, text="  ").grid(row=self.margin_4_pos[0], column=self.margin_4_pos[1])

    def save_settings(self):
        settings_files = self.fm.get_settings_dir()
        new_settings = []
        new_settings.append(str(self.dm.P1) + '\n')
        new_settings.append(str(self.dm.P2) + '\n')
        new_settings.append(str(self.dm.preFilterCap) + '\n')
        new_settings.append(str(self.dm.min_disp) + '\n')
        new_settings.append(str(self.dm.max_disp) + '\n')
        new_settings.append(str(self.dm.blockSize) + '\n')
        new_settings.append(str(self.dm.uniquenessRatio) + '\n')
        new_settings.append(str(self.dm.speckleWindowSize) + '\n')
        new_settings.append(str(self.dm.speckleRange) + '\n')
        new_settings.append(str(self.dm.disp12MaxDiff))
        path_to_pref = filedialog.asksaveasfile(
                    defaultextension='.txt', 
                    filetypes=[("Text files", '*.txt')],
                    initialdir=settings_files,
                    initialfile = '*.txt',
                    title="Choose filename")
        if path_to_pref is not None: 
            for s in new_settings: 
                path_to_pref.write(s)
            print("Settings saved!")
        else: print("Error when saving settings!")

    def load_settings(self):
        settings_files = self.fm.get_settings_dir()
        # init_settings = open(settings_files + '\\' + "disparity_default.txt", 'r')
        loaded = filedialog.askopenfile(initialdir = settings_files, title = "Select file", filetypes = (("Text files","*.txt"),("all files","*.*")))
        if loaded is not None: 
            new_settings_list = []
            for line in loaded.readlines(): new_settings_list.append(int(line.strip())) 
            self.dm.update_values(
                P1 = new_settings_list[0],
                P2 = new_settings_list[1],
                preFilterCap = new_settings_list[2],
                min_disp = new_settings_list[3],
                max_disp = new_settings_list[4],
                blockSize = new_settings_list[5],
                uniquenessRatio = new_settings_list[6],
                speckleWindowSize = new_settings_list[7],
                speckleRange = new_settings_list[8],
                disp12MaxDiff = new_settings_list[9])
            self.update_and_set_sliders()

    def calc_aspect_ratio(self, width, height):
        div = gcd(width, height)
        aspect_ratio = [int(width/div), int(height/div)]
        print(aspect_ratio)
        return aspect_ratio

    def scale_im_for_GUI(self, width, height):
        aspect_ratio = self.calc_aspect_ratio(width, height)
        # while (width > self.resize_dimensions_UI_pictures[0] or height > self.resize_dimensions_UI_pictures[1]):      #The proper way
        #     width = width - aspect_ratio[0]
        #     height = height - aspect_ratio[1]
        while (width > self.resize_dimensions_UI_pictures[0] or height > self.resize_dimensions_UI_pictures[1]):
            width = width/1.2
            height = height/1.2
        resize_dimensions = (int(width), int(height))
        print(resize_dimensions)
        return resize_dimensions    

    def prepare_and_load_maps(self, map_path):
        original = Image.open(map_path)
        resize_dimensions = self.scale_im_for_GUI(original.width, original.height)
        temp = original.resize(resize_dimensions, Image.ANTIALIAS)
        picture = ImageTk.PhotoImage(temp)
        self.reset_parent(self.disp_map_frame)
        self.left_image_path = map_path
        self.map_disparity = Label(self.disp_map_frame, image = picture, width = self.placeholder_size[0], height = self.placeholder_size[1])
        self.map_disparity.image = picture
        self.map_disparity.pack()

        # TO-DO Depth map transform from disparity map
        # self.reset_parent(self.depth_map_frame)
        # self.right_image_path = map_path
        # self.map_depth = Label(self.depth_map_frame, image=picture, width = self.placeholder_size[0], height = self.placeholder_size[1])
        # self.map_depth.image = picture
        # self.map_depth.pack()

    def prepare_and_load_image(self, side, picture_path):
        original = Image.open(picture_path)
        resize_dimensions = self.scale_im_for_GUI(original.width, original.height)
        # print(resize_dimensions)
        # print(original.width, original.height)
        temp = original.resize(resize_dimensions, Image.ANTIALIAS)
        picture = ImageTk.PhotoImage(temp)
        if (side == "left"): 
            self.reset_parent(self.left_img_frame)
            self.left_image_path = picture_path
            self.image_label_left = Label(self.left_img_frame, image = picture, width = self.placeholder_size[0], height = self.placeholder_size[1])
            self.image_label_left.image = picture
            self.image_label_left.pack()
        else: 
            self.reset_parent(self.right_img_frame)
            self.right_image_path = picture_path
            self.image_label_right = Label(self.right_img_frame, image=picture, width = self.placeholder_size[0], height = self.placeholder_size[1])
            self.image_label_right.image = picture
            self.image_label_right.pack()

    def open_channel(self, channel):
        loaded = filedialog.askopenfilename(initialdir = self.fm.get_res_dir(), title = "Select file", filetypes = (("JPG files","*.jpg"),("PNG files","*.png"),("all files","*.*")))
        if loaded is not None: 
            self.prepare_and_load_image(channel, loaded)

    def open_different_map(self):
        loaded = filedialog.askopenfilename(initialdir = self.fm.get_res_dir(), title = "Select file", filetypes = (("Image files","*.png"),("all files","*.*")))
        if loaded is not None: 
            self.prepare_and_load_maps(loaded)

    def calculate_disp_map(self, mode):
        # self.window_switch_btn_function(mode)
        self.dm.generate_disp_map(self.left_image_path, self.right_image_path)

    def window_switch_btn_function(self, mode):
        self.disparity_window.select(mode)

    def reset_parent(self, master):
        for widget in master.winfo_children():
            widget.destroy()

    
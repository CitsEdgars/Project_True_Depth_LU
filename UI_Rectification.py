from tkinter import *
from tkinter import filedialog, ttk
import cv2
from PIL import Image, ImageTk
from fractions import gcd

from FileManager import FileManager
from RectifyChannels import RectifyChannels
from CameraCalibration import CameraCalibration


class UI_Rectification():
    
    placeholder_size = [480,480]
    resize_dimensions_UI_pictures = [480,480]
    
    left_im_frame_pos = [0,1]
    right_im_frame_pos = [0,3]
 
    img_frames_frame_pos = [0,1]
    disp_slider_frame_pos = [0,5]
    disp_button_frame_pos = [2,1]

    map_frames_frame_pos = [0,1]
    disp_val_frame_pos = [0,4]
    secondary_btn_frame_pos = [2,1]
    
    calib_left_btn_pos = [0,1]
    load_left_btn_pos = [0,3]
    undistort_left_btn_pos = [0,5]
    calib_right_btn_pos = [0,7]
    load_right_btn_pos = [0,9]
    undistort_right_btn_pos = [0,11]

    show_offset_btn_pos = [0,11]
    rectify_save_btn_pos = [0,11]
    rectify_save_mine_pos = [0,11]

    btn_margin_1_pos = [0,0]
    btn_margin_2_pos = [0,2]
    btn_margin_3_pos = [0,4]
    btn_margin_4_pos = [0,6]
    btn_margin_5_pos = [0,8]
    btn_margin_6_pos = [0,10]
    btn_margin_7_pos = [0,12]

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

    offset_btn_pos = [0,0,1]
    rectify_default_pos = [2,0,1]
    rectify_mine_pos = [4,0,1]

    UI_window = Widget
    
    def __init__(self, master):
        self.UI_window = master
        self.Rectification_window = ttk.Notebook(self.UI_window)
        self.Rectification_window.pack(pady = 3, padx = 3)
        self.calibrate_and_undistort = Frame(self.Rectification_window)
        self.rectify = Frame(self.Rectification_window)
        self.calibrate_and_undistort.pack(fill = "both", expand = 1)
        self.rectify.pack(fill = "both", expand = 1)
        self.Rectification_window.add(self.calibrate_and_undistort, text = "  Calibrate, undistort and rectify  ")
        self.Rectification_window.add(self.rectify, text = "  Additonal information  ")
        self.fm = FileManager()

    def open_main(self):
        self.place_widgets()
        self.create_margins()

    def create_UI_image_frame(self):
        image_frame = Frame(self.calibrate_and_undistort, padx = 5, pady = 10)
        self.left_img_frame = LabelFrame(image_frame, text = "Left Channel", width = self.placeholder_size[0], height = self.placeholder_size[1])
        self.right_img_frame = LabelFrame(image_frame, text = "Right Channel", width = self.placeholder_size[0], height = self.placeholder_size[1])
        self.pack_channel_frames()
        return image_frame

    def pack_channel_frames(self):
        self.left_img_frame.grid(row = self.left_im_frame_pos[0], column = self.left_im_frame_pos[1])
        self.right_img_frame.grid(row = self.right_im_frame_pos[0], column = self.right_im_frame_pos[1])
        self.left_img_frame.pack_propagate(False)
        self.right_img_frame.pack_propagate(False)

    def pack_buttons(self):
        button_frame = Frame(self.calibrate_and_undistort) #TO-DO
        self.init_buttons(button_frame)
        self.set_button_panel(button_frame)
        return button_frame

    def init_disp_depth_values(self):
        disp_values_frame = Frame(self.calibrate_and_undistort, padx = 5, pady = 10)
        button_padding = [30,5]

        offset_btn = Button(disp_values_frame, text="Show rectification shift", command=lambda: self.show_shift(), padx=button_padding[0], pady=button_padding[1])
        rectify_default = Button(disp_values_frame, text="Rectify and Save", command=lambda: self.rectify_and_save(), padx=button_padding[0], pady=button_padding[1])
        rectify_mine = Button(disp_values_frame, text="Rectify and Save (Experimental)", command=lambda: self.rectify_and_save(), padx=button_padding[0], pady=button_padding[1], state = "disabled")

        offset_btn.grid(row=self.offset_btn_pos[0], column=self.offset_btn_pos[1], sticky=W+E)
        rectify_default.grid(row=self.rectify_default_pos[0], column=self.rectify_default_pos[1], sticky=W+E)
        rectify_mine.grid(row=self.rectify_mine_pos[0], column=self.rectify_mine_pos[1], sticky=W+E)

        Label(disp_values_frame, text="  ").grid(row=self.offset_btn_pos[0]+1, column=self.offset_btn_pos[1])
        Label(disp_values_frame, text="  ").grid(row=self.rectify_default_pos[0]+1, column=self.offset_btn_pos[1])
        return disp_values_frame

    def pack_disp_depth_values(self):
        self.coord_x.grid(row=self.coord_x_pos[0], column=self.coord_x_pos[2], sticky=W)
        self.coord_y.grid(row=self.coord_y_pos[0], column=self.coord_y_pos[2], sticky=W)
        self.disp_val.grid(row=self.disp_val_pos[0], column=self.disp_val_pos[2], sticky=W) 
        self.depth_val.grid(row=self.depth_val_pos[0], column=self.depth_val_pos[2], sticky=W) 
        self.transf_matrix.grid(row=self.curr_matrix_pos[0], column=self.curr_matrix_pos[2], sticky=W) 
   
    def calibrate_channel(self, channel):
        #TO-DO: Add path selector and modify the CameraCalibration calibration image selection
        left_calib_path = ""
        right_calib_path = ""
        cc = CameraCalibration(None, None, left_calib_path, right_calib_path)
        if (channel == "left"):
            cc.calibrate_camera(left_calib_path)
        else:
            cc.calibrate_camera(right_calib_path)

    def undistort_channel(self, channel):
        if (channel == "left"):
            cc = CameraCalibration(self.left_image_path, None, None, None)
            undistorted = cc.undistort_image(channel)
            new_file_path = self.fm.get_res_dir() + "\\left_undistorted.jpg"
            cv2.imwrite(new_file_path, undistorted)
            self.prepare_and_load_image(channel, new_file_path)
        else:
            cc = CameraCalibration(None, self.right_image_path, None, None)
            undistorted = cc.undistort_image(channel)
            new_file_path = self.fm.get_res_dir() + "\\right_undistorted.jpg"
            cv2.imwrite(new_file_path, undistorted)
            self.prepare_and_load_image(channel, new_file_path)
        

    def show_shift(self):
        temp_loc = self.fm.get_res_dir()    #Izdomaa kko labaaku
        rc = RectifyChannels(self.left_image_path, self.right_image_path, temp_loc, temp_loc, 20, True)

    def rectify_and_save(self):
        temp_loc = self.fm.get_res_dir()    #Izdomaa kko labaaku
        rc = RectifyChannels(self.left_image_path, self.right_image_path, temp_loc, temp_loc, 20, False)
        rc.rectify_with_default()

    def init_buttons(self, master):
        button_padding = [30,5]
        self.calbrate_left = Button(master, text="Calibrate left", command=lambda channel = "left": self.calibrate_channel(channel), padx=button_padding[0], pady=button_padding[1], state = "disabled")
        self.load_left = Button(master, text="Load left", command=lambda channel = "left": self.open_channel(channel), padx=button_padding[0], pady=button_padding[1])
        self.undistort_left = Button(master, text="Undistort", command=lambda channel = "left": self.undistort_channel(channel), padx=button_padding[0], pady=button_padding[1])

        self.calbrate_right = Button(master, text="Calibrate right", command=lambda channel = "right": self.calibrate_channel(channel), padx=button_padding[0], pady=button_padding[1], state = "disabled",)
        self.load_right = Button(master, text="Load right", command=lambda channel = "right": self.open_channel(channel), padx=button_padding[0], pady=button_padding[1])
        self.undistort_right = Button(master, text="Undistort", command=lambda channel = "right": self.undistort_channel(channel), padx=button_padding[0], pady=button_padding[1])


    def set_button_panel(self, master):
        self.calbrate_left.grid(row = self.calib_left_btn_pos[0], column = self.calib_left_btn_pos[1], columnspan = 1)
        self.load_left.grid(row = self.load_left_btn_pos[0], column = self.load_left_btn_pos[1], columnspan = 1)
        self.undistort_left.grid(row = self.undistort_left_btn_pos[0], column = self.undistort_left_btn_pos[1], columnspan = 1)

        self.calbrate_right.grid(row = self.calib_right_btn_pos[0], column = self.calib_right_btn_pos[1], columnspan = 1)
        self.load_right.grid(row = self.load_right_btn_pos[0], column = self.load_right_btn_pos[1], columnspan = 1)
        self.undistort_right.grid(row = self.undistort_right_btn_pos[0], column = self.undistort_right_btn_pos[1], columnspan = 1)

        Label(master, text="  ").grid(row=self.btn_margin_1_pos[0], column=self.btn_margin_1_pos[1])
        Label(master, text="  ").grid(row=self.btn_margin_2_pos[0], column=self.btn_margin_2_pos[1])
        Label(master, text="  ").grid(row=self.btn_margin_3_pos[0], column=self.btn_margin_3_pos[1])
        Label(master, text="                    ").grid(row=self.btn_margin_4_pos[0], column=self.btn_margin_4_pos[1])
        Label(master, text="  ").grid(row=self.btn_margin_5_pos[0], column=self.btn_margin_5_pos[1])
        Label(master, text="  ").grid(row=self.btn_margin_6_pos[0], column=self.btn_margin_6_pos[1])
        Label(master, text="                                                                                 ").grid(row=self.btn_margin_7_pos[0], column=self.btn_margin_7_pos[1])
        Label(master, text="                                                                                 ").grid(row=self.btn_margin_7_pos[0]+1, column=self.btn_margin_7_pos[1])

        
    def place_widgets(self):
        primary_buttons = self.pack_buttons()
        primary_buttons.grid(row=self.disp_button_frame_pos[0], column=self.disp_button_frame_pos[1], columnspan = 5)
        channel_frames = self.create_UI_image_frame()
        channel_frames.grid(row=self.img_frames_frame_pos[0], column=self.img_frames_frame_pos[1], columnspan = 3)
        disparity_depth_values = self.init_disp_depth_values()
        disparity_depth_values.grid(row=self.disp_val_frame_pos[0], column=self.disp_val_frame_pos[1], sticky=W)

    def create_margins(self):
        Label(self.calibrate_and_undistort, text="  ").grid(row=self.margin_1_pos[0], column=self.margin_1_pos[1])
        Label(self.calibrate_and_undistort, text="  ").grid(row=self.margin_2_pos[0], column=self.margin_2_pos[1])
        Label(self.calibrate_and_undistort, text="  ").grid(row=self.margin_3_pos[0], column=self.margin_3_pos[1])
        
    def scale_im_for_GUI(self, width, height):
        while (width > self.resize_dimensions_UI_pictures[0] or height > self.resize_dimensions_UI_pictures[1]):
            width = width/1.1
            height = height/1.1
        resize_dimensions = (int(width), int(height))
        print(resize_dimensions)
        return resize_dimensions

    def prepare_and_load_image(self, side, picture_path):
        print(picture_path)
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

    def reset_parent(self, master):
        for widget in master.winfo_children():
            widget.destroy()
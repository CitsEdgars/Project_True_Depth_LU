from CameraCalib.CameraCalib import CameraCalib
from xml.etree import ElementTree as et
import cv2
import ast

class CameraCalibration():

    calib_src_left = ""
    calib_src_right = ""
    undistort_left = 'left.jpg'
    undistort_right = 'right.jpg'

    calibration_file_left = ''
    calibration_file_right = ''
    imagesfolder = ''
    viewcalibration = False

    def __init__(self, undistort_left, undistort_right, calib_left_src, calib_right_src):
        self.calib_src_left = calib_left_src
        self.calib_src_right = calib_right_src
        self.undistort_left = undistort_left
        self.undistort_right = undistort_right
        self.get_and_set_params()

    def get_and_set_params(self):
        tree = et.parse('settings/cameracalibration.xml') #make changeable
        root = tree.getroot()
        xmlfile = root.findall('camera')
        # TO-DO: Bad formulation of what I need, I have 1 argument, but there could be many
        for params in xmlfile:
            self.calibration_file_left = params.find('calibrationFileLeft').text
            self.calibration_file_right = params.find('calibrationFileRight').text
            self.imagesfolder = params.find('imagesFolder').text 
            self.viewcalibration = ast.literal_eval(params.find('viewCalibration').text)

    def calibrate_camera(self, images_folder): # Camera Calibration Usage
        # camc = CameraCalib(calibrationfile, viewcalibration) 
        # camc.calib(images_folder)
        return None

    def undistort_image(self, channel):
        if (channel == "left"):
            camc_left = CameraCalib(self.calibration_file_left, self.viewcalibration)
            camc_left.calibParams()
            returned_img = cv2.imread(self.undistort_left) 
            returned_img = camc_left.undistort(returned_img) 
        else:         
            camc_right = CameraCalib(self.calibration_file_right, self.viewcalibration) 
            camc_right.calibParams()
            returned_img = cv2.imread(self.undistort_right)  
            returned_img = camc_right.undistort(returned_img) 
        return returned_img

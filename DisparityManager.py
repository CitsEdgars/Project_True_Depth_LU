import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

class DisparityManager():

    lmbda = 60000
    sigma = 2.6

    resize_param = 1
    use_filter = 0

    P1 = 0
    P2 = 0
    preFilterCap = 0
    min_disp = 0
    max_disp = 0
    blockSize = 0
    uniquenessRatio = 0
    speckleWindowSize = 0
    speckleRange = 0
    disp12MaxDiff = 0

    def __init__(self, P1, P2, preFilterCap, min_disp, max_disp, blockSize, uniquenessRatio, speckleWindowSize, speckleRange, disp12MaxDiff):
        self.P1 = P1
        self.P2 = P2
        self.preFilterCap = preFilterCap
        self.min_disp = min_disp
        self.max_disp = max_disp
        self.blockSize = blockSize
        self.uniquenessRatio = uniquenessRatio
        self.speckleWindowSize = speckleWindowSize
        self.speckleRange = speckleRange
        self.disp12MaxDiff = disp12MaxDiff  
    
    def update_values(self,
            P1=None, 
            P2=None, 
            preFilterCap=None, 
            min_disp=None, 
            max_disp=None,
            blockSize=None,
            uniquenessRatio=None,
            speckleWindowSize=None,
            speckleRange=None,
            disp12MaxDiff=None):
        if(P1 is not None): self.P1 = P1
        if(P2 is not None): self.P2 = P2
        if(preFilterCap is not None): self.preFilterCap = preFilterCap
        if(min_disp is not None): self.min_disp = min_disp
        if(max_disp is not None): self.max_disp = max_disp
        if(blockSize is not None): self.blockSize = blockSize
        if(uniquenessRatio is not None): self.uniquenessRatio = uniquenessRatio
        if(speckleWindowSize is not None): self.speckleWindowSize = speckleWindowSize
        if(speckleRange is not None): self.speckleRange = speckleRange
        if(disp12MaxDiff is not None): self.disp12MaxDiff = disp12MaxDiff 

    def resize_picture(self, img, param):
        downsized = cv2.resize(img, (0,0), fx=param, fy=param)
        return downsized

    def generate_disp_map(self, left_link, right_link):
        img_left = self.resize_picture(cv2.imread(left_link, 1), self.resize_param)
        img_right = self.resize_picture(cv2.imread(right_link, 1), self.resize_param)

        image_bw_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY) 
        image_bw_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY) 

        stereo = cv2.StereoSGBM_create(
            minDisparity= int(self.min_disp),
            numDisparities = int(self.max_disp) - int(self.min_disp),
            blockSize = int(self.blockSize),
            uniquenessRatio = int(self.uniquenessRatio),
            speckleWindowSize = int(self.speckleWindowSize),
            speckleRange = int(self.speckleRange),
            disp12MaxDiff = int(self.disp12MaxDiff),
            preFilterCap = int(self.preFilterCap),
            P1 = int(self.P1),
            P2 = int(self.P2))
        
        # stereo = cv2.StereoBM_create(numDisparities = int(self.max_disp), blockSize = int(self.blockSize))



        if (self.use_filter == 1): 
            wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=stereo)
            wls_filter.setLambda(self.lmbda)     
            wls_filter.setSigmaColor(self.sigma)
            disparity_right = stereo.compute(image_bw_right, image_bw_left).astype(np.float32) / int(self.max_disp)
            disparity_left = stereo.compute(image_bw_left, image_bw_right).astype(np.float32) / int(self.max_disp)
            disparity_map = wls_filter.filter(disparity_left, image_bw_left, disparity_map_right=disparity_right)

            # cv2.imshow('disparity_map', disparity_map)
            # disparity_map = cv2.normalize(src=disparity_map, dst=disparity_map, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX);
            # disparity_map = np.uint8(disparity_map)

            print("Calculated filtered image")
        else: 
            disparity_map = stereo.compute(image_bw_left, image_bw_right) / int(self.max_disp)
            print("Calculated unfiltered image")

        # if (self.use_filter == 1): 
        #     wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=stereo)
        #     sigma_range = [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0]
        #     lmdba_range = [5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000]
        #     for y in lmdba_range:
        #         for x in sigma_range:
        #             wls_filter.setLambda(y)     
        #             wls_filter.setSigmaColor(x)
        #             disparity_right = stereo.compute(image_bw_right, image_bw_left).astype(np.float32) / int(self.max_disp)
        #             disparity_left = stereo.compute(image_bw_left, image_bw_right).astype(np.float32) / int(self.max_disp)
        #             disparity_map = wls_filter.filter(disparity_left, image_bw_left, disparity_map_right=disparity_right)
        #             map_name = "map_filtered_" + str(y) + "_" + str(x) + ".png"
        #             plt.imsave(fname = map_name, arr = disparity_map, cmap='CMRmap_r')
        #     # disparity_map = disparity_left
        #     print("Calculated filtered image")
        # else: 
        #     disparity_map = stereo.compute(img_left, img_right).astype(np.float32) / int(self.max_disp)
        #     print("Calculated unfiltered image")

        plt.imshow(X=disparity_map, cmap='CMRmap_r')
        plt.show()

        #plt.imsave(fname = "map_raw.png", arr = disparity_map, cmap='gray')
        #plt.imsave(fname = "map_filtered.png", arr = disparity_map, cmap='gray')
        # im = Image.open("map.png")
        # im2 = im.crop((int(self.max_disp), 0, 1000, 1500))      
        # im2.save("map_crop.png")


    def update_P1(self, value): 
        self.update_values(P1=value)
    def update_P2(self, value): 
        self.update_values(P2=value)
    def update_preFilterCap(self, value): 
        self.update_values(preFilterCap=value)
    def update_min_disp(self, value): 
        self.update_values(min_disp=value)
    def update_max_disp(self, value): 
        self.update_values(max_disp=value)
    def update_blockSize(self, value): 
        self.update_values(blockSize=value)
    def update_uniquenessRatio(self, value): 
        self.update_values(uniquenessRatio=value)
    def update_speckleWindowSize(self, value): 
        self.update_values(speckleWindowSize=value)
    def update_speckleRange(self, value): 
        self.update_values(speckleRange=value)
    def update_disp12MaxDiff(self, value): 
        self.update_values(disp12MaxDiff=value)
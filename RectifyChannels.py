import cv2
import math
from matplotlib import pyplot as plt

from skimage.util import img_as_float
from skimage.feature import (corner_harris, corner_subpix, corner_peaks,
                             plot_matches)
from skimage.transform import warp
from skimage.exposure import rescale_intensity
from skimage.color import rgb2gray
from skimage.measure import ransac

class RectifyChannels():

    show_result = False
    match_amount = 10

    def __init__(self, left_src, right_src, left_trgt, right_trgt, match_amount, show_result):
        self.left = cv2.imread(left_src, 0)
        self.right = cv2.imread(right_src, 0)
        self.left_target = left_trgt + "\\rectified_left.jpg"
        self.right_target = right_trgt + "\\rectified_right.jpg"
        self.match_amount = match_amount
        self.show_result = show_result
        self.read_dimensions(self.left, self.right)
        self.find_ORB_matches()

    def rectify_with_default(self):
        self.find_ORB_matches()
        rect_left, rect_right = self.crop_images()
        cv2.imwrite(self.right_target, rect_right)
        cv2.imwrite(self.left_target, rect_left)
    
    def read_dimensions(self, left, right):
        # TO-DO: Add a checker for both images.
        height, width = left.shape
        image_dimensions = (width, height)
        self.picture_dimensions = image_dimensions

    def find_ORB_matches(self):
        orb = cv2.ORB_create()

        kpLeft, desLeft = orb.detectAndCompute(self.left, None)
        kpRight, desRight = orb.detectAndCompute(self.right, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

        matches = bf.match(desLeft, desRight)
        matches = sorted(matches, key = lambda x:x.distance)

        matches_to_present = matches[:self.match_amount]

        self.list_kpLeft = []
        self.list_kpRight = []
        self.list_y_coord_diff = []

        for match in matches_to_present:

            imgLeft_idx = match.queryIdx
            imgRight_idx = match.trainIdx

            (xLeft, yLeft) = kpLeft[imgLeft_idx].pt
            (xRight, yRight) = kpRight[imgRight_idx].pt

            self.list_kpLeft.append((xLeft, yLeft))
            self.list_kpRight.append((xRight, yRight))
            self.list_y_coord_diff.append(yLeft - yRight)

        if (self.show_result == True):
            imgResult = cv2.drawMatches(self.left, kpLeft, self.right, kpRight, matches_to_present, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS) 
            plt.imshow(imgResult)
            plt.show()
            cv2.waitKey(0) 
            cv2.destroyAllWindows()

    def crop_images(self):
        height_shift_diff = math.ceil(sum(self.list_y_coord_diff) / len(self.list_y_coord_diff)) 
        print(height_shift_diff, self.picture_dimensions[1], self.picture_dimensions[0]) 
        rect_left = self.left[height_shift_diff:self.picture_dimensions[1], 0:self.picture_dimensions[0]]      #[start row:end row, start columnt:end column]
        rect_right = self.right[0:self.picture_dimensions[1]-height_shift_diff, 0:self.picture_dimensions[0]]
        return rect_left, rect_right



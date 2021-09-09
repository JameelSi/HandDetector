import numpy as np
import cv2
import os
from matplotlib import pyplot as plt


if __name__ == "__main__":
    dirr = './images'
    images = []
    # loop over the folder and insert each image to the list created above. 
    for pic in os.listdir(dirr):
        img = cv2.imread(os.path.join(dirr,pic))
        if img is not None:
           images.append(img)
    
    for i in range(len(images)):
        # convert to gray, blur find edges
        gray = cv2.cvtColor(images[i],cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 7)
        gray=255-gray
        gray = cv2.normalize(gray,  gray, 0, 255, cv2.NORM_MINMAX) 
        gray = cv2.Canny(gray,90,110)
        kernel = np.ones((5,5),np.uint8)
        gray = cv2.dilate(gray,kernel,iterations = 1)
        rows = gray.shape[0]
        # now find circles or semi circles in the pictures which are the fingers 
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.1, rows / 8,
                                param1=30, param2=20,
                                minRadius=1, maxRadius=30)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for j in circles[0, :]:
                center = (j[0], j[1])
                radius = j[2]
                cv2.circle(images[i], center, 3, (255, 0, 0), 3)
        



        plt.imshow(images[i])
        plt.title(i+1)
        plt.tight_layout()
        plt.show()
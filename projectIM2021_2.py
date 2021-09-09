import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
import xlwt 
from xlwt import Workbook
if __name__ == "__main__":
    dirr = './images'
    images = []
    # loop over the folder and insert each image to the list created above. 
    for pic in os.listdir(dirr):
        img = cv2.imread(os.path.join(dirr,pic))
        if img is not None:
           images.append(img)
    
    for i in range(len(images)):
        # convert to gray ,blur apply canny
        gray = cv2.cvtColor(images[i],cv2.COLOR_BGR2GRAY)
        gray=gray[gray.shape[0]//30:gray.shape[0],int(gray.shape[1]/2.5):gray.shape[1]-gray.shape[1]//10]
        gray = cv2.medianBlur(gray, 23)
        gray = cv2.Canny(gray,20,80)
        kernel = np.ones((5,5),np.uint8)
        # dialate edges
        gray = cv2.dilate(gray,kernel,iterations = 4)
        points=[0,0,0,0,0,0,0,0,0]
        #  find points using relations to edges and other points
        # First point
        for fY in range(gray.shape[0]):
            fX=gray.shape[1]-1
            if gray[fY,fX]==255:
                for sP in range(fY,gray.shape[0],1):
                    if gray[sP,fX]==0:
                        break
                    else:
                        fX=fX-3
            else:
                continue
            break
        points[0]=[fX+int(images[i].shape[1]/2.5),sP-10+images[i].shape[0]//30]
        # Second point
        for sP in range(sP+30,gray.shape[0],2):
            if gray[sP,fX]==255:
                break
            else:
                if fX+10<gray.shape[1]:
                    fX=fX+1
        points[1]=[fX+int(images[i].shape[1]/2.5),sP+images[i].shape[0]//30]
        # Third point
        for fX in range(fX,0,-1):
            if gray[sP,fX]==0:
                break
            else:
                sP=sP+1
        points[2]=[fX+int(images[i].shape[1]/2.5),sP-10+images[i].shape[0]//30]
        # Ninth point 
        for sP in range(sP-100,0,-5):
            if gray[sP,fX]==255:
                break
            else:
                fX=fX-1
        points[8]=[fX+int(images[i].shape[1]/2.5),sP-10+images[i].shape[0]//30]
        # Eigth point
        points[7]=[int( (4*( points[8][0] - points[0][0]/3 ) )/3 ),points[8][1]-10]
        # Sixth points
        fX=points[0][0]-int(images[i].shape[1]/2.5) -10
        sP=points[0][1]-images[i].shape[0]//30 +10
        for sP in range(sP,gray.shape[0],20):
            if gray[sP,fX]==255:
                break
            else:
                fX=fX-20
        points[5]=[fX+int(images[i].shape[1]/2.5),sP+images[i].shape[0]//30]
        # Seventh point
        fX=(points[0][0]-int(images[i].shape[1]/2.5)+points[1][0]-int(images[i].shape[1]/2.5))//2 
        sP=(points[0][1]-images[i].shape[0]//30 + points[1][1]-images[i].shape[0]//30)//2 
        for fX in range(fX,0,-10):
            if (gray[sP,fX]==255 or fX==1 ):
                break
        points[6]=[fX+int(images[i].shape[1]/2.5),sP+images[i].shape[0]//30]
        # Fourth point
        fX=points[2][0]-int(images[i].shape[1]/2.5)-40
        sP=points[2][1]-images[i].shape[0]//30  -20
        for sP in range(sP,0,-1):
            if gray[sP,fX]==255:
                break
            else: 
                fX=fX-1
        points[3]=[fX+int(images[i].shape[1]/2.5),sP+images[i].shape[0]//30]
        # Fifth point
        fX=(points[5][0] + points[3][0] )//2
        sP=points[5][1] 
        points[4]=[fX,sP]
        # draw and connect points
        pts=np.asarray(points,dtype=np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(images[i],[pts],True,(255,0,0))
        wb = Workbook() 
        sheet1 = wb.add_sheet('Points')
        sheet1.write(0,0,"Point")
        sheet1.write(0,1,"X")
        sheet1.write(0,2,"Y")
        for j in range(9):
            sheet1.write(j+1,0,str(j))
        for j in range(9):
            sheet1.write(j+1,1,str(points[j][0]))
        for j in range(9):
            sheet1.write(j+1,2,str(points[j][1]))
        wb.save('Points{}.xls'.format(i))
 

        plt.imshow(images[i])
        plt.title(i+1)
        plt.tight_layout()
        plt.show()



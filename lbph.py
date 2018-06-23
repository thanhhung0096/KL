from skimage.feature import local_binary_pattern
import cv2
import numpy as np
import ctypes
import time
class LBPH():
    def __init__(self,image,P , R):
        # self.image = cv2.equalizeHist(image)
        self.image = image
        self.P = P
        self.R = R
        self.HIST = None
    def create_LBP(self):
        self.image = cv2.resize(self.image, (200, 200))
       
        return local_binary_pattern(self.image,self.P,self.R ,method="default")
##
        self.image = self.image.astype("float")
        r, c = self.image.shape
        outdata = np.zeros((r, c), dtype=np.double)
        lib = ctypes.cdll.LoadLibrary('./main.so')
        fun = lib.cfun
        # Here comes the fool part.

        fun(ctypes.c_void_p(self.image.ctypes.data), ctypes.c_int(r), ctypes.c_int(c), ctypes.c_void_p(outdata.ctypes.data))
        outdata = outdata.astype("uint8")
        return outdata

    def divide_image(self,image):
        images = []
        for r in range(0, 199, 20):
            for c in range(0, 199, 20):
                images.append(image[r:r + 20, c:c + 20])
        return images

    def create_MB_LBPH_2(self):
        # t =  time.time()
        eps = 1e-9
        lbp_image = self.create_LBP()
        lbp_image = lbp_image.astype("uint8")
        cv2.imwrite("aaa.jpg",lbp_image)       
        lbp_blocks = self.divide_image(lbp_image)
        HIST = np.empty((0))
        for block in lbp_blocks:
            # print( block
            # print block.shape
            # hist, _ = np.histogram(lbp_image.ravel(), bins=np.arange(0, self.P + 3), range=[0, self.P +2])
            hist, a = np.histogram(block.ravel(), bins=np.arange(0,256), range=[0,255])
            # print hist
            # print "\n\n"
            HIST = np.concatenate((HIST, hist), axis=0)
        HIST = HIST.astype("float32")
        HIST /= (HIST.sum() + eps)
        # print "Time for extract MB_LBPH: " , (time.time() - t)
        self.HIST = HIST
##        print "shape " ,HIST.shape
        return HIST

    def findClosest(self, hists):
##        print self.HIST
        Dis = []
        minDis = 1000
        pos = 0
        for index ,hist in enumerate (hists):
            dis = cv2.compareHist(self.HIST, hist,method=cv2.HISTCMP_CHISQR) *100
    
            Dis.append(dis)
            if dis < minDis:
                minDis = dis
                pos = index
                
        return minDis,pos,Dis
    def detect_eye(self):
        eye_cascade_path = "haarcascade_eye.xml.xml"
        eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
        self.image = self.image.astype("uint8")
        eyes = eye_cascade.detectMultiScale(self.image,scaleFactor=1.2,minNeighbors=5)

            
            
            
        
        
        
        
        
        
        
        
        
        
        
        
        
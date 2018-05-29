from skimage.feature import local_binary_pattern
import cv2
import numpy as np
import time
class LBPH():
    def __init__(self,image,P , R):
        self.image = image
        self.P = P
        self.R = R
        self.HIST = None
    def create_LBP(self):
        return local_binary_pattern(self.image,self.P,self.R,method="default")

    def divide_image(self,image):
        images = []
        for r in range(0, 199, 20):
            for c in range(0, 199, 20):
                images.append(image[r:r + 20, c:c + 20])
        return images
    def create_MB_LBPH(self):
        # t =  time.time()
        image = cv2.resize(self.image, (200, 200))
        eps = 1e-9
        image_blocks = self.divide_image(image)
        HIST = np.empty((0))
        for block in image_blocks:
            # print block.shape
            lbp_image = local_binary_pattern(block, self.P, self.R, method='default')
            # print lbp_image
            # hist, _ = np.histogram(lbp_image.ravel(), bins=np.arange(0, self.P + 3), range=[0, self.P +2])
            hist, a = np.histogram(lbp_image.ravel(), bins=np.arange(0,256), range=[0,255])
            # print hist
            # print a
            # print "\n\n"
            HIST = np.concatenate((HIST, hist), axis=0)
        HIST = HIST.astype("float32")
        HIST /= (HIST.sum() + eps)
        # print "Time for extract MB_LBPH: " , (time.time() - t)
        self.HIST = HIST
        return HIST

    def create_MB_LBPH_2(self):
        # t =  time.time()
        image = cv2.resize(self.image, (200, 200))
        eps = 1e-9
        lbp_image = local_binary_pattern(image,8,2,'default')
##        lbp_image = lbp_image.astype("uint8")
        cv2.imwrite("a/lbp.png",lbp_image)
        lbp_blocks = self.divide_image(lbp_image)
        HIST = np.empty((0))
        for block in lbp_blocks:
            # print block
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
            
            
            
            
        
        
        
        
        
        
        
        
        
        
        
        
        
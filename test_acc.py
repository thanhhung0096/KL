import os
import cv2
import numpy as np
from lbph import  LBPH
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier
face_cascade_path = "lbpcascade_frontalface.xml"
from sklearn.svm import SVC
# aaa = "train data"
aaa = "orl_faces"
def detect_face(gray):
    face_cascde = cv2.CascadeClassifier(face_cascade_path)
    faces = face_cascde.detectMultiScale(gray, scaleFactor=1.2,minNeighbors=5)
    if (len(faces) ==0):
        return None,None
    (x,y,w,h) = faces[0]
    return gray[y:y+w, x:x+h],faces[0]


def extract_data():
    faces = []
    labels = []
    folders = os.listdir(aaa)
    for folder in folders:
        label = int(folder.replace("s", ""))
        images = os.listdir(aaa +"/"+ folder)
        for img in images:
            path = aaa + "/" + folder + "/" + img
            image = cv2.imread(path)
            ##            print type(image)
            ##            cv2.imshow("Training on image...", image)
            cv2.waitKey(100)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # gray = cv2.fastNlMeansDenoising(gray,None,4,7,21)
            # face, rect = detect_face(gray)
            # if face is not None:
            labels.append(label)
            faces.append(gray)


    return faces, labels

def findClosest(hist,listHists):
    ##        print self.HIST
    Dis = []
    minDis = 1000
    pos = 0
    for index, h in enumerate(listHists):
        dis = cv2.compareHist( hist,h, method=cv2.HISTCMP_CHISQR) * 100
        Dis.append(dis)
        if dis < minDis:
            minDis = dis
            pos = index

    return minDis, pos
def get_logTransform_image(i,c = 50):
    img_tmp = c * np.uint8(np.log1p(i+1))
    return img_tmp
if __name__ == '__main__':
    np.random.seed(10)
    faces , labels = extract_data()
    hists = []
    for face in faces:

        lbph = LBPH(face,8,2)
        hists.append(lbph.create_MB_LBPH_2())
        face = cv2.equalizeHist(face)
    print len(hists)
    data = zip(hists,labels)
    np.random.shuffle(data)
    hists,labels =zip(*data)
    trainSize = int(0.8*len(hists))
    trainX = hists[0:trainSize]
    trainY = labels[0:trainSize]

    testX= hists[trainSize : ]
    testY = labels[trainSize:]


    predictY = []

    Total_dis = 0;
    for i in range(len(testX)):
        # print np.array_equal(testX[i],testX_HE[i])
        dis,pos = findClosest(testX[i],trainX)
        predictY.append(trainY[pos])

    print predictY
    print testY
    print "acc using MB-LBPH: " ,accuracy_score(list(predictY), list(testY))*100


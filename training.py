import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import os
from lbph import LBPH
#function
face_cascade_path = "lbpcascade_frontalface.xml"

def detect_face(gray):
    face_cascde = cv2.CascadeClassifier(face_cascade_path)
    faces = face_cascde.detectMultiScale(gray, scaleFactor=1.2,minNeighbors=5)
    if (len(faces) ==0):
        return None,None
    (x,y,w,h) = faces[0]
    return gray[y:y+w, x:x+h],faces[0]

def draw_rectangle(rect):
    (x,y,w,h) =  rect
    cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
def extract_data_training():
    faces = []
    labels=[]
    folders =  os.listdir('train data')
    for folder in folders:
        label = int(folder.replace("s",""))
        images = os.listdir("train data/" + folder)
        for img in images:
            path = "train data/"+folder+"/"+img
            image = cv2.imread(path)
##            print type(image)
##            cv2.imshow("Training on image...", image)
            cv2.waitKey(100)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face,rect = detect_face(gray)
            if face is not None:
                #save
                path ="Faces/"+folder+"/"+img
                print "save face to "+path
                cv2.imwrite(path,face)
##                print type(face)
                labels.append(label)
                faces.append(face)
        
    return faces,labels
    
    
if __name__ == "__main__":
    t = time.time()
    faces,labels = extract_data_training()
    hists =[]
    for face in faces:
        lbph = LBPH(face,8,1)
        hists.append(lbph.create_MB_LBPH())
    
    np.savez("trained/trained.npz" , hists = hists, labels = labels)
    print "Training completed"
    print "Total time: " ,(time.time() - t) 
    
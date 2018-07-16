#!/bin/sh
import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import os
from lbph import LBPH
import shutil
#function



def detect_face(gray):
    face_cascade_path = "lbpcascade_frontalface.xml"
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
    
    path_to_train_data = "media/data"
    faces = []
    labels=[]
    folders =  os.listdir(path_to_train_data)
    User = ""
    label =0
    for folder in folders:
        label +=1
        print (label,folder)
        User += " "  + folder
        face_folder_path = "Faces/" + folder
        if not os.path.exists(face_folder_path):
            os.makedirs(face_folder_path)
##        label = int(folder.replace("s",""))
        images = os.listdir( path_to_train_data+"/" + folder)
        for img in images:
            path = path_to_train_data+"/"+folder+"/"+img
            image = cv2.imread(path)
##            print type(image)
##            cv2.imshow("Training on image...", image)
            cv2.waitKey(100)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face,rect = detect_face(gray)
            if face is not None:
                #save
                path ="Faces/"+folder+"/"+img
                print ("save face to "+path)
                cv2.imwrite(path,face)
##                print type(face)
                labels.append(label)
                faces.append(face)
            else:
                os.remove(path)
                print ("removed "  + path)
    with open("user","w") as f:
        f.write(User)
    return faces,labels
    
    
def main():
    t = time.time()
    try:
        shutil.rmtree("Faces")
    except:
        os.mkdir("Faces")
    faces,labels = extract_data_training()

    hists =[]
    for face in faces:
        lbph = LBPH(face,8,2)
        hists.append(lbph.create_MB_LBPH_2())
    ##    print hists[0].shape
    
    np.savez("trained/trained.npz" , hists = hists, labels = labels)
    print ("Training completed")
    print ("Total time: " ,(time.time() - t) )

main()

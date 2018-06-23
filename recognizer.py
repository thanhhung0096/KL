import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import os
from lbph import LBPH
#function

Names=[""]
def detect_face(gray):
    face_cascade_path = "lbpcascade_frontalface.xml"
    face_cascde = cv2.CascadeClassifier(face_cascade_path)
    faces = face_cascde.detectMultiScale(gray, scaleFactor=1.2,minNeighbors=5)
    if (len(faces) ==0):
        return None,None
    (x,y,w,h) = faces[0]
    return gray[y:y+w, x:x+h],faces[0]

def draw_rectangle(rect,g):
    (x,y,w,h) =  rect
    cv2.rectangle(g,(x,y),(x+w,y+h),(255,0,0),2)
    return g

def draw_name(img,text,x,y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

def predict(face,rect,gray,_hists,_labels,_Names):
##    cv2.imwrite("a/aa.png",face)
    lbph = LBPH(face,8,2)
    _ = lbph.create_MB_LBPH_2()
    confidence , pos,_ = lbph.findClosest(_hists)
    label = _labels[pos]
    
##    label,confidence =reconizer.predict(face)
    (x,y,w,h) = rect
    if confidence < 200:
        print (label)
        print( "Recognition: {}, confidence: {}".format(_Names[label],confidence))
        text = "{},{}".format(_Names[label],confidence)
##    text = Names[label]
        draw_name(gray,text,x,y)
    else:
        print( "Unknow people!!!")
        text = "unknow"
        draw_name(gray,text,x,y)
    
count = 0
if __name__ == "__main__":
    
    file = open("user","r")
    content = file.read();
    for i in range(1,len(content.split(" "))):
        Names.append(content.split(" ")[i])
    print( "Users: " , Names[1:])
    
    trained = np.load("trained/trained.npz")
    hists = trained['hists']
    labels = trained['labels']
    print( "Loaded train data.")
    
    
    #recognizer = cv2.face.createLBPHFaceRecognizer()

    #recognizer.load("trained/trained.yml")


    camera = PiCamera()
    camera.resolution = (480,320)
    camera.brightness = 60
    camera.framerate = 30
    rawCapture = PiRGBArray(camera,size=(480,320))

    time.sleep(0.1)


    for frame in camera.capture_continuous(rawCapture, format="rgb",use_video_port=True):
        
        image = frame.array
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face,rect = detect_face(gray)
        if face is not None:
            print( "Face Detected ")
            gray =draw_rectangle(rect,gray)
            predict(face,rect,gray,hists,labels,Names)
            
        cv2.imshow('video',gray)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        
        if key == ord("q"):
            break
        
        elif key == ord("c"):
            print( "capturing picture")
            name = "train data/Hung/" + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + ".png"
            print( name, type(name))
            cv2.imwrite(name,gray)
            
            

    cv2.destroyAllWindows()



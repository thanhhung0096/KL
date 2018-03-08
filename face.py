import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import os 
#function
face_cascade_path = "lbpcascade_frontalface.xml"
Names={"","s1","s2","Hung"}
def detect_face(gray):
    face_cascde = cv2.CascadeClassifier(face_cascade_path)
    faces = face_cascde.detectMultiScale(gray, scaleFactor=1.2,minNeighbors=5)
    if (len(faces) ==0):
        return None,None
    (x,y,w,h) = faces[0]
    return gray[y:y+w, x:x+h],faces[0]

def draw_rectangle(face):
    (x,y,w,h) =  face
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
            cv2.imshow("Training on image...", image)
            cv2.waitKey(100)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            rect,face = detect_face(gray)
            if face is not None:
                #save
                path ="Faces/"+folder+"/"+img
                print "save face to "+path
                cv2.imwrite(path,face)
##                print type(face)
                labels.append(label)
                faces.append(face)
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            cv2.destroyAllWindows()
    return faces,labels
def draw_name(img,name,x,y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

def predict(face,gray,reconizer):
    label,confidence =reconizer.predict(face)
    (x,y,w,h) = face
    text = "{},{}".format(Names[label],confidence)
    draw_name(gray,text,x,y)
    
if __name__ == "__main__":
    
    faces,labels = extract_data_training()
    
    recognizer = cv2.createLBPHFaceRecogizer()
    recognizer.train(faces,np.array(labels))
    
    
      
    count = 1


    camera = PiCamera()
    camera.resolution = (480,320)
    camera.brightness = 65
    camera.framerate = 30
    rawCapture = PiRGBArray(camera,size=(480,320))

    time.sleep(0.1)


    for frame in camera.capture_continuous(rawCapture, format="rgb",use_video_port=True):
        
        image = frame.array
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rect,face = detect_face(gray)
        if face is not None:
            print "Face Detected "
            draw_rectangle(face)
            predict(face,gray,recognizer)
            
        cv2.imshow('video',gray)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        
        if key == ord("q"):
            break
        
        elif key == ord("c"):
            print "capturing picture"
            name = "train data/s3/{}.png".format(count)
            cv2.imwrite(name,gray)
            count+=1
            

    cv2.destroyAllWindows()
    


# Import Libraries
import cv2,os
import numpy as np
from PIL import Image
import base64
from Adafruit_IO import Client
from send3 import send
import time,requests
#import RPi.GPIO as r
#from RPLCD.gpio import CharLCD
'''
# Settings of LCD
r.setmode(r.BOARD)
r.setwarnings(False)
r.setup(37,r.OUT)
r.setup(35,r.OUT)
r.setup(33,r.OUT)
r.setup(31,r.OUT)
r.setup(29,r.OUT)
r.setup(23,r.OUT)

r.output(37,1)
r.output(35,1)

lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23], numbering_mode=r.BOARD)
lcd.cursor_pos=(0,0)

'''

# Connecting to the server
aio = Client('Devil927','c91525ae446a4d19b1679df2325d9382')
# Classifier for Face Detection 
face_clff=cv2.CascadeClassifier('/home/rashu/Desktop/final_Project/face.xml')

# Classifier for Face Recognition
rec=cv2.face.LBPHFaceRecognizer_create()

# Path for the Database 
img_paths = [os.path.join('/home/rashu/Desktop/final_Project/dataset',f1) for f1 in os.listdir('/home/rashu/Desktop/final_Project/dataset')]
faces=[]
ids=[]

# Fetching Data from Dataset
for i in img_paths:
    n=cv2.imread(i)
    n=cv2.cvtColor(n,cv2.COLOR_BGR2GRAY)
    n=np.array(n,'uint8')
    face2 = face_clff.detectMultiScale(n, minNeighbors=5, scaleFactor=1.1)
    for x, y, w, h in face2:
        faces.append(n[y:y+w,x:x+h])
        ids.append(int(i.split('.')[1]))
        
# Train the Recognizer
rec.train(faces,np.array(ids))

# Pause time for training
time.sleep(2)

while True:
    if 'ON' in aio.data('new-feed')[0][3]:
        aio.send_data('new-feed','OFF')
        # Start the live feed
        cap=cv2.VideoCapture(0)
        _,f=cap.read()
        lcd.write_string(u'Welcome Sir')
        f=0
        while True:
            _,f=cap.read()
            time.sleep(0.1)
            print(f)
            img=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
            # Detecting the face in real time
            face=face_clff.detectMultiScale(img,minNeighbors=5,scaleFactor=1.1)
            id=0
            w=0
            # Making Box arround the Face
            for x,y,w,h in face:
                f=cv2.rectangle(f,(x,y),(x+w,y+h),(0,255,10),2)
                img=cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,10),2)
                f2=img[y:y+h,x:x+w]
                # Predict The face
                id,conf=rec.predict(f2)
                
                global x1,y1
                x1=x
                y1=y
                font = cv2.FONT_HERSHEY_SIMPLEX
                j=str(id ) if id!=3 else  'Rashu'
                # Putting an label over recognised image
                if conf>40 and id!=0 and id !=None:
                    f=cv2.putText(f,"Hello " +j ,(x+50,y+50),font,1,(0,0,255),2,cv2.LINE_AA)
                else:
                    f=cv2.putText(f,"Hello Stranger",(x+50,y+50),font,1,(0,0,255),2,cv2.LINE_AA) 
                # Saving and Sending Image to the Server
                cv2.imwrite('image.jpg',f)
                send('image.jpg')
                break
            # Showing The live Feed
            cv2.imshow('frame',f)
            
            k=cv2.waitKey(1)
            
            if w>=20:
                break
    ''' lcd.clear()
        time.sleep(3)
        url='https://api.thingspeak.com/channels/526652/feeds.json?api_key=6UCD2FUMVIZCXJNN&results=2'
        k=requests.get(url)
        if k.content.decode('utf-8')[-5]==0:
            lcd.write_string(u'Wait for \n some time')
        time.sleep(1)
        lcd.clear()
        time.sleep(1)
        if k.content.decode('utf-8')[-5]==0:
            lcd.write_string(u'Owner unreachable\n come tommorrow')
        elif k.content.decode('utf-8')[-5]==1:
            lcd.write_string(u'Open The Door')
            time.sleep(1)
            lcd.write_string(u'Welcome In Sir')
            requests.get('https://api.thingspeak.com/update?api_key=0VK1SZAJ8C8WT76K&field1=0')
            time.sleep(1)
            lcd.write_string(u'Clossing Door')
        else:
            lcd.write_string(u'Permission\n Denied')
        time.sleep(2)
        lcd.clear()
        
        
        cv2.destroyAllWindows()
'''

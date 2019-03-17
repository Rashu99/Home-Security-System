# Import Libraries
from Adafruit_IO import Client
from PIL import Image
import base64
import cv2


def send(k):
    # Connecting to the Server
    aio = Client('Devil927','c91525ae446a4d19b1679df2325d9382')
    BASE_DIR='./data/'
    SRC_FILE=BASE_DIR+k
    DST_FILE=BASE_DIR+'lastsmall.jpg'
    
    fd_img = open(SRC_FILE, 'r')
    img = Image.open(fd_img)
    size = 320, 240
    img.thumbnail(size)
    img.save(DST_FILE, img.format)
    fd_img.close()
     
    with open(DST_FILE, "rb") as imageFile:
        str = base64.b64encode(imageFile.read())
    import requests
    requests.get('https://api.thingspeak.com/update?api_key=0VK1SZAJ8C8WT76K&field1='+str)
    aio.send('img', str )

#send('image.jpg')

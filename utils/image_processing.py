import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64

def decode_image(image_data):
    header, encoded = image_data.split(',', 1)
    img_data = base64.b64decode(encoded)
    img = Image.open(BytesIO(img_data))
    return np.array(img)

def detect_faces(img_array):
    gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

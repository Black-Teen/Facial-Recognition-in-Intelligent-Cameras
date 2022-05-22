import os
from PIL import Image
import numpy as np
import cv2
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR,"images")

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
name_id = 0
labels_id = {}
labels = []

c_train = []


for root,dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith('png') or file.endswith('jpg') or  file.endswith('JPG'):
            path = os.path.join(root,file)
            label = os.path.basename(os.path.dirname(path)).replace(" ","-").lower()
            #print(label, path)
            if not label in labels_id:
                labels_id[label] = name_id
                name_id +=1
            id_ = labels_id[label]
            #print(labels_id)
            t_image = Image.open(path).convert("L")
            size = (550,550)
            final_image = t_image.resize(size,Image.ANTIALIAS)
            image_array = np.array(final_image, "uint8")
            faces = face_cascade.detectMultiScale(image_array ,
                                        scaleFactor=1.1,
                                        minNeighbors=5,
                                        minSize=(60, 60),
                                        flags=cv2.CASCADE_SCALE_IMAGE)
            for (x,y,w,h) in faces:
                roi_gray = image_array[y:y+h, x:x+w]
                c_train.append(roi_gray)
                labels.append(id_)
#print(c_train)
#print(labels)
with open ("labels.pickle", 'wb') as f:
    pickle.dump(labels_id, f)

recognizer.train(c_train,np.array(labels))
recognizer.save("trainer.yml")
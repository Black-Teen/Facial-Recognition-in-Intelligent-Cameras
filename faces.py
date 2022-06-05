# OpenCV program to detect face in real time
# import libraries of python OpenCV
import cv2
import os
import time
import pickle
from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2
from flask import g
import imutils



def start():
	show_frame()




# load the required trained XML classifiers

def show_frame():

	global cap
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	eye_classifier = cv2.CascadeClassifier('haarcascade_eye.xml')

	recognizer = cv2.face.LBPHFaceRecognizer_create()
	# capture frames from a camera
	recognizer.read("trainer.yml")
	cap = cv2.VideoCapture(0)

	frame_width = int(cap.get(3))
	frame_height = int(cap.get(4))
	
	size = (frame_width, frame_height)

	if (cap.isOpened() == False): 
		print("Error reading video file")



	# loop runs if capturing has been initialized.
	labels_dict = {}
	with open ("labels.pickle", 'rb') as f:
		og_labels_dict = pickle.load(f)
		labels_dict = {v:k for k,v in og_labels_dict.items()}

	result = cv2.VideoWriter('videodatabase/filename.avi', 
							cv2.VideoWriter_fourcc(*'MJPG'),
							10, size)

	vid_key = 0
		# reads frames from a camera
	current_time = time.time()
		
	while True:
		ret, img = cap.read()
		ret, frame = cap.read()
		updated_time = time.time()
		local_time = time.ctime(updated_time)
		if ret == True: 
			if updated_time - current_time > 10:
				current_time = updated_time
				new_date =str(local_time).replace(":", "-")
				filename = 'videodatabase/video_time_int/'+'Camera_rec '+new_date
				result = cv2.VideoWriter(filename+'.avi', 
								cv2.VideoWriter_fourcc(*'MJPG'),
								10, size)
			result.write(img)
		# convert to gray scale of each frames
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# Detects faces of different sizes in the input image
		faces = face_cascade.detectMultiScale(gray,
											scaleFactor=1.1,
											minNeighbors=5,
											minSize=(60, 60),
											flags=cv2.CASCADE_SCALE_IMAGE)

		for (x,y,w,h) in faces:
			# To draw a rectangle in a face
			cv2.rectangle(img, (x, y), (x + w, y + h),(0,255,0), 2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = img[y:y+h, x:x+w]

			#recognizer
			id_, conf = recognizer.predict(roi_gray)

			if conf >= 45:# and conf < 90:
				print(id_)
				print(labels_dict[id_])
				font =  cv2.FONT_HERSHEY_SIMPLEX
				name = labels_dict[id_]
				color = (255,255,255)
				stroke = 2
				cv2.putText(img,name,(x,y),font,1,color,stroke,cv2.LINE_AA)


			img_item = "my_image.png"
			cv2.imwrite(img_item,roi_gray)

			eyes=eye_classifier.detectMultiScale(roi_gray)
			# drawing_eyes_rectangles
			for (ex,ey,ew,eh) in eyes:
				cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,255,0),2)



		img1 = imutils.resize(img, width=640)
		im = Image.fromarray(img1)
		mg = ImageTk.PhotoImage(image=im)

		lblVideo.configure( image=mg, text="Why are doing this" )
		lblVideo.image= mg
		print(lblVideo.image)
		lblVideo. after ( 10 ,show_frame )	

		cv2.imshow('img',img)

	# Wait for Esc key to stop
		k = cv2.waitKey(30) & 0xff
		if k == 27:
			break


def finish():
	global cap
	cap.release()



cap = None

root = Tk ()


btnStart = Button ( root, text= "Start" , width= 45 , command=start )
btnStart. grid ( column= 0 , row= 0 , padx= 5 , pady= 5 )		

btnFinish = Button ( root, text= "Finish" , width= 45 , command=finish)
btnFinish. grid ( column= 1 , row= 0 , padx= 5 , pady= 5 )
lblVideo = Label ( root )
lblVideo. grid ( column= 0 , row= 1 , columnspan= 2 )

root.mainloop()



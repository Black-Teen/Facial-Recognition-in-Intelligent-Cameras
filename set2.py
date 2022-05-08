# OpenCV program to detect face in real time
# import libraries of python OpenCV
import cv2
import os
import time

# load the required trained XML classifiers
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# capture frames from a camera
cap = cv2.VideoCapture(0)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
   
size = (frame_width, frame_height)

if (cap.isOpened() == False): 
    print("Error reading video file")

# loop runs if capturing has been initialized.


result = cv2.VideoWriter('videodatabase/filename.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)

current_time = time.time()
vid_key = 0
while True:


	# reads frames from a camera
	ret, img = cap.read()
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

	# Display an image in a window
	cv2.imshow('img',img)

	# Wait for Esc key to stop
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

# Close the window
cap.release()
result.release()

cv2.destroyAllWindows()

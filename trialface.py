from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2
import imutils

def start () :
    global cap
    cap = cv2. VideoCapture ( 0 , cv2.CAP_DSHOW )
    display ()
    
def display():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, display)
        else:
            lblVideo.image = ""
            cap.release()

def finish():
    global cap
    cap.release()

cap = None
root = Tk ()
btnStart = Button ( root, text= "Start" , width= 45 , command=start )
btnStart. grid ( column= 0 , row= 0 , padx= 5 , pady= 5 )
btnFinish = Button ( root, text= "Finish" , width= 45 , command=finish )
btnFinish. grid ( column= 1 , row= 0 , padx= 5 , pady= 5 )
lblVideo = Label ( root )
lblVideo. grid ( column= 0 , row= 1 , columnspan= 2 )
root. mainloop ()


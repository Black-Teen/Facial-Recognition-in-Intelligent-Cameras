from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import pickle
import time
import threading
import pyautogui
import numpy as np
import face_recognition
import os
import smtplib
import time
import email
from twilio.rest import Client
import tkinter.messagebox

newim_no = 0
newuserpath= " "

known_face_encodings = [

]
known_face_names = [

]

unknown_faces = []

cap = cv2. VideoCapture ( 0 , cv2.CAP_DSHOW )

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

video_cap = cap
            
size = (frame_width, frame_height)

train_dir = os.listdir("Faces")
for person in train_dir:
    pix = os.listdir(f'Faces/{person}')
    for person_img in pix:
        face = face_recognition.load_image_file(f"Faces/{person}/{person_img}")
        face_bounding_boxes = face_recognition.face_locations(face)
        if len(face_bounding_boxes) == 1:
            face_enc = face_recognition.face_encodings(face)[0]
            known_face_encodings.append(face_enc)
            known_face_names.append(person)
        else:
            print(f'{person}/{person_img} cannot be used for face encoding')

# Create arrays of known face encodings and their names


# Initialize some variables
face_locations = []

face_encodings = []
face_names = []
process_this_frame = True

result = cv2.VideoWriter('videodatabase/filename.avi',cv2.VideoWriter_fourcc(*'MJPG'),10, size)




current_time = time.time()

def input_video () :
    global cap
    
    if selected. get () == 1 :
        path_video = filedialog. askopenfilename ( filetypes = [
            ( "all video format" , ".mp4" ) ,
            ( "all video format" , ".avi" )])
        if len ( path_video ) > 0 :   
            btnEnd. configure ( state= "active" )
            buttScreen.configure ( state= "active" )
            rad1. configure ( state= "disabled" )
            rad2. configure ( state= "disabled" )
            pathInputVideo = "..." + path_video [ -20 : ]
            lblInfoVideoPath. configure ( text=pathInputVideo )
            cap = cv2. VideoCapture ( path_video )
            display ()
    if selected. get () == 2 :
        btnEnd. configure ( state= "active" )
        buttScreen.configure ( state= "active" )
        rad1. configure ( state= "disabled" )
        rad2. configure ( state= "disabled" )
        lblInfoVideoPath. configure ( text= "" )
        cap=video_cap
        display ()


def display () :
    global cap
    global current_time
    global size
    global result
    global to_screen
    ret, frame = cap. read ()
    to_screen = frame
    updated_time = time.time()
    local_time = time.ctime(updated_time)
   

    if ret == True :
        if updated_time - current_time > 10:
     
            
            current_time = updated_time
            new_date =str(local_time).replace(":", "-")
            filename = 'videodatabase/video_time_int/'+'Camera_rec '+new_date
            result = cv2.VideoWriter(filename+'.avi', cv2.VideoWriter_fourcc(*'MJPG'),10, size)
        result.write(frame)
        frame = imutils. resize ( frame, width= 640 )
        frame = easy_detection ( frame )
        frame = cv2. cvtColor ( frame, cv2.COLOR_BGR2RGB )
        im = Image. fromarray ( frame )
        img = ImageTk. PhotoImage ( image=im )
        lblVideo. configure( image=img )
        lblVideo. image = img
        lblVideo. after ( 10 , display )
    else :
        lblVideo. image = ""
        lblInfoVideoPath. configure ( text= "" )
        rad1. configure ( state= "active" )
        rad2. configure ( state= "active" )
        selected. set ( 0 )
        btnEnd. configure ( state= "disabled" )
        chap. release ()
  


def easy_detection ( frame ) :
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            else:
                img_item = "unknownface.png"
                cv2.imwrite(img_item,frame)
                def sendmail(imname):
                    ################# SMTP SSL ################################
                    start = time.time()
                    try:
                        smtp_ssl = smtplib.SMTP_SSL(host="smtp.mail.yahoo.com", port=465)
                    except Exception as e:
                        print("ErrorType : {}, Error : {}".format(type(e).__name__, e))
                        smtp_ssl = None

                    print("Connection Object : {}".format(smtp_ssl))
                    print("Total Time Taken  : {:,.2f} Seconds".format(time.time() - start))

                    ######### Log In to mail account ############################
                    print("\nLogging In.....")
                    resp_code, response = smtp_ssl.login(user="juanpombe@yahoo.com", password="giioypwrjesqekon")

                    print("Response Code : {}".format(resp_code))
                    print("Response      : {}".format(response.decode()))

                    ################ Send Mail ########################
                    print("\nSending Mail..........")

                    message = email.message.EmailMessage()

                    message["From"] = "juanpombe@yahoo.com"
                    message["To"] = ["kagwepeter07@gmail.com", ]
                    message["cc"] = ["pkagwe07.2309@gmail.com",]
                    message["Bcc"] = ["kariukipeter46@yahoo.com", ]

                    message["Subject"] =  "Mail with attachments"

                    body = '''
                    Hello All,

                    Please find attached file.

                    Regards,
                    CoderzColumn
                    '''
                    message.set_content(body)

                    ### Attach JPEG Image.
                    with open(imname, mode="rb") as fp:
                        img_content = fp.read()
                        message.add_attachment(img_content, maintype="image", subtype="jpeg", filename="kalam.jpeg")

                    ### Send Message
                    response = smtp_ssl.send_message(msg=message)

                    print("List of Failed Recipients : {}".format(response))

                    ######### Log out to mail account ############################
                    print("\nLogging Out....")
                    resp_code, response = smtp_ssl.quit()

                    print("Response Code : {}".format(resp_code))
                    print("Response      : {}".format(response.decode()))

                    account_sid = os.environ['TWILIO_ACCOUNT_SID'] = 'AC6258d8972ac6c28e95d07a0c18fe6506'
                    auth_token = os.environ['TWILIO_AUTH_TOKEN'] = '5b9edd6bba20d167ae34617b47bf9fd1'
                    client = Client(account_sid, auth_token)

                    message = client.messages \
                        .create(
                             body='Please check your email, an intruder has been detected',
                             from_='+19895107791',
                             to='+254707801908'
                         )

                    print(message.sid)

                if len(unknown_faces) == 0:

                    unknown_faces.append(face_encoding)
                    print("Intruder Detected");
                    sendmail(img_item)

                else:
                    matches1 = face_recognition.compare_faces(unknown_faces, face_encoding)
                    face_distances1 = face_recognition.face_distance(unknown_faces, face_encoding)
                    best_match_index1 = np.argmin(face_distances1)
                    if matches1[best_match_index1]:
                        print("Reported")
                    else:
                        unknown_faces.append(face_encoding)
                        print("Intruder Detected");
                        sendmail(img_item)
                                                              
            face_names.append(name)

    


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    return frame

def takeScreenShot():
    global to_screen
    cv2.imwrite("in_memory_to_disk.png", to_screen)

def finish_cleanup () :
    lblVideo. image = ""
    lblInfoVideoPath. configure ( text= "" )
    rad1. configure ( state= "active" )
    rad2. configure ( state= "active" )
    selected. set( 0 )
    result.write(frame)
    chap. release ()
    
def adduser():


    def input_Image () :
        global cap
        
        if selected.get()==3:
            path_video = filedialog. askopenfilename ( filetypes = [
                ( "all video format" , ".mp4" ) ,
                ( "all video format" , ".avi" )])
            if len ( path_video ) > 0 :   
                buttScreens.configure ( state= "active" )
                buttCreateuser.configure ( state= "active" )
                rad1. configure ( state= "disabled" )
                rad2. configure ( state= "disabled" )
                pathInputVideo = "..." + path_video [ -20 : ]
                cap = cv2. VideoCapture ( path_video )
        if selected.get()== 4 :
            buttScreens.configure ( state= "active" )
            buttCreateuser.configure ( state= "active" )
            rad1. configure ( state= "disabled" )
            rad2. configure ( state= "disabled" )
            cap=video_cap
            openCamera()

        
    def openCamera():
         global cap
         global framez
         
         if cap is not None:
             ret, frame1 = cap.read()
             framez = frame1
             if ret == True:
                frame1 = imutils.resize(frame1, width=640)
                frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
                im1 = Image.fromarray(frame1)
                img1 = ImageTk.PhotoImage(image=im1)
                lblVideo1.configure(image=img1)
                lblVideo1.image = img1
                lblVideo1.after(10, openCamera)
             else:
                lblVideo1.image = ""
                cap.release()
    def get_folder_name():
        global newuserpath
        name1=e1.get()
        name2=e2.get()
        folder_name = name1+ "-" + name2
        cwd = os.getcwd()
        path = os.path.join(cwd ,"Faces")
        createfolder =os.path.join(path,folder_name)

        if not os.path.exists(createfolder):
            os.mkdir(createfolder)
            tkinter.messagebox.showinfo("Done.",  "Crated new user  " + folder_name + "   Please take screenshots of the user profile picture")
            newuserpath=createfolder
        else:
            tkinter.messagebox.showinfo("Try again.",  "A user with that named " + folder_name +  "already exists!")
            print("A user with that name already exists!")
        

    def takeUserScreenShot():
        global newim_no
        imname= "image"+str(newim_no)+".png"
        if newuserpath != " ":
            path = newuserpath
            cv2.imwrite(os.path.join(path , imname), framez)
            newim_no +=1
        else:
            tkinter.messagebox.showinfo("Try again",  "No new user created")
        
         
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("Add user")
 
    # sets the geometry of toplevel
    
 
    # A Label widget to show in toplevel)
    lblInfo3 = Label ( newWindow, text= "Add users recognized by system" , font= "bold" )
    lblInfo3. grid ( column= 0 , row= 0 ,pady=10, padx =5)

    lblInfo4 =  Label(newWindow, text="First Name:")
    lblInfo5 =  Label(newWindow, text="Last Name:")

    lblInfo4. grid ( row= 3,pady=5)
    lblInfo5. grid ( row= 4,pady=5)

    e1 = Entry(newWindow,width= 40 )
    e2 = Entry(newWindow,width= 40  )

    e1.grid(row=3, column=1)
    e2.grid(row=4, column=1)

    buttCreateuser = Button ( newWindow, text= "Register user" ,width= 20 , state= "disabled" , command=get_folder_name )
    buttCreateuser.grid ( column= 1 , row= 5  ,  padx =10 )

    rad3 = Radiobutton ( newWindow, text= "Take screenshots from video" , width= 40 , value= 3 , variable=selected, command=input_Image )
    rad4 = Radiobutton ( newWindow, text= "Take screnshots from camera" , width= 40 , value= 4 , variable=selected, command=input_Image )
    rad3. grid ( column= 0 , row= 6 , pady=10, padx =20)
    rad4. grid ( column= 1 , row= 6, pady=10, padx =20 )

    lblVideo1 = Label ( newWindow )
    lblVideo1. grid ( column= 0 , row= 7 , columnspan= 2 )
    buttScreens = Button ( newWindow, text= "Take screen shot" ,width= 20 , state= "disabled" , command=takeUserScreenShot )
    buttScreens . grid ( column= 0 , row= 8  ,  padx =10 )

cap = None
root = Tk ()
root.title(" facial recognition system")
lblInfo1 = Label ( root, text= "Facial Recodnition System" , font= "bold" )
lblInfo1. grid ( column= 0 , row= 0 , columnspan= 2 )

lblInfo2 = Label ( root, text= "Select the video input")
lblInfo2. grid ( column= 0 , row= 1 , columnspan= 2 )


selected = IntVar ()
rad1 = Radiobutton ( root, text= "Choose video" , width= 20 , value= 1 , variable=selected, command=input_video )
rad2 = Radiobutton ( root, text= "Live Video" , width= 20 , value= 2 , variable=selected, command=input_video )
rad1. grid ( column= 0 , row= 2 , pady=20, padx =10)
rad2. grid ( column= 1 , row= 2, pady=20, padx =10 )

btnUser = Button ( root, text= "Add user" , width= 20 , command=adduser )
btnUser. grid ( column= 2 , row= 2  , pady=20, padx =10 )


lblInfoVideoPath = Label ( root, text= "" , width= 20,)
lblInfoVideoPath. grid ( column= 0 , row= 3 )
lblVideo = Label ( root , borderwidth=5, relief="ridge")
lblVideo. grid ( column= 0 , row= 4 , columnspan= 2 )
buttScreen = Button ( root, text= "Take screen shot" ,width= 20 , state= "disabled" , command=takeScreenShot )
buttScreen . grid ( column= 0 , row= 5  ,  padx =10 )
btnEnd = Button ( root, text= "End display and cleanup" , width= 20 ,state= "disabled" , command=finish_cleanup )
btnEnd. grid ( column= 1 , row= 5  , pady=20, padx =10 )
root. mainloop ()

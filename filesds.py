import os
cwd = os.getcwd()
path = os.path.join(cwd ,"dlib\Faces")
createfolder =os.path.join(path,"Musa")

if not os.path.exists(createfolder):
    os.mkdir(createfolder)
    print("Directory created!")

   

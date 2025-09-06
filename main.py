############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

##################################################################################

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)

###################################################################################

def contact():
    mess._show(title='Contact us', message="Please contact us on : 'xxxxxxxxxxxxx@gmail.com' ")

###################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

###################################################################################

def save_pass():
    try:
        # Create directory if it doesn't exist
        os.makedirs("TrainingImageLabel", exist_ok=True)
        
        # Get the password file path
        password_file = os.path.join("TrainingImageLabel", "psd.txt")
        
        # Check if password file exists
        if os.path.isfile(password_file):
            with open(password_file, "r") as tf:
                key = tf.read().strip()
        else:
            master.destroy()
            new_pas = tsd.askstring('New Password', 'Please enter a new password below', show='*')
            if new_pas is None or new_pas.strip() == "":
                mess._show(title='No Password Entered', message='Password not set!! Please try again')
                return
            with open(password_file, "w") as tf:
                tf.write(new_pas.strip())
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return

        # Get entered passwords
        op = old.get().strip()
        newp = new.get().strip()
        nnewp = nnew.get().strip()

        # Validate old password
        if op != key:
            mess._show(title='Wrong Password', message='Please enter correct old password.')
            return

        # Validate new password
        if not newp:
            mess._show(title='Error', message='New password cannot be empty!')
            return

        # Check if new passwords match
        if newp != nnewp:
            mess._show(title='Error', message='New passwords do not match!')
            return

        # Save new password
        with open(password_file, "w") as txf:
            txf.write(newp)
        
        mess._show(title='Success', message='Password changed successfully!!')
        master.destroy()

    except Exception as e:
        mess._show(title='Error', message=f'An error occurred: {str(e)}')
        if 'master' in globals():
            master.destroy()

###################################################################################

def change_pass():
    global master, old, new, nnew
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    
    # Create and place widgets
    lbl4 = tk.Label(master, text='    Enter Old Password', bg='white', font=('times', 12, ' bold '))
    lbl4.place(x=10, y=10)
    
    old = tk.Entry(master, width=25, fg="black", relief='solid', font=('times', 12, ' bold '), show='*')
    old.place(x=180, y=10)
    
    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    
    new = tk.Entry(master, width=25, fg="black", relief='solid', font=('times', 12, ' bold '), show='*')
    new.place(x=180, y=45)
    
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    
    nnew = tk.Entry(master, width=25, fg="black", relief='solid', font=('times', 12, ' bold '), show='*')
    nnew.place(x=180, y=80)
    
    # Buttons
    cancel = tk.Button(master, text="Cancel", command=master.destroy, fg="black", bg="red", 
                      height=1, width=25, activebackground="white", font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#3ece48", 
                     height=1, width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    
    # Center the window
    master.update_idletasks()
    width = master.winfo_width()
    height = master.winfo_height()
    x = (master.winfo_screenwidth() // 2) - (width // 2)
    y = (master.winfo_screenheight() // 2) - (height // 2)
    master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    master.mainloop()

#####################################################################################

def psw():
    try:
        # Create directory if it doesn't exist
        os.makedirs("TrainingImageLabel", exist_ok=True)
        
        # Get the password file path
        password_file = os.path.join("TrainingImageLabel", "psd.txt")
        
        # Check if password file exists
        if os.path.isfile(password_file):
            with open(password_file, "r") as tf:
                key = tf.read().strip()
        else:
            new_pas = tsd.askstring('New Password', 'Please enter a new password below', show='*')
            if new_pas is None or new_pas.strip() == "":
                mess._show(title='No Password Entered', message='Password not set!! Please try again')
                return
            with open(password_file, "w") as tf:
                tf.write(new_pas.strip())
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return

        # Get password from user
        password = tsd.askstring('Password', 'Enter Password', show='*')
        
        if password is None:
            return
        elif password.strip() == "":
            mess._show(title='Error', message='Password cannot be empty!')
            return
        elif password.strip() == key:
            TrainImages()
        else:
            mess._show(title='Wrong Password', message='You have entered wrong password')

    except Exception as e:
        mess._show(title='Error', message=f'An error occurred: {str(e)}')

######################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

#######################################################################################

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    
    # Create directories with proper error handling
    try:
        os.makedirs("StudentDetails", exist_ok=True)
        os.makedirs("TrainingImage", exist_ok=True)
    except Exception as e:
        mess._show(title='Error', message=f'Failed to create directories: {str(e)}')
        return

    serial = 0
    exists = os.path.isfile(os.path.join("StudentDetails", "StudentDetails.csv"))
    if exists:
        with open(os.path.join("StudentDetails", "StudentDetails.csv"), 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open(os.path.join("StudentDetails", "StudentDetails.csv"), 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()

    Id = (txt.get())
    name = (txt2.get())

    if not Id or not name:
        mess._show(title='Error', message='Please enter both ID and Name')
        return

    if ((name.isalpha()) or (' ' in name)):
        try:
            cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not cam.isOpened():
                mess._show(title='Error', message='Could not open camera. Please check if camera is connected.')
                return
                
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            if detector.empty():
                mess._show(title='Error', message='Failed to load face detector')
                return

            sampleNum = 0
            message1.configure(text="Taking Images... Press 'q' to quit")
            
            while (True):
                ret, img = cam.read()
                if not ret:
                    mess._show(title='Error', message='Failed to grab frame from camera')
                    break
                    
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    
                    # Create the full path for saving the image
                    image_path = os.path.join("TrainingImage", f"{name}.{serial}.{Id}.{sampleNum}.jpg")
                    
                    # Save the face image
                    try:
                        cv2.imwrite(image_path, gray[y:y + h, x:x + w])
                        print(f"Saved image: {image_path}")  # Debug print
                    except Exception as e:
                        print(f"Error saving image: {str(e)}")  # Debug print
                        continue
                    
                    # Display the frame with face detection
                    cv2.imshow('Taking Images', img)
                
                # Display sample count
                cv2.putText(img, f'Samples: {sampleNum}/100', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Taking Images', img)
                
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif sampleNum >= 100:
                    break
                    
            cam.release()
            cv2.destroyAllWindows()
            
            if sampleNum > 0:
                res = f"Images Taken for ID : {Id} ({sampleNum} samples)"
                row = [serial, '', Id, '', name]
                with open(os.path.join('StudentDetails', 'StudentDetails.csv'), 'a+') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
                csvFile.close()
                message1.configure(text=res)
            else:
                mess._show(title='Error', message='No face detected. Please try again.')
            
        except Exception as e:
            mess._show(title='Error', message=f'An error occurred: {str(e)}')
            if 'cam' in locals():
                cam.release()
            cv2.destroyAllWindows()
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)

########################################################################################

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################

def TrackImages():
    try:
        check_haarcascadefile()
        
        # Create required directories
        os.makedirs("Attendance", exist_ok=True)
        os.makedirs("StudentDetails", exist_ok=True)
        
        # Clear existing attendance display
        for k in tv.get_children():
            tv.delete(k)
            
        # Initialize variables
        msg = ''
        i = 0
        j = 0
        
        # Initialize face recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Check if training data exists
        trainer_path = os.path.join("TrainingImageLabel", "Trainner.yml")
        if not os.path.isfile(trainer_path):
            mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
            return
            
        # Load the trained model
        recognizer.read(trainer_path)
        
        # Initialize face detector
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)
        if faceCascade.empty():
            mess._show(title='Error', message='Failed to load face detector')
            return
            
        # Initialize camera
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cam.isOpened():
            mess._show(title='Error', message='Could not open camera. Please check if camera is connected.')
            return
            
        # Set up font for display
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Define attendance columns
        col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
        
        # Check if student details exist
        student_details_path = os.path.join("StudentDetails", "StudentDetails.csv")
        if not os.path.isfile(student_details_path):
            mess._show(title='Details Missing', message='Students details are missing, please check!')
            cam.release()
            cv2.destroyAllWindows()
            return
            
        try:
            # Read student details
            df = pd.read_csv(student_details_path)
        except Exception as e:
            mess._show(title='Error', message=f'Failed to read student details: {str(e)}')
            cam.release()
            cv2.destroyAllWindows()
            return
            
        # Get current date for attendance file
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
        attendance_file = os.path.join("Attendance", f"Attendance_{date}.csv")
        
        # Create attendance file if it doesn't exist
        if not os.path.isfile(attendance_file):
            with open(attendance_file, 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(col_names)
        
        # Read existing attendance records
        attendance_records = set()
        if os.path.isfile(attendance_file):
            try:
                with open(attendance_file, 'r') as csvFile1:
                    reader = csv.reader(csvFile1)
                    next(reader)  # Skip header
                    for row in reader:
                        if row:  # Check if row is not empty
                            attendance_records.add(row[0])  # Add ID to set
            except Exception as e:
                print(f"Error reading attendance file: {str(e)}")
        
        message1.configure(text="Taking Attendance... Press 'q' to quit or click 'Save & Close'")
        
        # Create a window for the camera feed
        cv2.namedWindow('Taking Attendance', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Taking Attendance', 800, 600)
        
        # Flag to control the main loop
        running = True
        
        # Dictionary to track marked attendance in current session
        session_attendance = set()
        
        def save_and_close():
            nonlocal running
            running = False
            try:
                # Release camera
                if cam.isOpened():
                    cam.release()
                
                # Close all OpenCV windows
                cv2.destroyAllWindows()
                
                # Update main window message
                message1.configure(text="Attendance Completed")
                
                # Show success message
                mess._show(title='Success', message='Attendance saved successfully!')
            except Exception as e:
                print(f"Error in save_and_close: {str(e)}")
        
        # Add Save & Close button to the main window
        save_button = tk.Button(frame1, text="Save & Close", command=save_and_close,
                              fg=TEXT_COLOR, bg=ACCENT_COLOR, width=35, height=1,
                              activebackground=BUTTON_HOVER, activeforeground=TEXT_COLOR,
                              font=('Helvetica', 15, 'bold'), relief='flat',
                              cursor='hand2')
        save_button.place(x=30, y=400)  # Place it below the Take Attendance button
        
        # Set start time for 10-second timer
        start_time = time.time()
        attendance_marked = False  # Flag to track if attendance was marked
        
        while running:
            # Check if 10 seconds have passed
            if time.time() - start_time >= 10:
                if attendance_marked:
                    # Show success message after 10 seconds
                    mess._show(title='Success', message='Attendance marked successfully!')
                    # Close camera and windows
                    running = False
                    if cam.isOpened():
                        cam.release()
                    cv2.destroyAllWindows()
                    message1.configure(text="Attendance Completed")
                    break
                else:
                    # If no attendance was marked in 10 seconds, show message and close
                    mess._show(title='No Attendance', message='No attendance marked in 10 seconds')
                    running = False
                    if cam.isOpened():
                        cam.release()
                    cv2.destroyAllWindows()
                    message1.configure(text="Attendance Completed")
                    break
                
            ret, im = cam.read()
            if not ret:
                mess._show(title='Error', message='Failed to grab frame from camera')
                break
                
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            # Optimize face detection parameters
            faces = faceCascade.detectMultiScale(gray, 1.1, 4, minSize=(30, 30))
            
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
                
                try:
                    # Recognize face
                    serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
                    
                    if conf < 50:  # Lower confidence threshold for better recognition
                        # Get student details
                        student_info = df[df['SERIAL NO.'] == serial]
                        if not student_info.empty:
                            name = student_info['NAME'].values[0]
                            id = student_info['ID'].values[0]
                            
                            # Check if already marked present in current session or previous sessions
                            if id not in attendance_records and id not in session_attendance:
                                # Mark attendance
                                ts = time.time()
                                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                                
                                attendance = [str(id), '', str(name), '', str(date), '', str(timeStamp)]
                                
                                # Save attendance
                                with open(attendance_file, 'a+') as csvFile1:
                                    writer = csv.writer(csvFile1)
                                    writer.writerow(attendance)
                                
                                # Update display
                                tv.insert('', 0, text=str(id), values=(str(name), str(date), str(timeStamp)))
                                
                                # Add to both attendance records
                                attendance_records.add(id)
                                session_attendance.add(id)
                                
                                # Display success message on video feed
                                cv2.putText(im, f"Attendance Marked: {name}", (x, y + h + 20), 
                                          font, 0.7, (0, 255, 0), 2)
                                
                                # Set attendance marked flag
                                attendance_marked = True
                                
                            else:
                                cv2.putText(im, f"Already Marked: {name}", (x, y + h + 20), 
                                          font, 0.7, (255, 0, 0), 2)
                        else:
                            cv2.putText(im, "Unknown", (x, y + h + 20), font, 0.7, (0, 0, 255), 2)
                    else:
                        cv2.putText(im, "Unknown", (x, y + h + 20), font, 0.7, (0, 0, 255), 2)
                except Exception as e:
                    print(f"Error processing face: {str(e)}")
                    cv2.putText(im, "Error", (x, y + h + 20), font, 0.7, (0, 0, 255), 2)
            
            # Display the frame
            cv2.imshow('Taking Attendance', im)
            
            # Break loop on 'q' press
            if cv2.waitKey(1) == ord('q'):
                running = False
                break
                
        # Cleanup
        if cam.isOpened():
            cam.release()
        cv2.destroyAllWindows()
        message1.configure(text="Attendance Completed")
        
    except Exception as e:
        mess._show(title='Error', message=f'An error occurred: {str(e)}')
        if 'cam' in locals() and cam.isOpened():
            cam.release()
        cv2.destroyAllWindows()

###########################################################################################

def clear_all_data():
    try:
        # Directories to clear
        directories = [
            "TrainingImage",
            "TrainingImageLabel",
            "StudentDetails",
            "Attendance"
        ]
        
        # Clear each directory
        for directory in directories:
            if os.path.exists(directory):
                for file in os.listdir(directory):
                    file_path = os.path.join(directory, file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Error deleting {file_path}: {str(e)}")
        
        # Clear the attendance display
        for k in tv.get_children():
            tv.delete(k)
            
        # Update messages
        message1.configure(text="1)Take Images  >>>  2)Save Profile")
        message.configure(text="Total Registrations till now  : 0")
        
        mess._show(title='Success', message='All data has been cleared successfully!')
        
    except Exception as e:
        mess._show(title='Error', message=f'An error occurred while clearing data: {str(e)}')

######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

######################################## GUI FRONT-END ###########################################

# Define colors
BG_COLOR = '#1a1a1a'  # Dark background
FRAME_COLOR = '#2d2d2d'  # Slightly lighter dark
BUTTON_COLOR = '#404040'  # Button background
BUTTON_HOVER = '#505050'  # Button hover
TEXT_COLOR = '#ffffff'  # White text
ACCENT_COLOR = '#00ff00'  # Green accent
ERROR_COLOR = '#ff0000'  # Red for errors
SUCCESS_COLOR = '#00ff00'  # Green for success

window = tk.Tk()
window.geometry("1280x720")
window.resizable(True,False)
window.title("Attendance System")
window.configure(background=BG_COLOR)

frame1 = tk.Frame(window, bg=FRAME_COLOR)
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg=FRAME_COLOR)
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Face Recognition Based Attendance System",
                   fg=TEXT_COLOR, bg=BG_COLOR, width=55, height=1,
                   font=('Helvetica', 29, 'bold'))
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg=FRAME_COLOR)
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg=FRAME_COLOR)
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text=f"{day}-{mont[month]}-{year}  |  ",
                fg=ACCENT_COLOR, bg=BG_COLOR, width=55, height=1,
                font=('Helvetica', 22, 'bold'))
datef.pack(fill='both', expand=1)

clock = tk.Label(frame3, fg=ACCENT_COLOR, bg=BG_COLOR, width=55, height=1,
                font=('Helvetica', 22, 'bold'))
clock.pack(fill='both', expand=1)
tick()

head2 = tk.Label(frame2, text="For New Registrations",
                fg=TEXT_COLOR, bg=FRAME_COLOR,
                font=('Helvetica', 17, 'bold'))
head2.grid(row=0, column=0, pady=10)

head1 = tk.Label(frame1, text="For Already Registered",
                fg=TEXT_COLOR, bg=FRAME_COLOR,
                font=('Helvetica', 17, 'bold'))
head1.place(x=0, y=0)

lbl = tk.Label(frame2, text="Enter ID", width=20, height=1,
              fg=TEXT_COLOR, bg=FRAME_COLOR,
              font=('Helvetica', 17, 'bold'))
lbl.place(x=80, y=55)

txt = tk.Entry(frame2, width=32, fg=TEXT_COLOR, bg=BUTTON_COLOR,
              font=('Helvetica', 15, 'bold'), insertbackground=TEXT_COLOR)
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="Enter Name", width=20,
               fg=TEXT_COLOR, bg=FRAME_COLOR,
               font=('Helvetica', 17, 'bold'))
lbl2.place(x=80, y=140)

txt2 = tk.Entry(frame2, width=32, fg=TEXT_COLOR, bg=BUTTON_COLOR,
               font=('Helvetica', 15, 'bold'), insertbackground=TEXT_COLOR)
txt2.place(x=30, y=173)

message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile",
                   bg=FRAME_COLOR, fg=TEXT_COLOR, width=39, height=1,
                   font=('Helvetica', 15, 'bold'))
message1.place(x=7, y=230)

message = tk.Label(frame2, text="", bg=FRAME_COLOR, fg=TEXT_COLOR,
                  width=39, height=1, font=('Helvetica', 16, 'bold'))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="Attendance", width=20,
               fg=TEXT_COLOR, bg=FRAME_COLOR, height=1,
               font=('Helvetica', 17, 'bold'))
lbl3.place(x=100, y=115)

# Style configuration for Treeview
style = ttk.Style()
style.configure("Treeview",
                background=FRAME_COLOR,
                foreground=TEXT_COLOR,
                rowheight=25,
                fieldbackground=FRAME_COLOR)
style.configure("Treeview.Heading",
                background=BUTTON_COLOR,
                foreground=TEXT_COLOR,
                relief="flat")
style.map("Treeview",
          background=[("selected", BUTTON_HOVER)],
          foreground=[("selected", TEXT_COLOR)])

tv = ttk.Treeview(frame1, height=13, columns=('name', 'date', 'time'),
                  style="Treeview")
tv.column('#0', width=82)
tv.column('name', width=130)
tv.column('date', width=133)
tv.column('time', width=133)
tv.grid(row=2, column=0, padx=(0, 0), pady=(150, 0), columnspan=4)
tv.heading('#0', text='ID')
tv.heading('name', text='NAME')
tv.heading('date', text='DATE')
tv.heading('time', text='TIME')

scroll = ttk.Scrollbar(frame1, orient='vertical', command=tv.yview)
scroll.grid(row=2, column=4, padx=(0, 100), pady=(150, 0), sticky='ns')
tv.configure(yscrollcommand=scroll.set)

# Button styling function
def create_button(parent, text, command, x, y, width=35, height=1, bg=BUTTON_COLOR):
    button = tk.Button(parent, text=text, command=command,
                      fg=TEXT_COLOR, bg=bg, width=width, height=height,
                      activebackground=BUTTON_HOVER, activeforeground=TEXT_COLOR,
                      font=('Helvetica', 15, 'bold'), relief='flat',
                      cursor='hand2')
    button.place(x=x, y=y)
    return button

# Create buttons with new styling
clearButton = create_button(frame2, "Clear", clear, 335, 86, width=11)
clearButton2 = create_button(frame2, "Clear", clear2, 335, 172, width=11)
takeImg = create_button(frame2, "Take Images", TakeImages, 30, 300)
trainImg = create_button(frame2, "Save Profile", psw, 30, 380)
trackImg = create_button(frame1, "Take Attendance", TrackImages, 30, 50, bg=ACCENT_COLOR)
quitWindow = create_button(frame1, "Quit", window.destroy, 30, 450, bg=ERROR_COLOR)
clearDataButton = create_button(frame1, "Clear All Data", clear_all_data, 30, 500, bg=ERROR_COLOR)

##################### MENUBAR #################################

menubar = tk.Menu(window, relief='flat', bg=FRAME_COLOR, fg=TEXT_COLOR)
filemenu = tk.Menu(menubar, tearoff=0, bg=FRAME_COLOR, fg=TEXT_COLOR)
filemenu.add_command(label='Change Password', command=change_pass)
filemenu.add_command(label='Contact Us', command=contact)
filemenu.add_command(label='Exit', command=window.destroy)
menubar.add_cascade(label='Help', font=('Helvetica', 12, 'bold'), menu=filemenu)

window.configure(menu=menubar)
window.mainloop()

####################################################################################################

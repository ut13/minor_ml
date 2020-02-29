import cv2
import serial
import time

# load the required trained XML classifiers
# https://github.com/Itseez/opencv/blob/master/
# data/haarcascades/haarcascade_frontalface_default.xml
# Trained XML classifiers describes some features of some
# object we want to detect a cascade function is trained
# from a lot of positive(faces) and negative(non-faces)
# images.
ser = serial.Serial('COM3', 9600)

face_cascade = cv2.CascadeClassifier('C:\\Users\\utkar\\Downloads\\haarcascade_frontalface_default.xml')

# capture frames from a camera
cap = cv2.VideoCapture(0)

# loop runs if capturing has been initialized.

def led_on_off(user_input):
    # user_input = input("\n Type on / off / quit : ")
    if user_input ==1:
        print("LED is on...")
        time.sleep(0.1)
        ser.write(b'H')
    elif user_input ==0:
        print("LED is off...")
        time.sleep(0.1)
        ser.write(b'L')
    elif user_input =="quit" or user_input == "q":
        print("Program Exiting")
        time.sleep(0.1)
        ser.write(b'L')
        ser.close()
    else:
        print("Invalid input. Type on / off / quit.")

time.sleep(2) # wait for the serial connection to initialize
while 1:

    # reads frames from a camera
    ret, img = cap.read()

    # convert to gray scale of each frames
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detects faces of different sizes in the input image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    print(type(faces))

    if len(faces) == 0:
        print("No faces found")
        led_on_off(0)
    else:
        led_on_off(1)
        print(faces)
        print(faces.shape)
        print("Number of faces detected: " + str(faces.shape[0]))
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.rectangle(img, ((0, img.shape[0] - 25)), (270, img.shape[0]), (255, 255, 255), -1)
        cv2.putText(img, "Number of faces detected: " + str(faces.shape[0]), (0, img.shape[0] - 10),
                    cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0), 1)

    # Display an image in a window
    cv2.imshow('img', img)

    # Wait for Esc key to stop
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Close the window
cap.release()

# De-allocate any associated memory usage
cv2.destroyAllWindows()
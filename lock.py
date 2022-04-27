import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
from datetime import date
import speech_recognition as sr
import winsound
import pyttsx3
import datetime
import smtplib
import math
import random

k = pyttsx3.init()
sound = k.getProperty('voices')
k.setProperty('voice', sound[0].id)
k.setProperty('rate', 130)
k.setProperty('pitch', 200)
count = 0


def speak(text):
    k.say(text)
    k.runAndWait()

data_path = "C:/Users/gupta/PycharmProjects/Project/FaceDettector/"
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]

Training_Data, Labels = [], []

for i, files in enumerate(onlyfiles):
    image_path = data_path + onlyfiles[i]
    images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    Training_Data.append(np.asarray(images, dtype=np.uint8))
    Labels.append(i)

Labels = np.asarray(Labels, dtype=np.int32)
model = cv2.face.LBPHFaceRecognizer_create()

model.train(np.asarray(Training_Data), np.asarray(Labels))
print("Congratulations model is TRAINED ... *_*...")

face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def face_detector(img, size=0.5):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    i = 0
    if faces is ():
        return img, []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        roi = img[y:y + h, x:x + w]
        roi = cv2.resize(roi, (200, 200))
        i = i + 1

        if (i > 1):
            print("alert")
            cap.release()
            cv2.destroyAllWindows()
            msg = "more than one people trying to access"
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("sanskriti.gupta2020@vitbhopal.ac.in", "vzoe kcxq jfbh ailg")
            s.sendmail('&&&&&&&&&&&', "gupta.sanskriti08@gmail.com", msg)

    return img, roi


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    image, face = face_detector(frame)

    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        result = model.predict(face)

        if result[1] < 500:
            Confidence = int(100 * (1 - (result[1]) / 300))

        if 75 < Confidence:
            Date = date.today()
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak("Face is found at  " + time)
            cv2.putText(image, "HELLO USER", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("Face Cropper", image)
            count = 1

            listener = sr.Recognizer()
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            cap.release()
            cv2.destroyAllWindows()
        else:
            pass

        if count == 1:
            def talk(text):
                engine.say(text)
                engine.runAndWait()


            def take_command():
                try:
                    with sr.Microphone() as source:
                        talk("Hello Sanskriti Say lock ")
                        print("listening...")
                        voice = listener.listen(source)
                        command = listener.recognize_google(voice)
                        command = command.lower()
                        if 'dodo' in command:
                            command = command.replace('dodo', '')
                            talk(command)
                except:
                    pass
                return command


            command = take_command()

            if 'lock' in command:
                digits = "0123456789"
                OTP = ""
                List = []
                for i in range(0, 4):
                    OTP += digits[math.floor(random.random() * 10)]
                for i in OTP:
                    List.append(i)
                talk(List)
                otp = OTP + " is your OTP"
                msg = otp
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login("sanskriti.gupta2020@vitbhopal.ac.in", "vzoe kcxq jfbh ailg")
                # emailid = input("Enter your email: ")
                s.sendmail('&&&&&&&&&&&', 'gupta.sanskriti08@gmail.com', msg)
                a = input("Enter Your OTP >>: ")
                if a == OTP:
                    print("Verified")
                else:
                    print("Please Check your OTP again")

            else:
                talk("Please say the command again")


        else:
            winsound.Beep(1000, 200)
            cv2.putText(image, "CAN'T RECOGNISE", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("Face Cropper", image)
            print(Confidence)
            print("Unauthorise user")
            cap.release()
            cv2.destroyAllWindows()
            msg = "unauthorise people"
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("sanskriti.gupta2020@vitbhopal.ac.in", "vzoe kcxq jfbh ailg")
            s.sendmail('&&&&&&&&&&&', "gupta.sanskriti08@gmail.com", msg)

    except:
        # speak("face not found")
        winsound.Beep(1000, 200)
        cv2.putText(image, "Face not FoUnD", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("Face Cropper", image)
        pass
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




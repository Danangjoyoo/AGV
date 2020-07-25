import cv2
import numpy as np
import time
import math
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(1)
tpk_cscd = cv2.CascadeClassifier('palm.xml')
kepal_cscd = cv2.CascadeClassifier('kepal.xml')
tim0 = time.time()
while (cap.isOpened()):
    time1 = time.time()
    ret, frame = cap.read()
    frame = cv2.resize(frame,None,fx=0.5,fy=0.5, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray,3)
    canny = cv2.Canny(blur,100,200,apertureSize=3)
    cv2.imshow('looo',canny)
    tpk = tpk_cscd.detectMultiScale(canny,1.05,3)
    kepal = kepal_cscd.detectMultiScale(gray,1.15,9)
    for (x,y,w,h) in tpk:
        w1 = str(w)
        dist = (0.00138 * (w ** 2)) - (0.7977 * w) + 139.71
        dist1 = round(dist, 2)  # rounded to have 2 decimals
        dist = str(dist1) + (" cm")  # convert to str and add 'cm' string
        cv2.rectangle(frame,(x,y),(x+w, y+h),(0,0,255),2)
        cv2.putText(frame, dist, (x + 1,), cv2.FONT_HERSHEY_COMPLEX, 1, (12, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, "Telapak", (x + 10, y + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (12, 0, 250), 1, cv2.LINE_AA)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            print(w1)
        #if x > 0:
         #   print("TELAPAK")
    for (x,y,w,h) in kepal:
        #true_dist = int(input("input true distance: "))
        w1 = str(w)
        dist = (0.00138*(w**2))-(0.7977*w)+139.71
        dist1 = round(dist, 2)   #rounded to have 2 decimals
        dist = str(dist1)+(" cm") #convert to str and add 'cm' string
        cv2.rectangle(frame,(x,y),(x+w, y+h),(30,255,0),5)
        cv2.putText(frame,"Kepal",(x+10, y+30), cv2.FONT_HERSHEY_COMPLEX, 1, (30, 255, 0), 1, cv2.LINE_AA)
        #cv2.putText(frame,dist,(x+1,y-5),cv2.FONT_HERSHEY_COMPLEX,1,(30, 255, 0),1,cv2.LINE_AA)
        """error_val1 = (true_dist - dist1) ** 2  # square it to make the value positive
        error_val2 = math.sqrt(error_val1)  # then squareroot it
        error_val3 = (error_val2 / true_dist) * 100
        error_val3 = round(error_val3, 2)
        error_val3 = str(error_val3)
        print(error_val3," %")"""
        if cv2.waitKey(1) & 0xFF == ord('c'):
           """ error_val1 = (true_dist-dist)**2 #square it to make the value positive
            error_val2 = math.sqrt(error_val1) #then squareroot it
            error_val3 = (error_val2/true_dist)*100
            error_val3 = str(error_val3)
            print(error_val3)"""
        #if x > 0:
         #   print("KEPAL")
    print(frame.shape[0])
    print(frame.shape[1])
    frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)
    time2 = time.time()
    fps = 1/(time2-time1)
    fps = round(fps,2)
    cv2.putText(frame,"FPS: %a"%fps,(50,50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,10,10),1)
    cv2.imshow('lol', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
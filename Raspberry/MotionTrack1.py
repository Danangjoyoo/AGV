import cv2
import numpy as np
import time

cap = cv2.VideoCapture(1)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while (cap.isOpened()):
    #ret, frame = cap.read()
    diff = cv2.absdiff(frame1,frame2)
    gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    cv2.imshow('blur',blur)
    _, thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh,None,iterations=3)
    contours,_ = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    #cv2.drawContours(frame1, contours, -1, (10,10,250),2)
    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        print(cv2.contourArea(contour))
        if cv2.contourArea(contour) < 700:
            continue
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(10,250,10),2)
    cv2.imshow('frame1',frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

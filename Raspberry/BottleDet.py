import cv2
import matplotlib.pyplot as plt

def size(img,ratio):
    img = cv2.resize(img,None,fx=ratio,fy=ratio,interpolation=cv2.INTER_AREA)
    return img

def detect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.medianBlur(gray,3)
    cv2.imshow('blur',blur)
    #g_cscd = cv2.CascadeClassifier('green1.xml')
    r_cscd = cv2.CascadeClassifier('human1.xml')
    #green = g_cscd.detectMultiScale(blur,1.05,2)
    red = r_cscd.detectMultiScale(blur,1.015,5)
    try:
        #for x,y,w,h in green:
            #cv2.rectangle(img,(x,y),(x+w,y+h),(20,250,10),2)
        for x,y,w,h in red:
            dist = ((-0.00000003*(w^6))+(0.00002*(w^5))-(0.0064*(w^4))+(0.9341*(w^3))-(76.688*(w^2))+(3346.9*w)-60640)
            dist = (-0.2713*w)+55.333
            dist = round(dist+10,2)
            vert = y+h
            horz = x+w
            #print(w)
            cv2.putText(img,("%a cm" % dist),(horz-70,vert),cv2.FONT_HERSHEY_COMPLEX,0.5,(250,50,50),1)
            cv2.rectangle(img,(x,y),(horz-20,vert-20),(20,20,250),2)
            #cv2.line(img,(x+10,y-15),(x+150,y-15),(20,20,250),30,cv2.LINE_4)
            text = cv2.putText(img,"Human",(x+10,y+30),cv2.FONT_HERSHEY_COMPLEX,0.7,(250,250,250),1)
    except:
        pass
    return img

cap = cv2.VideoCapture(1)

while (cap.isOpened()):
    _, frame = cap.read()
    frame = size(frame,0.5)
    #print(frame.shape[0])
    #print(frame.shape[1])
    frame= detect(frame)
    frame = size(frame,2)
    cv2.imshow('lal',frame)
    #cv2.imshow('awa',origin)
    #plt.imshow(frame)
    #plt.show()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
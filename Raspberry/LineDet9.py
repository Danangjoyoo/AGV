import time
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

def BEV(img):
    max_x = img.shape[1]
    max_y = img.shape[0]
    p1 = np.float32([[0, max_y*0.9], [max_x, max_y*0.9], [max_x*0.8, max_y*0.7], [max_x*0.2, max_y*0.7]])
    p2 = np.float32([[0, max_y], [max_x, max_y], [max_x, 0], [0, 0]])
    bev1 = cv2.getPerspectiveTransform(p1, p2)
    bev2 = cv2.warpPerspective(img, bev1, (max_x, max_y))
    return bev2

def roi(img,titik_sudut):
    mask = np.zeros_like(img)
    mask_color = (255)
    cv2.fillPoly(mask,np.array([titik_sudut],np.int32),mask_color)
    masked = cv2.bitwise_and(img,mask)
    return masked

def extract_B(lines):
    fit = []
    slope = []
    intercept =[]
    try:
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4)
            parameters = np.polyfit((x1,x2),(y1,y2),1)
            m = parameters[0]
            b = parameters[1]
            fit.append((m,b))
            slope.append(m)
            intercept.append(b)
    except:
        pass
    itc = np.average(intercept,axis=0)
    #print(avgfit)
    return itc

def process(img,degree):
    max_x = img.shape[1]
    max_y = img.shape[0]
    cv2.imshow('img',img)
    img = BEV(img)
    titik_sudut2 = [(0, max_y),
                    (max_x, max_y),
                    ((max_x)/2, (max_y)/2)]
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    canny = cv2.Canny(gray,30,100,apertureSize=3)
    blur = cv2.GaussianBlur(canny,(3,3),0)
    crop = roi(blur,titik_sudut2)
    cv2.imshow('crop',crop)
    lines = cv2.HoughLinesP(crop,1,np.pi/180,50,np.array([]),25,15)
    img,xl1,xl2,xr1,xr2 = drawline(img, lines)
    derajat_belok = degturn(img,xr1,xr2,xl1,xl2,degree)
    #b_value = extract_B(lines)
    return img, derajat_belok

def avgM(img,lines):
    copy = np.zeros_like(img)
    halfRegion = int((copy.shape[1])/2)
    fitL = []
    fitR = []
    try:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            if x1 <= halfRegion and x2 <= halfRegion:
                parametersL = np.polyfit((x1, x2), (y1, y2), 1)
                ml = parametersL[0]
                bl = parametersL[1]
                fitL.append((ml, bl))
            elif x1 > halfRegion and x2 > halfRegion:
                parametersR = np.polyfit((x1, x2), (y1, y2), 1)
                mr = parametersR[0]
                br = parametersR[1]
                fitR.append((mr, br))
    except:
        pass
    avgfitL = np.average(fitL, axis=0)
    avgfitR = np.average(fitR, axis=0)
    return avgfitL, avgfitR
"""def avgML(img,lines):
    copy = np.copy(img)
    halfRegion = int((copy.shape[1])/2)
    fitL = []
    try:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            if x1 <= halfRegion and x2 <= halfRegion:
                parameters1 = np.polyfit((x1, x2), (y1, y2), 1)
                ml = parameters1[0]
                bl = parameters1[1]
                fitL.append((ml, bl))
    except:
        pass
    avgfitL = np.average(fitL, axis=0)
    return avgfitL
def avgMR(img,lines):
    copy = np.copy(img)
    halfRegion = int((copy.shape[1])/2)
    fitR = []
    try:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            if x1 > halfRegion and x2 > halfRegion:
                parameters1 = np.polyfit((x1, x2), (y1, y2), 1)
                mr = parameters1[0]
                br = parameters1[1]
                fitR.append((mr, br))
    except:
        pass
    avgfitR = np.average(fitR, axis=0)
    return avgfitR"""

def drawline(img, lines):
    dxL1 = []
    dxL2 = []
    dxR1 = []
    dxR2 = []
    try:
        (mlx, blx),(mrx, brx) = avgM(img, lines)
        copy = np.zeros_like(img)
        y1 = int((copy.shape[0]) * 6 / 8)
        y2 = int((copy.shape[0]) * 7 / 8)
        xl1 = int((y1 - blx) / mlx)
        xl2 = int((y2 - blx) / mlx)
        xr1 = int((y1 - brx) / mrx)
        xr2 = int((y2 - brx) / mrx)
        x1_l = xl1
        x2_l = xl2
        x1_r = xr1
        x2_r = xr2
        dxL1.append(x1_l)
        dxL2.append(x2_l)
        dxR1.append(x1_r)
        dxR2.append(x2_r)
        cv2.line(img, (xl1, y1), (xl2, y2),
                 (250, 0, 250), 4)
        cv2.line(img,(xr1,y1),(xr2,y2),
                 (250, 0, 250), 4)
    except:
        pass
    dxL1 = np.average(dxL1, axis=0)
    dxL2 = np.average(dxL2, axis=0)
    dxR1 = np.average(dxR1, axis=0)
    dxR2 = np.average(dxR2, axis=0)
    return img, dxL1, dxL2, dxR1, dxR2

"""def drawlineL(img, lines):
    dx1 = []
    dx2 = []
    try:
        mlx, blx = avgML(img, lines)
        img = np.copy(img)
        yl1 = int((img.shape[0]) * 6 / 8)
        yl2 = int((img.shape[0]) * 7 / 8)
        xl1 = int((yl1 - blx) / mlx)
        xl2 = int((yl2 - blx) / mlx)
        x1 = xl1
        x2 = xl2
        dx1.append(x1)
        dx2.append(x2)
        cv2.line(img, (xl1, yl1), (xl2, yl2),
                 (250, 0, 250), 4)
    except:
        pass
    dx1 = np.average(dx1, axis=0)
    dx2 = np.average(dx2, axis=0)
    return img, dx1, dx2
def drawlineR(img, lines):
    dx1 = []
    dx2 = []
    try:
        mrx, brx = avgMR(img, lines)
        img = np.copy(img)
        yr1 = int((img.shape[0]) * 6 / 8)
        yr2 = int((img.shape[0]) * 7 / 8)
        xr1 = int((yr1 - brx) / mrx)
        xr2 = int((yr2 - brx) / mrx)
        x1 = xr1
        x2 = xr2
        dx1.append(x1)
        dx2.append(x2)
        cv2.line(img, (xr1, yr1), (xr2, yr2),
                 (250, 0, 250), 4)
    except:
        pass
    dx1 = np.average(dx1, axis=0)
    dx2 = np.average(dx2, axis=0)
    return img, dx1, dx2"""

def degturn(img,xr1,xr2,xl1,xl2, degree):
    ax1 = (xr1 + xl1) / 2
    ax2 = (xr2 + xl2) / 2
    deltaX = (ax1 - ax2)
    ay1 = int((img.shape[0]) * 6 / 8)
    ay2 = int((img.shape[0]) * 7 / 8)
    deltaY = (ay2 - ay1)
    depersam = deltaX/deltaY
    rad1 = math.atan(depersam)
    deg1 = math.degrees(rad1)
    nanrad = math.isnan(rad1)
    nanxr = math.isnan(xr1)
    nanxl = math.isnan(xl1)
    try:
        cv2.line(img,
                 (int(ax1), ay1),
                 (int(ax2), ay2),
                 (195, 90, 10), 2)
    except:
        pass
    if nanrad == True:
        if nanxl == False and nanxr == True:
            depersam = (xl1-xl2) / deltaY
            rad1 = math.atan(depersam)
            deg1 = math.degrees(rad1)
            deg1 = int(0.5 * deg1)
            cv2.line(img,
                     (int(xl1), ay1),
                     (int(xl2), ay2),
                     (195, 90, 10), 2)
        elif nanxl == True and nanxr == False:
            depersam = (xr1 - xr2) / deltaY
            rad1 = math.atan(depersam)
            deg1 = math.degrees(rad1)
            deg1 = int(-0.5 * deg1)
            cv2.line(img,
                     (int(xr1), ay1),
                     (int(xr2), ay2),
                     (195, 90, 10), 2)
        else:
            deg1 = degree
    return deg1

def ObjDet(img):
    car_cscd = cv2.CascadeClassifier('cars.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.medianBlur(gray,7)
    cars = car_cscd.detectMultiScale(blur,1.8,5)
    for (x,y,w,h) in cars:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,10,10),3)
        cv2.putText(img, "Car", (x, y-10),cv2.FONT_HERSHEY_COMPLEX,1,(150,150,150),2)
    return img

def mapping(value,min1,max1,min2,max2):
    range1 = max1-min1
    range2 = max2-min2
    mapped = float(max2-((max1-value)*range2/range1))
    mapped = round(mapped,2)
    return mapped

def FPS(img, time1, time2):
    runtime = time2 - starttime
    runtime = round(runtime, 2)
    # print("runtime ",runtime)
    dt = time2 - time1
    try:
        fps = 1 / dt
    except:
        fps = 10
        pass
    fps = round(fps, 2)
    # plt.imshow(frame)
    # plt.show()
    cv2.putText(frame, ("FPS = %a" % fps), (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (55, 60, 270), 2)
    #cv2.putText(frame, ("Runtime = %a sec" % runtime), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (55, 60, 270), 2)
    return img,fps

def track_matching(img,radian,B,bx,by):
    costeta = math.cos(radian)
    sinteta = math.sin(radian)
    bx = int(-((B/50)*costeta)+bx)
    by = int(((B/50)*sinteta)+by)
    img = cv2.circle(img,(bx,by),1,(250,250,50),2)
    return img,bx,by

def drawtrack(degree, track0, bval1, bx, by):
    rad = math.radians(degree)
    track2 = track0
    try:
        track1, bx, by = track_matching(track0, rad, bval1, bx, by)
        track2 = cv2.addWeighted(track0, 0.8, track1, 1, 0.0)
        windowtracking = size(track2,0.5)
        cv2.imshow('BEV', windowtracking)
        #print('success tracking')
    except:
        #print('fail tracking')
        pass
    return track2, bx, by

def size(img,scale):
    img = cv2.resize(img,None,fx=scale,fy=scale,interpolation=cv2.INTER_AREA)
    return img


cap = cv2.VideoCapture('rec4.mp4')
starttime = time.time()
idxs = 0
track = np.zeros((1800, 3604, 3), dtype=np.uint8)
bx = 3000
by = 800
degtrack = 0
sum_fps = []
degree = 0
sum1 = []
while (cap.isOpened()):
    control_time1 = time.time()
    time1 = time.time()
    time11 = time.time()
    _, frame = cap.read()
    frame = size(frame,0.5)
    frame, degree = process(frame, degree)
    degree = round(degree,2)
    #print("degree: ",degree)
    #frame = ObjDet(frame)
    frame = size(frame,2)
    #track,bx,by = drawtrack(degree,track,bval1,bx,by)
    #===================================================
    time2 = time.time()
    frame,fps = FPS(frame,time1,time2)
    sum_fps.append([fps])
    avg_fps = np.average(sum_fps,axis=0)
    avg_fps = np.array(avg_fps,dtype=np.float32)
    avg_fps = float(avg_fps[0])
    avg_fps = round(avg_fps,2)
    print("Avg FPS: ",avg_fps)
    #==================================================
    cv2.imshow('PROCESSED',frame)
    idxs += 1
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
    control_time2 = time.time()
    fps_control = round((1/30),3)
    control_t = round(control_time2-control_time1,3)
    print(control_t,fps_control)
    if control_t > fps_control:
        time.sleep((control_t-fps_control)/2)
        print(control_t-fps_control)
    time3 = time.time()
    true_fps = 1/(time3-time1)
    true_fps = round(true_fps,2)
    print("True FPS: {}".format(true_fps))
    #if idxs == 500:
    #    break

cap.release()
cv2.destroyAllWindows()
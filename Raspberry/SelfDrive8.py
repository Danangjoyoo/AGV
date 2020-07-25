import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
import RPi.GPIO as pi
import time


# ========= COMPUTER VISION ALGORITHM ==========

# REGION OF INTEREST
def roi(img, titik_sudut):
    mask = np.zeros_like(img)
    mask_color = (255)
    cv2.fillPoly(mask,
                 np.array([titik_sudut], np.int32),
                 mask_color)
    masked = cv2.bitwise_and(img, mask)
    return masked


def extract_B(lines):
    fit = []
    slope = []
    intercept = []
    try:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2),
                                    (y1, y2), 1)
            m = parameters[0]
            b = parameters[1]
            fit.append((m, b))
            slope.append(m)
            intercept.append(b)
    except:
        pass
    itc = np.average(intercept, axis=0)
    # print(avgfit)
    return itc


def process(img, degree0):
    copy = np.zeros_like(img)
    max_y = copy.shape[0]
    max_x = copy.shape[1]
    titik_sudut2 = [(0, (max_y * 1)),(max_x, (max_y * 1)),
                    (max_x, (max_y * 0.4)), (0, (max_y * 0.4))]
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    grayy = size(gray, 2)
    cv2.imshow('gray',grayy)    
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 250, 450, apertureSize=3)
    cann = size(canny, 2)
    cv2.imshow('can',cann)
    blurr = size(blur, 2)
    cv2.imshow('blurr',blurr)
    crop = roi(canny, titik_sudut2)
    cropp = size(crop, 2)
    cv2.imshow('crop', cropp)
    lines = cv2.HoughLinesP(crop, 1,
                            np.pi / 180, 20,
                            np.array([]), 30, 15)
    img, xl1, xl2 = drawlineL(img, lines)
    img, xr1, xr2 = drawlineR(img, lines)
    derajat_belok = degree0
    try:
        derajat_belok = degturn(img,
                                xr1, xr2,
                                xl1, xl2, degree0)
    except:
        pass
    # checkDeg(img, derajat_belok)
    b_value = extract_B(lines)
    return img, derajat_belok, b_value

delayy = 2

def degturn(img, xr1, xr2, xl1, xl2, degree):
    ax1 = (xr1 + xl1) / 2
    ax2 = (xr2 + xl2) / 2
    deltaX = (ax1 - ax2)
    ay1 = int((img.shape[0]) * 0.6)
    ay2 = int((img.shape[0]) * 1)
    deltaY = (ay2 - ay1)
    depersam = deltaX/deltaY
    rad1 = math.atan(depersam)
    deg1 = math.degrees(rad1)
    deg1 = deg1/2
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
            deg1 = int(0.4 * deg1)
            cv2.line(img,
                     (int(xl1), ay1),
                     (int(xl2), ay2),
                     (195, 90, 10), 2)
        elif nanxl == True and nanxr == False:
            depersam = (xr1 - xr2) / deltaY
            rad1 = math.atan(depersam)
            deg1 = math.degrees(rad1)
            deg1 = int(0.4 * deg1)
            cv2.line(img,
                     (int(xr1), ay1),
                     (int(xr2), ay2),
                     (195, 90, 10), 2)
        else:
            deg1 = 0
    return deg1

def avgMR(img, lines):
    copy = np.copy(img)
    halfRegion = int((copy.shape[1]) / 2)
    fitR = []
    try:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            if x1 > halfRegion and x2 > halfRegion:
                parameters1 = np.polyfit((x1, x2),
                                         (y1, y2), 1)
                mr = parameters1[0]
                br = parameters1[1]
                fitR.append((mr, br))
    except:
        pass
    avgfitR = np.average(fitR, axis=0)
    return avgfitR


def avgML(img, lines):
    copy = np.copy(img)
    halfRegion = int((copy.shape[1]) / 2)
    fitL = []
    try:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            if x1 <= halfRegion and x2 < halfRegion:
                parameters1 = np.polyfit((x1, x2),
                                         (y1, y2), 1)
                ml = parameters1[0]
                bl = parameters1[1]
                fitL.append((ml, bl))
    except:
        pass
    avgfitL = np.average(fitL, axis=0)
    return avgfitL

def drawlineL(img, lines):
    dx1 = []
    dx2 = []
    try:
        mlx, blx = avgML(img, lines)
        img = np.copy(img)
        blank = np.zeros((img.shape[0], img.shape[1],
                          3), dtype=np.uint8)
        yl1 = int((img.shape[0]) * 0.6)
        yl2 = int((img.shape[0]) * 1)
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
        print(mrx)
        img = np.copy(img)
        blank = np.zeros((img.shape[0], img.shape[1],
                          3), dtype=np.uint8)
        yr1 = int((img.shape[0]) * 0.6)
        yr2 = int((img.shape[0]) * 1)
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
    return img, dx1, dx2

def checkDeg(img, deg):
    try:
        x1 = 300
        y1 = 100
        x2 = int((x1 * (math.cos(deg))) -
                 (y1 * (math.sin(deg))))
        y2 = int((x1 * (math.sin(deg))) +
                 (y1 * (math.cos(deg))))
        try:
            cv2.line(img, (x2, y2), (x1, y1),
                     (30, 50, 75), 3)
        except:
            pass
    except:
        pass

# ========== MACHINE LEARNING ALGORITHM ========

# DETEKSI OBJEK
def ObjDet(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.medianBlur(gray, 7)
    kepal_cscd = cv2.CascadeClassifier('kepal.xml')
    lampu_cscd = cv2.CascadeClassifier('red7.xml')
    human_cscd = cv2.CascadeClassifier('human1.xml')
    kepal = kepal_cscd.detectMultiScale(blur, 1.15, 9)
    lampu = lampu_cscd.detectMultiScale(blur, 1.4, 44)
    # -----deteksi kepalan tangan------------
    jarak_kepal = []
    kepal_cscd = cv2.CascadeClassifier('kepal.xml')
    kepal = kepal_cscd.detectMultiScale(blur, 1.15, 9)
    lampu = lampu_cscd.detectMultiScale(blur, 1.4, 44)
    human = human_cscd.detectMultiScale(blur, 1.041, 6)
    for (x, y, w, h) in kepal:
        cv2.rectangle(img, (x, y), (x + w, y + h),
                      (20, 255, 10), 3)
        cv2.putText(img, "Car", (x, y - 10),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1, (150, 150, 150), 2)
        jarak_kepal.append(w)
    jarak_kepal = np.average(jarak_kepal, axis=0)
    # --------deteksi lampu merah--------
    jarak_lampu = []
    #lampu_cscd = cv2.CascadeClassifier('red7.xml')
    #lampu = lampu_cscd.detectMultiScale(blur, 1.4, 44)
    for (x, y, w, h) in lampu:
        cv2.rectangle(img, (x, y), (x + w, y + h),
                      (255, 30, 30), 3)
        cv2.putText(img, "Car", (x, y - 10),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1, (150, 150, 150), 2)
        jarak_lampu.append(w)
    jarak_lampu = np.average(jarak_lampu, axis=0)
    # ------deteksi telapak tangan--------
    jarak_telapak = []
    #human_cscd = cv2.CascadeClassifier('human1.xml')
    #human = human_cscd.detectMultiScale(blur, 1.041, 6)
    for (x, y, w, h) in human:
        cv2.rectangle(img, (x, y), (x + w, y + h),
                      (10, 10, 250), 3)
        cv2.putText(img, "Car", (x, y - 10),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1, (150, 150, 150), 2)
        jarak_telapak.append(w)
    jarak_telapak = np.average(jarak_telapak, axis=0)
    return img, jarak_kepal, jarak_lampu,jarak_telapak

# ======== CONTROL SYSTEM ALGORITHM USES =====

# KONVERSI SKALA
def mapping(value, min1, max1, min2, max2):
    range1 = max1 - min1
    range2 = max2 - min2
    mapped = float(max2 - ((max1 - value) *
                           range2 / range1))
    mapped = round(mapped, 2)
    return mapped

# MENGHITUNG NILAI FPS SELAMA PROCESSING
def FPS(img, time1, time2):
    runtime = time2 - starttime
    runtime = round(runtime, 2)
    dt = time2 - time1
    fps = 1 / dt
    fps = round(fps, 2)
    cv2.putText(frame, ("FPS = %a" % fps),
                (50, 50), cv2.FONT_HERSHEY_PLAIN,
                2, (55, 60, 270), 2)
    cv2.putText(frame, ("Runtime = %a sec" % runtime),
                (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                1, (55, 60, 270), 2)
    return img

# TRAJEKTORI KENDARAAN
def BEV(img, degree, B, bx, by):
    costeta = math.cos(degree)
    sinteta = math.sin(degree)
    bx = int(-((B / 10) * sinteta) + bx)
    # print("bx ",bx)
    by = int(((B / 10) * costeta) + by)
    # print("by ", by)
    img = cv2.circle(img, (bx, by), 1,
                     (250, 250, 50), 2)
    return img, bx, by

def drawBEV(deg, Bev2, bval1, bx, by):
    rad = math.radians(deg)
    try:
        bev1, bx, by = BEV(Bev2, rad, bval1, bx, by)
        Bev2 = cv2.addWeighted(Bev2, 0.8,
                               bev1, 1, 0.0)
        cv2.imshow('BEV', Bev2)
    except:
        pass

# MENGUBAH RESOLUSI LAYAR
def size(img, scale):
    img = cv2.resize(img, None, fx=scale, fy=scale,
                     interpolation=cv2.INTER_AREA)
    return img


# <<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>
# ====================CORE PROGRAM================

# ==========DEKLARASI COMPUTER VISION=========
cap = cv2.VideoCapture(0)
starttime = time.time()
idxs = 0
Bev2 = np.zeros((800, 1804, 3), dtype=np.uint8)
bx = 1500
by = 200
#time.sleep(2)
# ======DEKLARASI SISTEM KONTROL==============
pi.setmode(pi.BOARD)
bit1 = 40
bit2 = 38
bit3 = 36
bit4 = 32
bit5 = 37
bit6 = 26
bit7 = 24
arah = 22
power = 18
pi.setup(bit1, pi.OUT)
pi.setup(bit2, pi.OUT)
pi.setup(bit3, pi.OUT)
pi.setup(bit4, pi.OUT)
pi.setup(bit5, pi.OUT)
pi.setup(bit6, pi.OUT)
pi.setup(bit7, pi.OUT)
pi.setup(arah, pi.OUT)
pi.setup(power, pi.OUT)
brake1, brake2, brake3 = 0, 0, 0
dist1, dist2, dist3 = 1, 1, 1
deg = 0
abs_brake = 0
# =========DELAY DECLARATION=====
deg_container = []
iter1 = 1
degree = 0
delay_frame = delayy
# ==========ITERASI PROGRAM======
while (cap.isOpened()):
    time1 = time.time()
    _, frame = cap.read()
    frame = size(frame, 0.5)
    frame, degree_ext, bval1 = process(frame, deg)
    # DELAYING THE TURNING ACTION
    deg_container.append(degree_ext)
    if iter1 < delay_frame:
        degree = 0
    elif iter1 >= delay_frame:
        degree = deg_container[(iter1 - delay_frame)]
    #-----continue program----
    degree = round(degree, 2)
    deg = int(degree)
    print("degree: ", deg)
    # =====Machine Learning Activation==========
    if iter1 < delay_frame:
        dist1,dist2,dist3 = 1,1,1
    elif iter1 >= delay_frame:
        dist1,dist2,dist3 = 0,0,0
        #frame,dist1,dist2,dist3 = ObjDet(frame)
    if dist1 <= 20 and dist1 != 0:
        brake1 = 1
    elif dist1 > 20 or dist1 == 0:
        brake1 = 0

    if dist2 <= 20 and dist2 != 0:
        brake2 = 1
    elif dist2 > 20 or dist2 == 0:
        brake2 = 0

    if dist3 <= 20 and dist3 != 0:
        brake3 = 1
    elif dist3 > 20 or dist3 == 0:
        brake3 = 0
    # ========Bird's Eye View===============
    drawBEV(deg,Bev2,bval1,bx,by)
    idxs += 1
    print("iteration: ", iter1)
    iter1 += 1
    # ===============CONTROL SYSTEM===============
    # =============dynamo power================
    #print("DISTANCE: ", dist1, dist2, dist3)
    if brake1 == 0 and brake2 == 0 and brake3 == 0 and abs_brake == 0:
        pi.output(power, True)
        print(brake1, brake2, brake3, "GAS!")
    elif brake1 == 1 or brake2 == 1 or brake3 == 1 or abs_brake == 1:
        pi.output(power, False)
        print(brake1, brake2, brake3, "STOP!")

    # ==========degree convertion==============
    a = deg
    print("a: ", a)
    if a >= 0:
        pi.output(arah, True)
        a = a
    elif a < 0:
        pi.output(arah, False)
        a = a * -1

    b = format(a, 'b')
    print(b)
    c = str(b)
    d = len(c)

    if d == 1:
        bin1 = b[0]
        bin2 = '0'
        bin3 = '0'
        bin4 = '0'
        bin5 = '0'
        bin6 = '0'
        bin7 = '0'
    elif d == 2:
        bin1 = b[1]
        bin2 = b[0]
        bin3 = '0'
        bin4 = '0'
        bin5 = '0'
        bin6 = '0'
        bin7 = '0'
    elif d == 3:
        bin1 = b[2]
        bin2 = b[1]
        bin3 = b[0]
        bin4 = '0'
        bin5 = '0'
        bin6 = '0'
        bin7 = '0'
    elif d == 4:
        bin1 = b[3]
        bin2 = b[2]
        bin3 = b[1]
        bin4 = b[0]
        bin5 = '0'
        bin6 = '0'
        bin7 = '0'
    elif d == 5:
        bin1 = b[4]
        bin2 = b[3]
        bin3 = b[2]
        bin4 = b[1]
        bin5 = b[0]
        bin6 = '0'
        bin7 = '0'
    elif d == 6:
        bin1 = b[5]
        bin2 = b[4]
        bin3 = b[3]
        bin4 = b[2]
        bin5 = b[1]
        bin6 = b[0]
        bin7 = '0'
    elif d == 7:
        bin1 = b[6]
        bin2 = b[5]
        bin3 = b[4]
        bin4 = b[3]
        bin5 = b[2]
        bin6 = b[1]
        bin7 = b[0]

    if bin1 == '1':
        pi.output(bit1, True)
    elif bin1 == '0':
        pi.output(bit1, False)

    if bin2 == '1':
        pi.output(bit2, True)
    elif bin2 == '0':
        pi.output(bit2, False)

    if bin3 == '1':
        pi.output(bit3, True)
    elif bin3 == '0':
        pi.output(bit3, False)

    if bin4 == '1':
        pi.output(bit4, True)
    elif bin4 == '0':
        pi.output(bit4, False)

    if bin5 == '1':
        pi.output(bit5, True)
    elif bin5 == '0':
        pi.output(bit5, False)

    if bin6 == '1':
        pi.output(bit6, True)
    elif bin6 == '0':
        pi.output(bit6, False)

    if bin7 == '1':
        pi.output(bit7, True)
    elif bin7 == '0':
        pi.output(bit7, False)

    print(bin1, "|", bin2, "|", bin3, "|", bin4,
          "|", bin5, "|", bin6, "|", bin7)

    # ================FPS PROGRAM===============
    frame = size(frame, 2)
    time2 = time.time()
    frame = FPS(frame, time1, time2)
    cv2.imshow('PROCESSED', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("A3ROSOL CAR STOPPED")
        break

pi.cleanup()
cap.release()
cv2.destroyAllWindows()
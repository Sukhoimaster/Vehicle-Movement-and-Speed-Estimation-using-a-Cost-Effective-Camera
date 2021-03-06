import numpy as np
import cv2
import time

"""
Optical Flow and it' estimation using the Lucas Kanade Method
Reference : http://docs.opencv.org/trunk/d7/d8b/tutorial_py_lucas_kanade.html
"""


cap = cv2.VideoCapture('/Volumes/TimeWarp/ONE_ROAD_VIDEO/11440006.AVI')

# params for ShiTomasi corner detection
NUMPOINTS = 800
feature_params = dict( maxCorners = NUMPOINTS,
                       qualityLevel = 0.05,
                       minDistance = 16,
                       blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0,255,(NUMPOINTS,3))


# Take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

# Create a mask image for drawing purposes
#mask = np.zeros_like(old_frame)

while(1):
    mask = np.zeros_like(old_frame)
    ret,frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # calculate optical flow
    p1 = p0 * 0.1
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, p1, None, **lk_params)

    # Select good points
    good_new = p1[st==1]
    good_old = p0[st==1]

    # draw the tracks
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
    img = cv2.add(frame,mask)

    cv2.imshow('frame',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)
    #p0 = p1

cv2.destroyAllWindows()
cap.release()
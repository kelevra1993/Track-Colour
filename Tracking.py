# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import pyautogui
import time
import wx
import sys
import thread
from time import sleep
camera = cv2.VideoCapture(0)

def main():
#menu contextuel

    class MyPopupMenu(wx.Menu):
        
        def __init__(self, parent):
            super(MyPopupMenu, self).__init__()
            
            self.parent = parent
    
            mmi = wx.MenuItem(self, wx.NewId(), 'Minimize')
            self.AppendItem(mmi)
            self.Bind(wx.EVT_MENU, self.OnMinimize, mmi)
    
            emi = wx.MenuItem(self, wx.NewId(), 'Right Click')
            self.AppendItem(emi)
            self.Bind(wx.EVT_MENU, self.OnRightClick, emi)
    
            fmi = wx.MenuItem(self, wx.NewId(), 'Left Click')
            self.AppendItem(fmi)
            self.Bind(wx.EVT_MENU, self.OnLeftClick, fmi)
    
            dmi = wx.MenuItem(self, wx.NewId(), 'Double Click')
            self.AppendItem(dmi)
            self.Bind(wx.EVT_MENU, self.OnDbClick, dmi)
    
            cmi = wx.MenuItem(self, wx.NewId(), 'Close')
            self.AppendItem(cmi)
            self.Bind(wx.EVT_MENU, self.OnClose, cmi)
    
    
        def OnMinimize(self, e):
            self.parent.Iconize()
    
        def OnClose(self, e):
            #self.parent.Close()
            stop()
            cv2.destroyAllWindows()
    
        def OnRightClick(self, e):
            pyautogui.click(button='right')
            
        def OnLeftClick(self, e):
            pyautogui.click()
    
        def OnDbClick(self, e):
            pyautogui.click(clicks=2)
    
    class Example(wx.Frame):
        def __init__(self, *args, **kwargs):
            super(Example, self).__init__(*args, **kwargs) 
        
            self.timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.pop, self.timer)
        
        def InZone(self):
            if self.timer.IsRunning():
                pass
            else:
                print "starting timer..."
                self.timer.Start(2000,True)
        
        def pop(self,event):
            
            self.timer.Stop()
            self.PopupMenu(MyPopupMenu(self))

        
        def NotInZone(self):
            
            print "stop timer"
            self.timer.Stop() 
     
    ex = wx.App()
    big=Example(None)
    
      #fin menu contextuel
         
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
            help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
            help="max buffer size")
    args = vars(ap.parse_args())
    
    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    greenLower =(29, 86, 6)
    greenUpper =(64, 255, 255)
     
    pts = deque(maxlen=args["buffer"])
    
    # if a video path was not supplied, grab the reference
    # to the webcam
    if not args.get("video", False):
            camera = cv2.VideoCapture(0)
    # otherwise, grab a reference to the video file
    else:
            camera = cv2.VideoCapture(args["video"])
    def nothing(x):
        pass
    calibration=True
    cv2.namedWindow('Calibrate')
    cv2.resizeWindow('Calibrate', 600, 320)
    cv2.createTrackbar('Low H ','Calibrate',0,179,nothing)
    cv2.createTrackbar('High H','Calibrate',0,179,nothing)
    cv2.createTrackbar('Low S ','Calibrate',0,255,nothing)
    cv2.createTrackbar('High S','Calibrate',0,255,nothing)
    cv2.createTrackbar('Low V ','Calibrate',0,255,nothing)
    cv2.createTrackbar('High V','Calibrate',0,255,nothing)
    cv2.createTrackbar('erosion-dilatation','Calibrate',0,3,nothing)
    
    while calibration==True :
        
        LH=cv2.getTrackbarPos('Low H ','Calibrate')
        HH=cv2.getTrackbarPos('High H','Calibrate')
        LS=cv2.getTrackbarPos('Low S ','Calibrate')
        HS=cv2.getTrackbarPos('High S','Calibrate')
        LV=cv2.getTrackbarPos('Low V ','Calibrate')
        HV=cv2.getTrackbarPos('High V','Calibrate')
        er=cv2.getTrackbarPos('erosion-dilatation','Calibrate')
        greenLower =(LH,LS,LV)
        greenUpper =(HH,HS,HV)
        
        (grabbed, frame) = camera.read()
        frame = cv2.flip(frame,1)
        frame = imutils.resize(frame, width=720)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        if(er==0):
            mask = cv2.inRange(hsv, greenLower, greenUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
        """if(er==1):
            mask = cv2.inRange(hsv, greenLower, greenUpper)
            mask = cv2.dilate(mask, None, iterations=2)
            mask = cv2.erode(mask, None, iterations=2)
        if(er==2):
            mask = cv2.inRange(hsv, greenLower, greenUpper)
            mask = cv2.erode(mask, None, iterations=2)
        if(er==3):
            mask = cv2.inRange(hsv, greenLower, greenUpper)
            mask = cv2.dilate(mask, None, iterations=2)"""
        
        
        #we show the result of the calibration
        cv2.imshow("mask", mask)
        
        key = cv2.waitKey(1) & 0xFF

        # if the 'N' key is pressed, the calibration is set and we move on
        if key == ord("n"):
                calibration=False
                cv2.destroyAllWindows()
                break
        #default configuration of the patch
        if key == ord("d"):
                calibration=False
                #we keep the calibration to green patch
                greenLower =(29, 86, 6)
                greenUpper =(64, 255, 255)
                cv2.destroyAllWindows()
                break   
    
    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    #greenLower =(29, 86, 6)
    #greenUpper =(64, 255, 255)
    #greenLower =(40, 30, 0)
    #greenUpper =(200, 255, 255)
    
    while True:

            # grab the current frame
            (grabbed, frame) = camera.read()
            #sleep(4)
            frame = cv2.flip(frame,1)

            frame = imutils.resize(frame, width=600)

            cv2.line (frame,(0,300),(600,300),(0, 0, 0),thickness=1,lineType=8,shift=0)
            cv2.line (frame,(0,150),(600,150),(0, 0, 0),thickness=1,lineType=8,shift=0)
            cv2.line (frame,(200,150),(200,300),(0, 0, 0),thickness=1,lineType=8,shift=0)
            cv2.line (frame,(400,150),(400,300),(0, 0, 0),thickness=1,lineType=8,shift=0)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            mask = cv2.inRange(hsv, greenLower, greenUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            #frame=mask
    
            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None
    
            # only proceed if at least one contour was found
            if len(cnts) > 0:
                    # find the largest contour in the mask, then use
                    # it to compute the minimum enclosing circle and
                    # centroid
                    c = max(cnts, key=cv2.contourArea)
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    frame = imutils.resize(frame, width=600)
                    
                    
                    # only proceed if the radius meets a minimum size
                    if radius > 15:
                            #left rectangle
                            if x<200 and y>150 and y<300:
                                pass
                                    #cv2.rectangle (frame,(0,300),(200,150),(0, 255, 255),thickness=-1, lineType=8,shift=0)
                            #rght rectangle
                            if x>400 and y<300 and y>150:
                                pass
                                    #cv2.rectangle (frame,(600,150),(400,300),(0, 255, 255),thickness=-1, lineType=8,shift=0)
                            #upper rectangle
                            if y<150 :
                                pass
                                    #cv2.rectangle (frame,(0,0),(600,150),(0, 255, 100),thickness=-1, lineType=8,shift=0)
                            #lower rectangle
                            if y>300 :
                                pass
                                    #cv2.rectangle (frame,(0,300),(600,450),(0, 255, 100),thickness=-1, lineType=8,shift=0)
                            #clic zone
                            if x>200 and x<400 and y>150 and y<300:
                                #cv2.rectangle (frame,(200,150),(400,300),(0, 255, 255),thickness=-1, lineType=8,shift=0)
                                pass
                            # draw the circle and centroid on the frame,
                            # then update the list of tracked points
                            cv2.circle(frame, (int(x), int(y)), int(radius),
                                    (0, 255, 255), 2)
                            cv2.circle(frame, center, 5, (0, 0, 255), -1)
                            #left movement
                            if x<200 and y>150 and y<300:
                                    big.NotInZone()
                                    c, d = pyautogui.position()
                                    pyautogui.moveTo(int(c-10),int(d))
                            #right movement
                            if x>400 and y<300 and y>150:
                                    big.NotInZone()
                                    c, d = pyautogui.position()
                                    pyautogui.moveTo(int(c+10),int(d))
                            #upward movement
                            if y<150 :
                                    big.NotInZone()
                                    c, d = pyautogui.position()
                                    pyautogui.moveTo(int(c),int(d-10))
                            #downward movement
                            if y>300 :
                                    big.NotInZone()
                                    c, d = pyautogui.position()
                                    pyautogui.moveTo(int(c),int(d+10))
    
                            #clic zone
                            if x>200 and x<400 and y>150 and y<300:
                                big.InZone()
                                #thread.start_new_thread(big.InZone,)
                                
                                
                            # update the points queue
                            pts.appendleft(center)
    
            # loop over the set of tracked points
            for i in xrange(1, len(pts)):
                    # if either of the tracked points are None, ignore them
                    if pts[i - 1] is None or pts[i] is None:
                            continue
    
            # show the frame to our screen
            
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
    
            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                    break
    

    # cleanup the camera and close any open windows
    stop()
    
def stop():
    camera.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    main()

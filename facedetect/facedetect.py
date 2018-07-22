#!/usr/bin/env python

'''
face detection using haar cascades

USAGE:
    facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv

# local modules
from video import create_capture
from common import clock, draw_str


def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                     flags=cv.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv.rectangle(img, (x1, y1), (x2, y2), color, 2)

#添加装饰
def draw_decorate(img, rects, color):
    for x1, y1, x2, y2 in rects:
        x = x1+(x2-x1)//2
        y = y1+(y2-y1)//2
        cv.circle(img,(x,y), 30, (0,0,255), -1)
        cv.putText(img,'Hello',(x-100,y-50), cv.FONT_HERSHEY_SIMPLEX, 2,(255,255,255),2,cv.LINE_AA)

if __name__ == '__main__':
    import sys, getopt
    print(__doc__)

    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    try:
        video_src = video_src[0]
    except:
        video_src = 0
    args = dict(args)
    cascade_fn = args.get('--cascade', r"D:\mycode\mypython\python-study\facedetect\haarcascade_frontalface_default.xml")
    nested_fn  = args.get('--nested-cascade', r"D:\mycode\mypython\python-study\facedetect\haarcascade_eye.xml")

    cascade = cv.CascadeClassifier(cascade_fn)
    nested = cv.CascadeClassifier(nested_fn)

    cam = create_capture(video_src)

    while True:
        ret, img = cam.read()
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray = cv.equalizeHist(gray)

        t = clock()
        rects = detect(gray, cascade)
        vis = img.copy()
        draw_rects(vis, rects, (0, 255, 0))#画脸
        # draw_decorate(vis, rects, (0, 255, 0))
        
        if not nested.empty():
            for x1, y1, x2, y2 in rects:
                #roi = gray[y1:y2, x1:x2] 
                vis_roi = vis[y1:y2, x1:x2] #提取到的人脸图像
                #subrects = detect(roi.copy(), nested)#监测眼睛
                cv.imshow('face_',vis_roi)#展示人脸
                #draw_rects(vis_roi, subrects, (255, 0, 0)) #描边眼睛
        
        dt = clock() - t

        draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
        cv.imshow('facedetect', vis)
        
        if cv.waitKey(5) == ord('q'):
            break
    cv.destroyAllWindows()

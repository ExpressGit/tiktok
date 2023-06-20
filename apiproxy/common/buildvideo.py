
#!/usr/bin/env python  
# encoding: utf-8 
#Imports
import cv2
import os
import numpy as np
import re 
import time


video = cv2.VideoWriter('outpu.mp4', 0, int(vid.get(cv2.CAP_PROP_FPS)), (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))))
images = [img for img in os.listdir(os.path.join(dir,'Temp')) if img.endswith(".jpg")]
images = sortedproper(images)
for image in images:
    print(image)
    video.write(cv2.imread(image))

#Cleanup and print execution time
video.release()
vid.release()
print("--- %s seconds ---" % (time.time() - start_time))
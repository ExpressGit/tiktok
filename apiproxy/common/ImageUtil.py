#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: img_utils.py 
@time: 2019-12-25 14:23 
@description：图片工具类
"""
import cv2,os
from moviepy.video.VideoClip import ImageClip
from moviepy.editor import VideoFileClip

class ImageUtil(object):
    
    def __init__(self):
        pass
    
    def one_pic_to_video(self,image_path, output_video_path, fps, time):
        """
        一张图片合成视频,将图片作为背景
        one_pic_to_video('./../source/1.jpeg', './../source/output.mp4', 25, 10)
        :param path: 图片文件路径
        :param output_video_path:合成视频的路径
        :param fps:帧率
        :param time:时长
        :return:
        """

        image_clip = ImageClip(image_path)
        img_width, img_height = image_clip.w, image_clip.h

        # 总共的帧数
        frame_num = (int)(fps * time)

        img_size = (int(img_width), int(img_height))

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

        video = cv2.VideoWriter(output_video_path, fourcc, fps, img_size)

        for index in range(frame_num):
            frame = cv2.imread(image_path)
            # 直接缩放到指定大小
            frame_suitable = cv2.resize(frame, (img_size[0], img_size[1]), interpolation=cv2.INTER_CUBIC)

            # 把图片写进视频
            # 重复写入多少次
            video.write(frame_suitable)

        # 释放资源
        video.release()

        return VideoFileClip(output_video_path)


if __name__ == '__main__':
    imgutil = ImageUtil()
    img_dir = '/root/video_download/bili/浅影阿_/2023-05-27'
    imgutil.one_pic_to_video(os.path.join(img_dir,'Temp'),os.path.join(img_dir,'out.mp4'),24,144)
    
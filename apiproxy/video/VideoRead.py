#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import json
import time
import copy
import os
import hashlib

class VideoUtil(object):
    def __init__(self, root_dir):
        self.root_dir = root_dir  # 所有类型视频的根目录
        
    def findAllFiles(self):
        # 读取所有视频文件
        for root, ds, fs in os.walk(self.root_dir):
            for f in fs:
                fullname = os.path.join(root, f)
                yield fullname

    def findDateFiles(self,date_str):
        # 三个文件夹 douyin\bili\youtube
        # 读取文件并记录路径
        bili_file_list = []
        douyin_file_list = []
        youtube_file_list = []
        for file_path in vd.findAllFiles():
            if date_str in file_path:
                if 'douyin' in file_path:
                    douyin_file_list.append(file_path)
                if 'bili' in file_path:
                    bili_file_list.append(file_path)
                if 'youtube' in file_path:
                    youtube_file_list.append(file_path)
        return douyin_file_list,bili_file_list,youtube_file_list
    
    def findDateVideoFiles(self,date_str):
        # 三个文件夹 douyin\bili\youtube
        # 读取视频文件并记录路径
        bili_video_list = []
        douyin_video_list = []
        youtube_video_list = []
        douyin_file_list,bili_file_list,youtube_file_list = self.findDateFiles(date_str)
        for file in douyin_file_list:
            if file.endswith('.mp4'):
                douyin_video_list.append(file)
        
        for file in bili_file_list:
            if file.endswith('.mp4'):
                bili_video_list.append(file)

        for file in youtube_file_list:
            if file.endswith('.mp4'):
                youtube_video_list.append(file)
        return douyin_video_list,bili_video_list,youtube_video_list

    def get_video_md5(self,file_path):
        """
        分段读取，获取文件的md5值
        :param file_path:
        :return:
        """
        with open(file_path, 'rb') as file:
            md5_obj = hashlib.md5()
            while True:
                buffer = file.read(8096)
                if not buffer:
                    break
                md5_obj.update(buffer)
            hash_code = md5_obj.hexdigest()
        md5 = str(hash_code).lower()
        return md5
    
    def modify_file_md5(self,file_path):
        """
        修改文件的md5值
        :param file_path:
        :return:
        """
        with open(file_path, 'a') as file:
            file.write("####&&&&")

    def modify_videos_md5(self,video_files):
        """
            批量修改视频文件md5
        """
        if len(video_files)>0:
            for video in video_files:
                self.modify_file_md5(video)

    def checkRepeatVideo(self):
        # https://juejin.cn/s/cv2.videocapture%E5%BF%BD%E7%95%A5%E9%87%8D%E5%A4%8D%E5%B8%A7
        video_path = "your_video_path"
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        prev_frame = frame
        prev_timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)

        while ret:
            ret, frame = cap.read()
            if not ret:
                break
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
            if (frame == prev_frame).all() and timestamp == prev_timestamp:
                continue
            # 处理当前帧
            # ...
            prev_frame = frame
            prev_timestamp = timestamp
        cap.release()

if __name__ == '__main__':
    root_dir = '/root/video_download/douyin'
    date_str = '2023-06-07'
    vd = VideoUtil(root_dir=root_dir)
    file_name = '/root/video_download/douyin/user_小透明/post/2023-06-07/2023-06-07 19.12.41_考完了咱主打一个反差反差/2023-06-07 19.12.41_考完了咱主打一个反差反差_video.mp4'
    # douyin_video_list,bili_video_list,youtube_video_list= vd.findDateVideoFiles(date_str)
    #md5 修改
    # origin_md5 = vd.get_video_md5(file_name)
    # print(origin_md5)
    # vd.modify_file_md5(file_name)
    # new_md5 = vd.get_video_md5(file_name)
    # print(new_md5)

    

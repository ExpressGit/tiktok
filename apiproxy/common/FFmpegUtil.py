#!/usr/bin/env python  
# encoding: utf-8


# coding=utf-8
import os
import subprocess
import datetime
import json, pprint
import re, time
import threading
import random
import shutil


class FFmpeg(object):

    def __init__(self, editvdo, addlogo=None, addmusic=None):
        self.editvdo = editvdo
        self.addlogo = addlogo
        self.addmusic = addmusic
        # self.vdo_time, self.vdo_width, self.vdo_height, self.attr_dict = self.get_attr()
        self.editvdo_path = os.path.dirname(editvdo)
        self.editvdo_name = os.path.basename(editvdo)

    def get_attr(self):
        """
        获取视频属性参数
        :return:
        """
        strcmd = r'ffprobe -print_format json -show_streams -i "{}"'.format(self.editvdo)
        status, output = subprocess.getstatusoutput(strcmd)
        agrs = eval(re.search('{.*}', output, re.S).group().replace("\n", "").replace(" ", ''))
        streams = agrs.get('streams', [])
        agrs_dict = dict()
        [agrs_dict.update(x) for x in streams]
        vdo_time = agrs_dict.get('duration')
        vdo_width = agrs_dict.get('width')
        vdo_height = agrs_dict.get('height')
        attr = (vdo_time, vdo_width, vdo_height, agrs_dict)
        return attr

    def edit_head(self, start_time, end_time, deposit=None):
        """
        截取指定长度视频
        :param second: 去除开始的多少秒
        :param deposit: 另存为文件
        :return: True/Flase
        """
        if None == deposit:
            deposit = self.editvdo_path+'/'+'edit_head'+self.editvdo_name
        start = time.strftime('%H:%M:%S', time.gmtime(start_time))
        end = time.strftime('%H:%M:%S', time.gmtime(end_time))
        strcmd = 'ffmpeg  -i "{}" -vcodec copy -acodec copy -ss {} -to {} "{}" -y'.format(
            self.editvdo, start, end, deposit)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        if os.path.exists(deposit):
            os.remove(self.editvdo)
            os.rename(deposit, self.editvdo)
            return True
        else:
            return False
        
    def remove_45_bili_logo(self,video_width,video_height,logo_position,deposit=None):
        """
        去除bili水印(4:5视频)
        :param roi:水印坐标 左上方，右上方，右下方logo
        :return: True/False
        """
        if os.path.exists(deposit):
            os.remove(deposit)
        # ffmpeg -i 'a.mp4' -b:v 3441k -vf "delogo=x=1593:y=30:w=320:h=80:show=0" -c:a copy "no_logo.mp4"
        w = 700
        h = 200
        x_right = video_width*0.60
        h_bottom = video_height*0.9
        if video_height<=930:
            w = 130
            h = 60
        
        if logo_position == 'rightbottom':
            strcmd = 'ffmpeg  -i "{}" -vf "delogo=x={}:y={}:w={}:h={}:show=0" -c:a copy "{}" '.format(
            self.editvdo,x_right,h_bottom,w,h,deposit)

        if logo_position == 'righttop':
            strcmd = 'ffmpeg  -i "{}" -vf "delogo=x={}:y=60:w={}:h={}:show=0" -c:a copy "{}" '.format(
            self.editvdo,x_right,w,h,deposit)

        if logo_position == 'lefttop':
            strcmd = 'ffmpeg  -i "{}" -vf "delogo=x=50:y=60:w={}:h={}:show=0" -c:a copy "{}" '.format(
            self.editvdo,w,h,deposit)
        
        if logo_position == 'leftbottom':
            strcmd = 'ffmpeg  -i "{}" -vf "delogo=x=50:y={}:w={}:h={}:show=0" -c:a copy "{}" '.format(
            self.editvdo,h_bottom,w,h,deposit)
        
        if logo_position == 'empty':
            strcmd = 'ffmpeg  -i "{}"  -c:a copy "{}" '.format(
            self.editvdo, deposit)
       
        print("remove_45_bili_logo {} strcmd: {}".format(video_width,strcmd))
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)

    def remove_169_bili_logo(self,video_width,video_height,logo_position,deposit=None):
        """
        去除bili水印 16:9
        :param roi:水印坐标 左上方，右上方，右下方logo
        :return: True/False
        """
        if os.path.exists(deposit):
            os.remove(deposit);
        # fix 852*480
        w = 260
        h = 80
        if video_width<=680 :
            w = 160
            h = 50
        elif video_width<=950:
            w = 200
            h = 60
            
        # ffmpeg -i 'a.mp4' -b:v 3441k -vf "delogo=x=1593:y=30:w=320:h=80:show=0" -c:a copy "no_logo.mp4"
        x_right = video_width*0.7
        h_bottom = video_height*0.85
        # rightbottom，righttop，lefttop，leftbottom,empty

        if logo_position == 'rightbottom':
            strcmd = 'ffmpeg  -i "{}" -vf "delogo=x={}:y={}:w={}:h={}:show=0" -c:a copy "{}" '.format(
            self.editvdo, x_right,h_bottom,w,h,deposit)

        if logo_position == 'righttop':
            strcmd = 'ffmpeg  -i "{}" -vf "delogo=x={}:y=30:w={}:h={}:show=0" -c:a copy "{}" '.format(
            self.editvdo, x_right,w,h,deposit)

        if logo_position == 'lefttop':
            strcmd = 'ffmpeg  -i "{}" -vf "delogo=x=30:y=30:w={}:h={}:show=0" -c:a copy "{}" '.format(
            self.editvdo,w,h,deposit)
        
        if logo_position == 'leftbottom':
            strcmd = 'ffmpeg  -i "{}" -vf "delogo=x=30:y={}:w={}:h={}:show=0" -c:a copy "{}" '.format(
            self.editvdo, h_bottom,w,h,deposit)
        
        if logo_position == 'empty':
            strcmd = 'ffmpeg  -i "{}"  -c:a copy "{}" '.format(
            self.editvdo, deposit)

        print("remove_169_bili_logo {} strcmd: {}".format(video_width,strcmd))
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
    
    def edit_metadata(self,deposit=None):
        """
        修改视频的metadata信息
        :param deposit:修改后另存为路径，为空则覆盖
        :return: True/False
        ffmpeg -i a.mp4 -vcodec copy -acodec copy -metadata comment=sanyuanchuanmei -metadata description=sanyuanchuanmei  b.mp4 -y
        """
        strcmd = 'ffmpeg -i "{}" -vcodec copy -acodec copy -metadata comment='' -metadata description='' "{}" -y'.format(
                    self.editvdo,deposit)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        return True
    
    def add_video_subtitle(self, srt_file ,deposit=None):
        """
        添加视频字幕
        :param deposit:添加字幕后另存为路径，为空则覆盖
        :return: True/False
        """
        FONT_URL = 'apiproxy/font/HYBiRanTianTianQuanW-2.ttf'
        strcmd = 'ffmpeg -i "{}" -vf "subtitles={}" -c:a copy "{}" '.format(
                    self.editvdo, srt_file, deposit)
        print(strcmd)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        return True

    def edit_logo(self, deposit=None):
        """
        添加水印
        :param deposit:添加水印后另存为路径，为空则覆盖
        :return: True/False
        """
        if None == deposit:
            deposit = self.editvdo_path+'/'+'edit_logo'+self.editvdo_name
        strcmd = r'ffmpeg -i "{}" -vf "movie=\'{}\' [watermark];[in] ' \
                 r'[watermark] overlay=main_w-overlay_w-10:10 [out]"  "{}"'.format(
                    self.editvdo, self.addlogo, deposit)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        if os.path.exists(deposit):
            os.remove(self.editvdo)
            os.rename(deposit, self.editvdo)
            return True
        else:
            return False

    
    def edit_music(self, deposit=None):
        if None == deposit:
            deposit = self.editvdo_path+'/'+'edit_music'+self.editvdo_name
        strcmd = r'ffmpeg -y -i "{}" -i "{}" -filter_complex "[0:a] ' \
                 r'pan=stereo|c0=1*c0|c1=1*c1 [a1], [1:a] ' \
                 r'pan=stereo|c0=1*c0|c1=1*c1 [a2],[a1][a2]amix=duration=first,' \
                 r'pan=stereo|c0<c0+c1|c1<c2+c3,pan=mono|c0=c0+c1[a]" ' \
                 r'-map "[a]" -map 0:v -c:v libx264 -c:a aac ' \
                 r'-strict -2 -ac 2 "{}"'.format(self.editvdo, self.addmusic, deposit)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        if os.path.exists(deposit):
            os.remove(self.editvdo)
            os.rename(deposit, self.editvdo)
            return True
        else:
            return False

    def edit_rate(self, rete=30, deposit=None):
        """
        改变帧率
        :param rete: 修改大小帧率
        :param deposit: 修改后保存路径
        :return:
        """
        if None == deposit:
            deposit = self.editvdo_path+'/'+'edit_music'+self.editvdo_name
        strcmd = r'ffmpeg -i "{}" -r {} "{}"' % (self.editvdo, rete, deposit)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        if os.path.exists(deposit):
            os.remove(self.editvdo)
            os.rename(deposit, self.editvdo)
            return True
        else:
            return False

    def edit_power(self, power='1280x720', deposit=None):
        """
        修改分辨率
        :param power: 分辨率
        :param deposit: 修改后保存路径，为空则覆盖
        :return:
        """
        if None == deposit:
            deposit = self.editvdo_path+'/'+'edit_power'+self.editvdo_name
        strcmd = r'ffmpeg -i "{}" -s {} "{}"'.format(self.editvdo, power, deposit)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        if os.path.exists(deposit):
            os.remove(self.editvdo)
            os.rename(deposit, self.editvdo)
            return True
        else:
            return False

    def rdit_marge(self, vdo_head, vdo_tail, deposit=None):
        if None == deposit:
            deposit = self.editvdo_path+'/'+'rdit_marge'+self.editvdo_name
        with open(self.editvdo_path+'/'+'rdit_marge.txt', 'w', encoding='utf-8') as f:
            f.write("file '{}' \nfile '{}' \nfile '{}'" .format(
                vdo_head, self.editvdo, vdo_tail))
        strcmd = r'ffmpeg -f concat -safe 0 -i "{}" -c copy "{}"'.format(
            self.editvdo_path + '/' + 'rdit_marge.txt', deposit)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        if os.path.exists(deposit):
            os.remove(self.editvdo)
            os.rename(deposit, self.editvdo)
            return True
        else:
            return False

if __name__ == '__main__':
    video_path = '/root/video_download/douyin/user_小透明/post/2023-07-01/2023-07-01 11.18.00_哦一颗新鲜的土豆/哦一颗新鲜的土豆_edit.mp4'
    deposit = '/root/video_download/douyin/user_小透明/post/2023-07-01/2023-07-01 11.18.00_哦一颗新鲜的土豆/哦一颗新鲜的土豆_new.mp4'
    ffmpegUtil = FFmpeg(video_path)
    ffmpegUtil.edit_metadata(deposit)
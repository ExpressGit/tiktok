'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2023-07-10 17:06:50
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2023-07-17 10:07:52
FilePath: /tiktok/apiproxy/common/YoutuberVideo,py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import time
import copy
import os,sys
import hashlib
from yt_dlp import YoutubeDL
import subprocess
import shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from apiproxy.common.utils import Utils


class YoutuberVideo(object):
    
    def __init__(self):
        self.util = Utils()
   
    def download_from_youtube_up_space(self,video_format,num_works,space_link,day_str):
        '''
        从up主的空间定时下载视频
        #yt-dlp  -f "bv[ext=mp4]"  -k -N 2 --post-overwrites --dateafter 20230707 --write-subs  --sub-format srt https://www.youtube.com/@sunkemito/videos 
        '''
        strcmd = r'yt-dlp  -f "bv[ext={}]"  -k -N {} --post-overwrites --dateafter {} --write-subs  --sub-format srt {} '.format(
                    video_format,num_works,day_str,space_link)
        print(strcmd)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        print(result)
        if result.returncode==0:
            print("youtube channel downlaod video failed url:{} , date: {}:".format(space_link,day_str))
            return True
        else:
            return False
        
    def download_from_youtube_up_single_video(self,video_format,video_link):
        '''
        指定单个长视频或短视频（shorts）文件下载命令
        yt-dlp  -f "bv[ext=mp4]"  -k --post-overwrites  --write-subs  --sub-format srt https://www.youtube.com/watch?v=9qL-eqaG2kk
        '''
        strcmd = r'yt-dlp  -f "bv[ext={}]"  -k --post-overwrites  --write-subs  --sub-format srt {} '.format(
                    video_format,video_link)
        print(strcmd)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        print(result)
        if result.returncode==0:
            print("youtube channel downlaod video failed url:{} ,".format(video_link))
            return True
        else:
            return False

    def get_youtube_config(self):
        """
        get youtube config
        """
        youtube_config = '/root/workspace/tiktok/config/youtube_config.yml'
        config_dict = self.util.get_video_config_dict(youtube_config)
        return config_dict
        
    
    
    def build_web_data_dict(self,error_code,seriza_info,video_name):
        """
        构建web端返回的数据结构
        """
        url_download = ''
        result = {}
        youtube_config = self.get_youtube_config()
        temp_dir = youtube_config['temp_dir']
        address_ip = youtube_config['address_ip']
        video_path = os.path.join(temp_dir,video_name)
        new_video_path = video_path.replace("video_download","video_deliver")
        if not os.path.exists(new_video_path):
            shutil.copyfile(video_path,new_video_path)
        url_download = 'http://{}/temp_video/{}'.format(address_ip,video_name)
        result['data'] = {}
        result['data']['awemeType'] = 0
        result['data']['video'] = {}
        result['data']['video']['play_addr'] = {}
        result['data']['video']['cover_original_scale'] = {}
        result['data']['video']['dynamic_cover'] = {}
        result['data']['music'] = {}
        result['data']['music']['play_url'] = {}
        result['data']['author'] = {}
        result['data']['author']['avatar'] = {}
        result['data']['statistics'] = {}
        if error_code == 0:
            result["status_code"]=200
            #视频封面
            result['data']['video']['play_addr']['url_list']=[url_download] #视频下载地址
            
            result['data']['video']['cover_original_scale']['url_list']=[seriza_info['thumbnail']]
            result['data']['video']['dynamic_cover']['url_list']=[seriza_info['thumbnail']]
            result['data']['music']['play_url']['url_list']=[seriza_info['thumbnails'][0]['url']]
            #头像
            result['data']['author']['avatar']['url_list']=[seriza_info['thumbnail']]
            result['data']['author']['nickname']=seriza_info['uploader']
            result['data']['desc'] = seriza_info['fulltitle']
            #up主数据
            result['data']['statistics']['digg_count'] = seriza_info['channel_follower_count']
            result['data']['statistics']['collect_count'] = seriza_info['like_count']
            result['data']['statistics']['share_count'] = 0
            result['data']['statistics']['comment_count'] = seriza_info['comment_count']
        else:
            result["status_code"]=500
        print(result)
        return result
    
    def download_from_embed_single_video(self,video_link):
        '''
        通过yt-dlp python download video
        '''
        ydl_opts =  {
            'format': 'bv[ext=mp4]',
            #'format': 'bv*+ba/b', # video+audio
            # 'paths':{'home':'%(title)s.%(ext)s'},
            'outtmpl':'/root/video_download/temp_video/%(id)s.%(ext)s'
        }
        result = {}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_link, download=False)
            seriza_info = ydl.sanitize_info(info)
            error_code = ydl.download(video_link)
        video_name = seriza_info['id']+'.'+seriza_info['ext']
        result = self.build_web_data_dict(error_code,seriza_info,video_name)     
        return result,seriza_info
    
if __name__ == '__main__':
    youtube = YoutuberVideo()
    video_link = 'https://www.youtube.com/watch?v=3uwrwOHl_8c'
    # out_put_template = '/root/video_download/temp_video/%(title)s.%(ext)s'
    # result = youtube.download_from_youtube_up_single_video(video_format,video_link)
    error_code,seriza_info = youtube.download_from_embed_single_video(video_link)
    print(error_code)
    
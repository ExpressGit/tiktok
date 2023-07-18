#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@FileName   : BiliCommand.py
@Project    : apiproxy
@Description: 
@Author     : imgyh
@Mail       : admin@imgyh.com
@Github     : https://github.com/imgyh
@Site       : https://www.imgyh.com
@Date       : 2023/5/12 16:01
@Version    : v1.0
@ChangeLog 
------------------------------------------------

------------------------------------------------
'''

import argparse
import os
import sys,datetime
import json
import yaml,tqdm
import time
from yt_dlp import YoutubeDL
import subprocess
import re



 
def build_youtube_download_channle_command(link,beginday):
        #yt-dlp  -f "bv[ext=mp4]"  -k --post-overwrites --dateafter 20230707 --write-subs  --sub-format srt https://www.youtube.com/@sunkemito/videos  
        """
        下载 YouTube 频道
        :return: True/False
        """
        
        strcmd = r'yt-dlp  -f "bv[ext=mp4]"  -k3232 --post-overwrites --dateafter {} --write-subs  --sub-format srt {} '.format(
                    beginday,link)
        print(strcmd)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        print(result)
        if result.returncode==0:
            print("youtube channel downlaod video failed:",link)
            return True
        else:
            return False

def build_youtube_download_single_video(link):
    """
    下载指定link 的视频 
    yt-dlp  -f "bv[ext=mp4]"  -k --post-overwrites  --write-subs  --sub-format srt https://www.youtube.com/watch?v=9qL-eqaG2kk
    """
    strcmd = r'yt-dlp  -f "bv[ext=mp4]"  -k --post-overwrites  --write-subs  --sub-format srt {}'.format(
                    link)
    print(strcmd)
    result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
    print(result)
    if result.returncode==0:
        print("youtube channel downlaod video failed:",link)
        return True
    else:
        return False

def extract_video_info():
    URL = 'https://www.youtube.com/watch?v=mnUjsGGgsns'

    # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)
        sanitize_info = ydl.sanitize_info(info)
        info_json = json.dumps(sanitize_info)
        # ℹ️ ydl.sanitize_info makes the info json-serializable
        print(info_json)

def download_youtube_video():
    URLS = ['https://www.youtube.com/watch?v=BaW_jenozKc']
    with YoutubeDL() as ydl:
        error_code = ydl.download(URLS)

def judge_link_type(url):
    """
    判断url来自于哪个平台：youtube\douyin\bili\tiktok
    tiktoke:https://www.tiktok.com/@honorofkingscamp/video/7253433005253872939?is_from_webapp=1&sender_device=pc
    youtube:
    """
    platform = ''
    if len(url)==0:
        return False
    if re.search(r"(v.douyin)+",url):
        platform='douyin'
    elif re.search(r"(youtube.com)+",url):
        platform='youtube'
    elif re.search(r"(bilibili.com)+",url):
        platform='bili'
    elif re.search(r"(tiktok.com)+",url):
        platform='tiktok'
    else:
        platform=''
    return platform

if __name__ == "__main__":
    url = 'https://www.youtube.com/watch?v=BaW_jenozKc'
    beginday='20230707'
    # build_youtube_download_channle_command(url,beginday)
    # build_youtube_download_single_video(url)
    # extract_video_info()
    # download_youtube_video()
    # url = 'https://v.douyin.com/kcvMpuN/'
    # url ='https://www.youtube.com/watch?v=tGGaHHLbb1o'
    # url = 'https://www.bilibili.com/video/BV19j411o7BZ/?spm_id_from=333.999.0.0&vd_source=ea41ada76e180cf6c5af0f913147e4c0'
    url = 'https://www.tiktok.com/@honorofkingscamp/video/7253433005253872939?is_from_webapp=1&sender_device=pc'
    platform = judge_link_type(url)
    print(platform)
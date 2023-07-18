'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2023-07-10 17:06:50
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2023-07-18 20:25:33
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
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import shutil
from apiproxy.common.utils import Utils

class BiliVideo(object):
    
    def __init__(self):
       self.util = Utils()
       
    def download_single_bili_video_command(self,link):
        #yutto https://www.bilibili.com/video/BV13P411C7eE 1 -q 127 --output-format mp4 -d /root/video_download/temp -c 25ae6104%2C1703209865%2Ceff30%2A61T12ccqWBkcccaWqYaWMTRi5uWeD-TYCas46A5sbfdsgQsZVe02TUjmrheRO_kAjLL22EbQAAKQA --no-danmaku -tp {id}
        """
        https://www.bilibili.com/video/BV1vZ4y1M7mQ
        :param deposit:添加字幕后另存为路径，为空则覆盖
        :return: True/False
        """
        bili_config = self.get_bili_config()
        strcmd = r'yutto  {} -n 1 -q 127 --output-format mp4 '\
                 r' -d "{}" -c "{}" --no-danmaku -tp {id} '.format(
                    link,bili_config['temp_dir'],bili_config['cookie'])
        print(strcmd)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        video_name = link.split('/')[-1]
        result = self.build_web_data_dict(result.returncode,video_name)     
        return result
       
   
   
    def build_web_data_dict(self,error_code,video_name):
        """
        构建web端返回的数据结构
        """
        url_download = ''
        result = {}
        bili_config = self.get_bili_config()
        temp_dir = bili_config['temp_dir']
        address_ip = bili_config['address_ip']
        video_file_name = video_name+'.mp4'
        video_path = os.path.join(temp_dir,video_file_name)
        new_video_path = video_path.replace("video_download","video_deliver")
        if not os.path.exists(new_video_path):
            shutil.copyfile(video_path,new_video_path)
        url_download = 'http://{}/temp_video/{}'.format(address_ip,video_file_name)
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
            result['data']['video']['cover_original_scale']['url_list']=[]
            result['data']['video']['dynamic_cover']['url_list']=[]
            result['data']['music']['play_url']['url_list']=[]
            #头像
            result['data']['author']['avatar']['url_list']=[]
            result['data']['author']['nickname']=''
            result['data']['desc'] = video_name
            #up主数据
            result['data']['statistics']['digg_count'] = 0
            result['data']['statistics']['collect_count'] = 0
            result['data']['statistics']['share_count'] = 0
            result['data']['statistics']['comment_count'] = 0
        else:
            result["status_code"]=500
        print(result)
        return result
    
      
    def build_bili_download_command(self,link,path,n,q,output_format,tp,cookie,danmuku,beginday,endday):
        #yutto --batch https://space.bilibili.com/314480501 -n 1 -q 120 --output-format mp4 -d /root/video_download/bili -c 25ae6104%2C1703209865%2Ceff30%2A61T12ccqWBkcccaWqYaWMTRi5uWeD-TYCas46A5sbfdsgQsZVe02TUjmrheRO_kAjLL22EbQAAKQA --no-danmaku -tp {username}_{owner_uid}/{pubdate}/{name} --batch-filter-start-time 2023-06-21 --batch-filter-end-time 2023-06-28
        """
        添加视频字幕
        :param deposit:添加字幕后另存为路径，为空则覆盖
        :return: True/False
        """
        
        strcmd = r'yutto --batch "{}" -n {} -q {} --output-format "{}" '\
                 r' -d "{}" -c "{}" --no-danmaku -tp "{}" '\
                 r' --batch-filter-start-time "{}" --batch-filter-end-time "{}"'.format(
                    link, n,q,output_format,path,cookie,tp.replace("\\",""),beginday,endday)
        print(strcmd)
        
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        if not result:
            print("link downlaod video failed:",link)
        return True
   
    
    def get_bili_config(self):
        """
        get bili config
        """
        bili_config = '/root/workspace/tiktok/config/bili_config.yml'
        config_dict = self.util.get_video_config_dict(bili_config)
        return config_dict
    
    

if __name__ == '__main__':
    link = 'https://www.bilibili.com/video/BV1vZ4y1M7mQ'
    bili = BiliVideo()
    result = bili.download_single_bili_video_command(link)
    print(result)
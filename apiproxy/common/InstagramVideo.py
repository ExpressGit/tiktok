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
import time,datetime
import copy
from moviepy.editor import *
import os,sys
import hashlib
import subprocess
from random import choice
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import shutil
from apiproxy.common.utils import Utils
import asyncio
from instaloader import Instaloader,Post


class InstagramVideo(object):
    
    def __init__(self):
       self.util = Utils()
       self.config = self.get_instagram_config()
       self.loader = Instaloader(dirname_pattern=self.config['temp_dir'],filename_pattern='{owner_username}/{date_utc:%Y-%m-%d}/{target}')
       self.loader.load_session_from_file('santangworld')
    
    def download_single_instgram_video(self,link):
        """
        demo1 :https://www.instagram.com/p/Cu1hn7BJfqI/?img_index=1 多张图片
        demo2 :https://www.instagram.com/p/Cu_-h4GJdgO/  一张图片
        demo3 :https://www.instagram.com/p/CpN6lOVJgfI/  一个视频
        :param deposit:添加字幕后另存为路径，为空则覆盖
        :return: True/False
        """
        # link = 'Cu_-h4GJdgO'
        link = link.split('/p/')[1].replace("/",'')
        temp_dir = self.config['temp_dir']
        # loader = Instaloader(dirname_pattern=temp_dir,filename_pattern='{owner_username}/{date_utc:%Y-%m-%d}/{target}')
        # loader.load_session_from_file('santangworld')
        # loader.download_feed_posts(max_count=20, fast_update=True,
        #                    post_filter=lambda post: post.likes>100 & post.date_local >= '2023-07-24')
        post = Post.from_shortcode(self.loader.context, link)
        owner_username = post.profile
        output_format = "%Y-%m-%d"
        date_str = self.util.convert_utc_to_string(post.date_utc,output_format)
        print(post.shortcode)
        image_folder = os.path.join(temp_dir,owner_username,date_str)
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        download_url = ''
        if post.typename=='GraphVideo':
            #video
            download_url = post.video_url
            result = self.build_web_data_dict(True,post,download_url)
            pass
        elif post.typename=='GraphImage':
            #image
            download_url = post.url
            result = self.build_web_data_dict(True,post,download_url)
        else:
            #images
            code = self.loader.download_post(post,target=post.shortcode)
            duration = 5
            fps = 24
            output_file = os.path.join(image_folder,post.shortcode+'.mp4')
            self.images_to_video(output_file,image_folder,fps,duration)
            temp_dir = self.config['temp_dir']
            address_ip = self.config['address_ip']
            new_video_path = output_file.replace("video_download","video_deliver")
            if not os.path.exists(new_video_path):
                if not os.path.exists(os.path.dirname(new_video_path)) :
                    os.makedirs(os.path.dirname(new_video_path))
                    shutil.copyfile(output_file,new_video_path)
            download_url = 'http://{}/temp_video/{}'.format(address_ip,new_video_path.split('temp_video/')[1])
            result = self.build_web_data_dict(code,post,download_url)
        # 删除临时文件
        if os.path.exists(image_folder):
            shutil.rmtree(image_folder)
        return result
       
   
    def build_web_data_dict(self,code,post,download_url):
        """
        构建web端返回的数据结构
        """
        result = {}
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
        if code :
            result["status_code"]=200
            #视频封面
            result['data']['video']['play_addr']['url_list']=[download_url] #视频下载地址
            result['data']['video']['cover_original_scale']['url_list']=[post.url]
            result['data']['video']['dynamic_cover']['url_list']=[post.url]
            result['data']['music']['play_url']['url_list']=[post.url]
            #头像
            result['data']['author']['avatar']['url_list']=[post.owner_profile.profile_pic_url]
            result['data']['author']['nickname']=post.owner_profile.username
            result['data']['desc'] = post.pcaption
            #up主数据
            result['data']['statistics']['digg_count'] = post.likes
            result['data']['statistics']['collect_count'] = 0
            result['data']['statistics']['share_count'] = 0
            result['data']['statistics']['comment_count'] = post.comments
        else:
            result["status_code"]=500
        print(result)
        return result
    

    def images_to_video(self,output_file, image_folder, fps, duration):
        '''
        将图片合成video
        '''
        # 获取图片文件夹中所有的图片文件名
        images = [f"{image_folder}/{img}" for img in os.listdir(image_folder) if img.endswith(".jpg")]
        
        if len(images)==0:
            return False
        
        # 创建一个ImageClip对象列表，每个对象对应一个图片
        clips = [ImageClip(img).set_duration(duration/len(images)) for img in images]

        # 将ImageClip对象列表合成为一个VideoClip对象
        video = concatenate_videoclips(clips, method="compose")

        # 设置视频的帧率
        video = video.set_fps(fps)

        # 设置视频的总时长
        video = video.set_duration(duration)

        # 保存合成的视频文件
        video.write_videofile(output_file, codec="libx264")
        return True
   
    
    def get_instagram_config(self):
        """
        get insta config
        """
        insta_config = '/root/workspace/tiktok/config/instagram_config.yml'
        config_dict = self.util.get_video_config_dict(insta_config)
        return config_dict
    


if __name__ == '__main__':
    url = 'https://www.instagram.com/p/CpN6lOVJgfI/'
    short_code = 'CpN6lOVJgfI'
    insta = InstagramVideo()
    configs = insta.get_instagram_config()
    date_str = '2023-07-19'
    save_path = '/root/video_download/bili'
    insta.download_single_instgram_video(url)
    # str = 'BV1Z8411U7ud_Bin：亚运会，我们要冠军！.mp4'
    # video_name = str[:-4].split("_")[-1]
    # print(video_name)
    # -tp "{username}_{owner_uid}/{pubdate}/{name}"  --batch-filter-start-time "2023-07-17" --batch-filter-end-time "2023-07-18"
    
    # 使用datetime.fromtimestamp()函数将时间戳转换为datetime对象
    
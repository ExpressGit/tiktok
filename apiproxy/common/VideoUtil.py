#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import json
import time
import copy
import os
import hashlib
from moviepy.editor import *
import random
from moviepy.video.tools.drawing import circle

class VideoRead(object):
    def __init__(self, root_dir=None):
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
        for file_path in self.findAllFiles():
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


class VideoUtil(object):
    def __init__(self):
        pass
        
    def time_to_hms(self,seconds_time):
        """
        时间转为时分秒
        :param seconds_time: 秒数
        :return:
        """
        m, s = divmod(seconds_time, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)
    
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
                
    # ffmpeg 工具封装：https://github.com/inlike/Python-FFmpeg-Video/blob/master/FFmpeg-Video.py
    # 视频批量处理 ：https://juejin.cn/post/7188423692354125879
    
    def handle_frame(self,image_frame):
        """
        处理图片帧
        :param image_frame:图片帧
        :return:
        """
        image_frame_result = image_frame * 1.2
        # 如果颜色值超过255，直接设置为255
        image_frame_result[image_frame_result > 255] = 255
        return image_frame_result
    
    def increase_video_brightness(self,orign_file_path,dest_file_path):
        """
        增加视频整体亮度
        :param orign_file_path:源视频路径
        :param dest_file_path:目标视频路径
        :return:
        """
        video = VideoFileClip(orign_file_path)
        result = video.fl_image(handle_frame)
        result.write_videofile(dest_file_path)
    
    
    def video_brightness_by_ratio(self,video_raw_clip,ratio):
        """
        增加视频整体亮度0-2，>1 提升亮度， <1 调低亮度
        :param orign_file_path:源视频路径
        :param dest_file_path:目标视频路径
        :return:
        """
        # 调整系数值
        coefficient_value = ratio
        clip = video_raw_clip.fx(vfx.colorx, coefficient_value)
        return clip
    
    def change_video_bhd(self,orign_file_path,dest_file_path):
        """
            黑白处理
        :param orign_file_path:源视频路径
        :param dest_file_path:目标视频路径
        :return:
        """
        video = VideoFileClip(orign_file_path)
        video.fx(vfx.blackwhite).write_videofile(dest_file_path)
    
    def video_with_text(self,synthetic_video_clip, desc_text_clip):
        """
        视频中加入文字信息
        :param synthetic_video_clip:
        :param param:
        :return:
        """
        video_with_text_clip = CompositeVideoClip([synthetic_video_clip, desc_text_clip.set_start(0)])
        # video_with_text_clip.write_videofile(
        #     './source/temp_video_with_text.mp4')
        
        return video_with_text_clip
    
    def get_frame_from_video(self,video_name, frame_time, img_path):
        """
        获取视频某个时间的帧图片，保存在本地
        :param video_name: 视频路径
        :param frame_time: 截取帧的时间位置(s)
        :param img_path:生成图片的完整路径
        :return:
        """
        # 秒转为时、分、秒
        time_pre = time_to_hms(frame_time)

        os.system('ffmpeg -ss %s -i %s -frames:v 1 %s' % (time_pre, video_name, img_path))

    def generate_text_clip(self,text_content, font_params, duration):
        """
        产生字幕
        :return:
        """
        # 显示位置
        position = font_params.get('position')
        position_text = 'top' if position == 0 else 'bottom'

        return TextClip(text_content, font='./fonts/STHeiti Medium.ttc',
                        fontsize=font_params.get('size'), kerning=font_params.get('kerning'),
                        color=font_params.get('color')).set_position(("center", 150)).set_duration(duration)

    def get_video_basic_info(self,video_path):
        """
        获取视频的基础信息
        1、获取视频编辑对象
        2、视频宽、高、帧率
        3、分离音频
        """
        video_raw_clip = VideoFileClip(video_path)
        #宽、高
        video_width,video_height = video_raw_clip.w,video_raw_clip.h
        #视频时长
        duration = video_raw_clip.duration
        #帧率
        fps = video_raw_clip.fps
        #分离出audio
        audio = video_raw_clip.audio.subclip(0,video_raw_clip.duration)
        
        return video_raw_clip,duration,video_width,video_height,fps,audio
        
    
    def video_crop_clip(self,video_raw_clip):
        """
        视频基础处理
        1、视频截取（抽取）
        2、分离音频
        3、修改md5
        """
        # 视频截取
        duration = video_raw_clip.duration
        video_raw_clip = video_raw_clip.subclip(1,duration-1)
        return video_raw_clip
        
    def video_resize_clip(self,video_clip,ratio):
        """
        # 视频尺寸缩放
        """
        return vfx.resize(video_clip,ratio)
    
    def video_crop_size_clip(self,video_clip):
        """
        视频尺寸进行裁剪
        """
        #宽、高
        video_width,video_height = video_clip.w,video_clip.h
        x1,y1,x2,y2 = video_width*0.1,video_height*0.1,video_width*0.9,video_height*0.95
        width, height = x2 - x1, y2 - y1
        cropped_video = video_clip.crop(x1=x1, y1=y1, x2=x2, y2=y2).resize((width, height))
        return cropped_video

        
    def video_add_random_transition(self,clip):
            """
            给视频增加特效
            """
            transitions = [
                lambda c:c.fadein(3),  # 淡入特效 持续3秒
                lambda c:c.fadeout(3), # 淡出特效 持续3秒
                lambda c:vfx.freeze(c,freeze_duration=2),  # 冻结特效 持续2秒
                lambda c:c.crossfadein(3), # #淡入淡出交叉 持续3秒
                # lambda c:vfx.invert_colors(c), # 色彩反转
                # lambda c:vfx.colorx(c,0.5),
                lambda c:vfx.speedx(c,1.3),
                # lambda c:vfx.rotate(c,3), # 旋转3度
                lambda c:vfx.painting(c,1.1), # 油画特效3秒
                # lambda c:vfx.loop(c,n=2),  # 循环1次
                # lambda c:vfx.time_symmetrize(c), #倒放
                # lambda c:clip[::-1] #倒放
            ]
            # fl_time(lambda t: self.duration - t - 1, keep_duration=True)
            transition_func = random.choice(transitions)
            return transition_func(clip)


    
    def video_add_end_transition(self,clip_origin):
        clip = clip_origin.\
            add_mask()
        # The mask is a circle with vanishing radius r(t) = 800-200*t               
        clip.mask.get_frame = lambda t: circle(screensize=(clip.w,clip.h),
                                            center=(clip.w/2,clip.h/2),
                                            radius=max(0,int((clip.duration+3)*100-100*t)),
                                            col1=1.0, col2=0, blur=4)


        # # Make the text. Many more options are available.
        txt_clip = (TextClip("The End",size=(500, 500), color="yellow", font='../font/STHeiti Medium.ttc',method='label')
                    .set_position('center')
                    .set_duration(clip_origin.duration+1))

        
        final_clip = CompositeVideoClip([txt_clip,clip],
                                size =clip.size)
        return final_clip
        
    
    def video_add_Video_Text(self,text_content,video_clip,postion):
        """
        给视频增加文本
        #https://blog.itblood.com/2297.html
        """
        # print(TextClip.list("font"))
        FONT_URL = 'apiproxy/font/HYBiRanTianTianQuanW-2.ttf'
        txt_clip = (TextClip(text_content,fontsize=100,font=FONT_URL,color='yellow',method='label')
                    .set_position(postion)
                    .set_duration(video_clip.duration))
        
        final_clip = CompositeVideoClip([video_clip,txt_clip])
        return final_clip
    
    def video_add_image(self,img_path,video_clip,postion):
        """
        增加图片loggo
        # https://blog.itblood.com/2295.html
        """
        logo = (ImageClip(img_path)
                # 水印持续时间
                .set_duration(video_clip.duration)
                # 水印高度，等比缩放
                .resize(height=300)
                # 水印的位置
                .set_position(postion)
                # 水印边距和透明度
                .margin(left=30, top=30,opacity=0))
        
        final_clip = CompositeVideoClip([video_clip,logo])
        return final_clip
    
    def vid_title_en_split(self,video_title):
        '''
        设置封面标题，每N个字符插入\n
        '''
        res = ""
        font_size = 40
        words = video_title.split()  # 将原始字符串分割成单词列表
        if len(words)>12:
            font_size=60
        elif len(words)>9:
            font_size = 80
        elif len(words)>5:
            font_size = 100
        else:
            font_size = 100
        # for i in range(0, len(words), n):
        #     res += " ".join(words[i:i+n]) + "\n"
        # # 去掉最后一个 N
        # res = res[:-2]
        video_title = video_title.replace(",","\n").replace("，","\n").replace(".","\n").replace("!","\n")
        print(video_title)
        return video_title,font_size
    
    def vid_title_cn_split(self,video_title,n):
        '''
        设置封面标题，每N个字符插入\n
        '''
        res = ""
        font_size = 40
        words = video_title.split()  # 将原始字符串分割成单词列表
        if len(words)>12:
            font_size=40
        elif len(words)>9:
            font_size = 60
        elif len(words)>5:
            font_size = 80
        else:
            font_size = 100
        res = ""
        for i in range(0, len(video_title), n):
            res += s[i:i+n] + "N"
        # 去掉最后一个 N
        res = res[:-2]
        print(res)
        return res,font_size


    def generate_mask_cover(self,video_clip,video_path,video_title,postion):
            """
            生成视频的封面
            """
            img_temp_dir = '/root/workspace/imgtemp'
            FONT_URL = 'apiproxy/font/HYBiRanTianTianQuanW-2.ttf'
            # video_clip = VideoFileClip(video_path)
            #视频时长
            duration = video_clip.duration
            cover_video_png = video_path[:-4]+'_new_cover.png'
            img_save_path = os.path.join(img_temp_dir,"frame.png")
            #保存第一帧
            video_clip.save_frame(img_save_path,random.randint(1,int(duration)-3))
            #设置封面标题
            #读取视频
            img_clip = ImageClip(img_save_path).set_duration(1)
            # 文字视频
            video_new_title,font_size = self.vid_title_en_split(video_title=video_title)
            print(video_new_title)
            text_clip = (TextClip(video_new_title,fontsize=font_size,font=FONT_URL,color='black',method='label')
                        .set_position(postion)
                        .set_duration(1))

            # 合成视频
            composite_video_clip = CompositeVideoClip([img_clip,text_clip],size =img_clip.size)
            composite_video_clip.save_frame(cover_video_png)
            # 导出视频
            # finalclip = concatenate_videoclips(composite_video_clip,video_clip)
            return composite_video_clip,cover_video_png
    
    
    def translate_zh_en_text(self,video_path):
        """
        将中文字幕换成英文字幕
        """
        
        pass
    

if __name__ == '__main__':
    root_dir = '/root/video_download/douyin'
    date_str = '2023-06-07'
    vd = VideoUtil()
    file_name = '/root/video_download/douyin/user_小透明/post/2021-01-19/2021-01-19 15.35.34_你说你冷我让你多穿点你说你以前冷时前女友/2021-01-19 15.35.34_你说你冷我让你多穿点你说你以前冷时前女友_video.mp4'
    file_name_new = '/root/video_download/douyin/user_小透明/post/2021-01-19/2021-01-19 15.35.34_你说你冷我让你多穿点你说你以前冷时前女友/你说你冷我让你多穿点你说你以前冷时前女友_new.mp4'
    title = 'You said you are cold, let me wear more, you said that you used to be cold, the ex -girlfriend when you were cold'
    # video_raw_clip,duration,video_width,video_height,fps,audio = vd.get_video_basic_info(file_name)
    # vd.generate_mask_cover(video_raw_clip,file_name,title,'center')

    #查看md5 是否重复
    origin_md5 = vd.get_video_md5(file_name)
    print(origin_md5)
    new_md5 = vd.get_video_md5(file_name_new)
    print(new_md5)

    # new_file_name = file_name[:-4]
    # print(new_file_name+"_transition.mp4")
    # video_title = 'I want to insert a letter N between every six English words in this sentence？'
    # text = vd.vid_title_split(video_title=video_title,n=4)
    # print(text)
    # douyin_video_list,bili_video_list,youtube_video_list= vd.findDateVideoFiles(date_str)
    #md5 修改
    # origin_md5 = vd.get_video_md5(file_name)
    # print(origin_md5)
    # vd.modify_file_md5(file_name)
    # new_md5 = vd.get_video_md5(file_name)
    # print(new_md5)

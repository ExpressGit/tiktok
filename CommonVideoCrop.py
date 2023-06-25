'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2023-06-22 20:45:56
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2023-06-24 21:03:53
FilePath: /tiktok/CommonVideoCrop.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#!/usr/bin/env python  
# encoding: utf-8 

import os
from apiproxy.common import FFmpegUtil
from apiproxy.common.VideoUtil import VideoUtil,VideoRead
from apiproxy.common import ImageUtil
from apiproxy.common import utils
from apiproxy.common.SubtitleUtil import *
from apiproxy.common import TranslateUtil
import shutil
import re

"""
通用视频处理类
"""
class CommonVideoCrop(object):

    def __init__(self) -> None:
        self.vd = VideoUtil()

    def get_video_info(self,video_path):
        '''
        获取视频的基础信息
        '''
        video_raw_clip,duration,video_width,video_height,fps,audio = self.vd.get_video_basic_info(video_path)
        return video_raw_clip,duration,video_width,video_height,fps,audio

    def write_title_file(self,title,file_path):
        '''
            写入标题文件（覆盖）
        '''
        with open(file_path, 'w') as writers: # 打开文件
            writers.write(title) 
        writers.close() 
        print(" title en 已写入文件 done")

    def remove_bili_logo(self,video_path):
        '''
        去除bili视频水印
        '''
        if not os.path.exists(video_path):
            print(" 视频文件不存在 ")
        dir_path = os.path.dirname(video_path)
        vdo_name = os.path.basename(video_path)
        video_raw_clip,duration,video_width,video_height,fps,audio = self.get_video_info(video_path=video_path)
        new_video_path = os.path.join(dir_path,vdo_name[:-4]+"_logo.mp4")
        ffmpegutil = FFmpegUtil.FFmpeg(video_path)
        if video_width>video_height:
            print("16:9 视频去掉logo")
            ffmpegutil.remove_169_bili_logo(video_width,video_height,new_video_path)
        else:
            print("4:5 视频 去掉 logo")
            ffmpegutil.remove_45_bili_logo(video_width,video_height,new_video_path)
        return new_video_path

    def adjust_video_crop(self,video_path,video_title):
        '''
        对视频进行基础处理
        # 1、视频截取
        # 2、增加视频转场特效
        # 3、调整视频亮度，可用系数调节
        # 4、视频尺寸缩放
        # 5、视频结束增加结束特效
        # 6、基于视频内容设置视频封面
        # 7、修改视频的meta信息
        '''
        if not os.path.exists(video_path):
            print(" 视频文件不存在 ")
            return 
        dir_path = os.path.dirname(video_path)
        final_save_dir_path = dir_path.replace("video_download","video_deliver")
        print(final_save_dir_path)
        vdo_name = os.path.basename(video_path)
        if not os.path.exists(final_save_dir_path):
            os.makedirs(final_save_dir_path)
        video_raw_clip,duration,video_width,video_height,fps,audio = self.get_video_info(video_path=video_path)
        # 1、视频截取
        video_raw_crop_clip=self.vd.video_crop_size_clip(video_raw_clip)
        print(" 视频截取 done")
        # 2、增加视频转场特效
        video_trans_clip = self.vd.video_add_random_transition(video_raw_crop_clip)
        print(" 增加视频转场特效 done")
        # 3、调整视频亮度
        video_bright_clip = self.vd.video_brightness_by_ratio(video_trans_clip,ratio=1.2)
        print(" 调整视频亮度 done")
        # 4、视频尺寸缩放
        video_size_clip = self.vd.video_resize_clip(video_bright_clip,ratio=0.9)
        print(" 视频尺寸缩放 done")
        # 5、增加结束特效
        video_end_clip = self.vd.video_add_end_transition(video_size_clip)
        print(" 增加结束特效 done")
        # 6、设置视频封面
        title_en = self.translate_text(video_title,'en')
        video_png_clip,cover_png_path = self.vd.generate_mask_cover(video_end_clip,video_path,video_title=title_en,postion=('top','center'))
        edit_video_path = os.path.join(dir_path,video_title+'_edit.mp4')
        video_end_clip.write_videofile(edit_video_path,fps=24)
        new_cover_png_path = cover_png_path.replace("video_download","video_deliver")
        #复制cover 封面
        shutil.copyfile(cover_png_path, new_cover_png_path)
        #生成标题文件
        title_file_path =  os.path.join(final_save_dir_path,video_title+'.txt')
        self.write_title_file(title_en+'\n'+video_title,title_file_path)
        print(" 设置视频封面 done")
        # 7、修改视频的meta信息
        new_video_path = os.path.join(final_save_dir_path,video_title+'_new.mp4')
        ffmpegutil = FFmpegUtil.FFmpeg(edit_video_path)
        ffmpegutil.edit_metadata(new_video_path)
        print(" 修改视频的meta信息 done")
        
        print("{} video deal process done!!".format(video_title))

    def clear_video(self,origin_video_path):
        '''
        中间过程产出的视频清理
        清理多余视频文件，节省空间
        '''
        dir_path = os.path.dirname(origin_video_path)
        for file_path, empty_list, file_name_list in os.walk(dir_path):
            for file_name in file_name_list:
                if re.search('.*?[logo|edit|new|en].mp4',file_name):
                    print("delete " + file_name)
                    file = os.path.join(file_path,file_name)
                    if os.path.exists(file):
                        os.remove(file)
        print(" 冗余 视频 删除 完成 done")

    def add_video_subtitle(self,video_path,srt_file):
        '''
        给视频添加字幕
        '''
        if not os.path.exists(video_path):
            print(" 视频文件不存在 ")
            return
        dir_path = os.path.dirname(video_path)
        video_name = os.path.basename(video_path)
        srt_en_file = os.path.join(dir_path,video_name[:-9]+'_en.srt')
        output_video_file = os.path.join(dir_path,video_name[:-9]+'_en.mp4')
        #构建字幕文件
        segments = file_to_subtitles(srt_file)
        segments_en = ch_translate_to_en(segments)
        create_srt_file(segments_en,srt_en_file)
        #给视频添加字幕
        add_subtitle_in_video(video_path,srt_en_file,output_video_file)
        print(" 视频 添加 英文 字幕 done")
        return output_video_file

    def translate_text(self,text,lang):
        '''
        description:  实现文本翻译能力
        param {*} text
        param {*} lang
        return {*}
        '''
        trans_text = TranslateUtil.translate_text(text,lang)
        return trans_text
    
if __name__ == '__main__':
    file_name = '/root/video_download/bili/雪柔睡不醒/2023-06-22/沉浸式体验小仓鼠女友30秒洗头.mp4'
    title = '沉浸式体验小仓鼠女友30秒洗头'
    commonutil = CommonVideoCrop()
    # commonutil.adjust_video_crop(file_name,title)
    # commonutil.remove_bili_logo(file_name)
    
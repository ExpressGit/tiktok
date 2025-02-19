'''
Author: lelexu
Date: 2023-06-22 21:45:13
LastEditTime: 2023-07-12 08:59:44
FilePath: /tiktok/DouYinVideoCrop.py
Description: 
'''
#!/usr/bin/env python  
# encoding: utf-8 


from apiproxy.common.VideoUtil import VideoUtil,VideoRead
from CommonVideoCrop import CommonVideoCrop
import datetime,os,sys
from tqdm import tqdm
import shutil

class YoutubeVideoCrop(object):


    def __init__(self) -> None:
        self.base_dir = '/root/video_download'
        self.vd_read = VideoRead(self.base_dir)

    def get_all_video_list(self,date_str=None):

        Youtube_video_list = []
        youtube_srt_list = []
        if date_str == None:
            date_str = datetime.date.today() + datetime.timedelta(-1)
            print(date_str)
        _,_,Youtube_video_list,_ = self.vd_read.findDateVideoFiles(date_str)
        # 读取字幕文件
        _,_,Youtube_files_list,_ = self.vd_read.findDateFiles(date_str)
        # 读取logo postion文件
        link_logo_youtube_dict = self.vd_read.getVideoLogoPostion(config_name='youtube')
        # 将uid 和 video_path 结合，组装dict
        video_logo_dict = {}
        for uid,logpos in link_logo_youtube_dict.items():
            for video_file in Youtube_video_list:
                if uid in video_file:
                    video_logo_dict[video_file] = logpos
                    continue
        print(video_logo_dict)
        # 提取字幕文件
        for file in Youtube_files_list:
            if file.endswith('.srt'):
                youtube_srt_list.append(file)
        return Youtube_video_list,youtube_srt_list,video_logo_dict
    
    def remove_Youtube_logo(self,video_list,logo_dict):
        '''
        去除bili视频的水印
        '''
        video_new_list = []
        if video_list==None or len(video_list)==0:
            print("视频列表为空，无需处理 remove_Youtube_logo~~~")
            return 
        video_util = CommonVideoCrop()
        for video_file,logpos in tqdm(logo_dict.items()):
            new_video_file = video_util.remove_bili_logo(video_file,logpos)
            video_new_list.append(new_video_file)
        print("youtube 视频水印 已清理")
        return video_new_list

    def deal_videos_list(self,video_list):
        '''
        针对bili视频列表进行处理
        '''
        if video_list==None or len(video_list)==0:
            print("视频列表为空，无需处理 deal_videos_list~~~")
            return 
        video_util = CommonVideoCrop()
        for video_file in tqdm(video_list):
            vdo_name = os.path.basename(video_file)
            video_titles = vdo_name.split("_")
            video_title = video_titles[0]
            print(video_title)
            video_util.adjust_video_crop(video_file,video_title)
        print("本次 youtube视频 均已处理完成~~~~")
        # 清理冗余视频
        for video_file in tqdm(video_list):
            video_util.clear_video(video_file)

    def add_video_srt(self,video_list,srt_list):
        '''
        帮助视频添加字幕
        '''
        if video_list==None or len(video_list)==0 or len(srt_list)==0:
            print("视频列表为空，无需处理 add_video_srt~~~")
            return video_list
        # 构建视频，字幕的匹配关系
        video_util = CommonVideoCrop()
        video_to_srt_list = []
        new_video_list = []
        for video_file in video_list:
            base_name = os.path.basename(video_file)[:-9]
            for srt in srt_list:
                dir_name = os.path.dirname(srt)
                srt_basename = os.path.basename(srt)[:-4]
                # 针对一个视频存在多个srt文件
                if base_name in srt_basename and '中文' in srt_basename:
                    video_to_srt_list.append([video_file,srt])
        for video_file,srt in video_to_srt_list:
            new_video_path = video_util.add_video_subtitle(video_file,srt)
            new_video_list.append(new_video_path)
        return new_video_list
        

    def add_video_en_subtitle(self,video_list):
        '''
        video add english subtitle
        '''
        if len(video_list) == 0:
            print("视频列表为空，无需处理 add_video_en_subtitle~~~")
            return
        video_util = CommonVideoCrop()
        video_audio_list = self.vd_read.getVideoAudioReg(config_name='youtube')
        ret_video_list = []
        for video_file in video_list:
            add_flag =  True # 是否已经语音处理
            for video_keyword,flag in tqdm(video_audio_list.items()):
                if video_keyword in video_file and flag:
                    video_new_file = video_util.add_video_en_subtitle(video_file=video_file)
                    if len(video_new_file)>1:
                        ret_video_list.append(video_new_file)
                        add_flag = False
                        continue
            if add_flag:
                ret_video_list.append(video_file)
        print("~~~~~~~~~~video add english subtitle success~~~~~~~~")
        return ret_video_list
    

if __name__ == '__main__':
    if None == sys.argv[1]:
        date_str =  datetime.date.today() + datetime.timedelta(-1)
    else:
        date_str = sys.argv[1]
    print(" 本次 youtube 视频 处理 日期:%s" % date_str)
    
    # date_str = '2023-06-30'
    
    youtube_crop = YoutubeVideoCrop()
    video_list,srt_list,video_logo_dict = youtube_crop.get_all_video_list(date_str)
    new_video_list = youtube_crop.remove_Youtube_logo(video_list,video_logo_dict)
    print(new_video_list)
    en_video_list = youtube_crop.add_video_en_subtitle(new_video_list)
    # new_en_video_list = youtube_crop.add_video_srt(new_video_list,srt_list)
    youtube_crop.deal_videos_list(en_video_list)
    
    #清理冗余视频 en logo new edit 视频&srt文件
    common = CommonVideoCrop()
    common.clear_video('/root/video_download/youtube')

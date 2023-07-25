'''
Author: lelexu
Date: 2023-06-22 21:45:13
LastEditTime: 2023-06-23 21:11:45
FilePath: /tiktok/DouYinVideoCrop.py
Description: 
'''
#!/usr/bin/env python  
# encoding: utf-8 


from apiproxy.common.VideoUtil import VideoUtil,VideoRead
from CommonVideoCrop import CommonVideoCrop
import datetime,os,sys
from tqdm import tqdm

class DouYinVideoCrop(object):


    def __init__(self) -> None:
        self.base_dir = '/root/video_download'
        self.vd_read = VideoRead(self.base_dir)

    def get_all_video_list(self,date_str=None):

        douyu_video_list = []
        if date_str == None:
            date_str = datetime.date.today() + datetime.timedelta(-1)
            print(date_str)
        douyu_video_list,_,_,_ = self.vd_read.findDateVideoFiles(date_str)

        return douyu_video_list
    
    def deal_videos_list(self,video_list):
        '''
        针对抖音视频列表进行处理
        '''
        if len(video_list)==0:
            print("视频列表为空，无需处理~~~")
            return 
        video_util = CommonVideoCrop()
        for video_file in tqdm(video_list):
            vdo_name = os.path.basename(video_file)
            video_titles = vdo_name.split("_")
            video_title = video_titles[1]
            print(video_title)
            video_util.adjust_video_crop(video_file,video_title)
            video_util.clear_video(video_file)
        print("本次 抖音视频 均已处理完成~~~~")
        # 清理冗余视频
        # for video_file in tqdm(video_list):
        #     video_util.clear_video(video_file)

    def add_video_en_subtitle(self,video_list):
        '''
        video add english subtitle
        '''
        if len(video_list) == 0:
            print("视频列表为空，无需处理 add_video_en_subtitle~~~")
            return
        video_util = CommonVideoCrop()
        video_audio_list = self.vd_read.getVideoAudioReg(config_name='douyin')
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
    print(" 本次 抖音 视频 处理 日期:%s" % date_str)
    douyin_crop = DouYinVideoCrop()
    # date_str = '2023-06-11'
    video_list = douyin_crop.get_all_video_list(date_str)
    en_video_list = douyin_crop.add_video_en_subtitle(video_list)
    douyin_crop.deal_videos_list(en_video_list)
    
    #清理冗余视频 en logo new edit 视频&srt文件
    common = CommonVideoCrop()
    common.clear_video('/root/video_download/douyin')
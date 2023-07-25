#!/bin/bash
###
 # @Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 # @Date: ${endday} 12:40:21
 # @LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 # @LastEditTime: 2023-07-13 21:48:49
 # @FilePath: /tiktok/download_corp_video.sh
 # @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
### 

# 执行命令：nohup bash /root/workspace/tiktok/download_corp_video.sh 1 > /root/workspace/logs/video-$(date +"%Y-%m-%d").log 2>&1 &

workspace_dir=/root/workspace/tiktok

cd ${workspace_dir}

pwd
# date
beginday=`date -d 'yesterday' '+%Y-%m-%d'`
endday=`date '+%Y-%m-%d'`
echo ${beginday}
echo ${endday}

# #douyin
# echo "=====================================DouYinCommand donwload video begin====================================="
# python3 DouYinCommand.py -C False --config douyin 
# if [ $? -eq 0 ]; then
#     echo ${endday}" douyin download video success "
# else
#     echo ${endday}" douyin download video failed "
#     exit 1
# fi
# echo "=====================================DouYinCommand donwload video end====================================="

# # video 流水线处理
# echo "=====================================DouYinVideoCrop crop video begin====================================="
# python3 DouYinVideoCrop.py ${beginday}
# if [ $? -eq 0 ]; then
#     echo ${endday}" douyin corp video success "
# else
#     echo ${endday}" douyin corp video failed "
#     exit 1
# fi
# echo "=====================================DouYinVideoCrop crop video end====================================="


# #youtube
# echo "=====================================YoutubeCommand donwload video begin====================================="
# python3 YotuberCommand.py -C False --config youtube 

# if [ $? -eq 0 ]; then
#     echo ${endday}" youtube download video success "
# else
#     echo ${endday}" youtube download video failed "
#     exit 1
# fi
# echo "=====================================YoutubeCommand donwload video end====================================="

# # video 流水线处理
# echo "=====================================YotuberVideoCrop crop video begin====================================="
# python3 YotuberVideoCrop.py ${beginday}
# if [ $? -eq 0 ]; then
#     echo ${endday}" youtube corp video success "
# else
#     echo ${endday}" youtube corp video failed "
#     exit 1
# fi
# echo "=====================================YotuberVideoCrop crop video end====================================="


#bili
echo "=====================================BiliCommand donwload video begin====================================="
python3 BiliCommand.py -C False --config bili 
if [ $? -eq 0 ]; then
    echo ${endday} " bili download video success "
else
    echo ${endday} " bili download video failed "
    exit 1
fi
echo "=====================================BiliCommand donwload video end====================================="

# video 流水线处理
echo "=====================================BiliVideoCrop crop video begin====================================="
python3 BiliVideoCrop.py ${beginday}
if [ $? -eq 0 ]; then
    echo ${endday} " bili corp video success "
else
    echo ${endday} " bili corp video failed "
    exit 1
fi
echo "=====================================BiliVideoCrop crop video end====================================="

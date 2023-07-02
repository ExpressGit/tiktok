#!/bin/bash
###
 # @Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 # @Date: ${endday} 12:40:21
 # @LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 # @LastEditTime: 2023-07-02 17:08:10
 # @FilePath: /tiktok/download_corp_video.sh
 # @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
### 

workspace_dir=/root/workspace/tiktok

cd ${workspace_dir}

pwd
# date
beginday=`date -d 'yesterday' '+%Y-%m-%d'`
endday=`date '+%Y-%m-%d'`
echo ${beginday}
echo ${endday}

# douyin
python3 DouYinCommand.py -C False --config beauty 
if [ $? -eq 0 ]; then
    echo ${endday}" douyin download video success "
else
    echo ${endday}" douyin download video failed "
    exit 1
fi
# video 流水线处理
python3 DouYinVideoCrop.py ${beginday}
if [ $? -eq 0 ]; then
    echo ${endday}" douyin corp video success "
else
    echo ${endday}" douyin corp video failed "
    exit 1
fi


#bili
python3 BiliCommand.py -C False --config bili 
if [ $? -eq 0 ]; then
    echo ${endday}" bili download video success "
else
    echo ${endday}" bili download video failed "
    exit 1
fi

# video 流水线处理
python3 BiliVideoCrop.py ${beginday}
if [ $? -eq 0 ]; then
    echo ${endday}" bili corp video success "
else
    echo ${endday}" bili corp video failed "
    exit 1
fi


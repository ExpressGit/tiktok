#!/bin/bash
###
 # @Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 # @Date: 2023-06-25 12:40:21
 # @LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 # @LastEditTime: 2023-06-25 12:49:44
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

# # douyin
# python3 DouYinCommand.py -C False --config beauty >> "/$(date +%Y-%m-%d).log" 2>&1
# if [ $? -eq 0 ]; then
#     echo ${endday}" douyin download video success "
# else
#     echo ${endday}" douyin download video failed "
# fi
# # video 流水线处理
# python3 DouYinVideoCrop.py ${beginday}
# if [ $? -eq 0 ]; then
#     echo ${endday}" douyin corp video success "
# else
#     echo ${endday}" douyin corp video failed "
# fi


# # bili
# yutto --batch https://space.bilibili.com/1480975816 -n 1 -q 120 --output-format mp4 -d /root/video_download/bili -c 25ae6104%2C1703209865%2Ceff30%2A61T12ccqWBkcccaWqYaWMTRi5uWeD-TYCas46A5sbfdsgQsZVe02TUjmrheRO_kAjLL22EbQAAKQA --no-danmaku -tp {username}/{pubdate}/{name} --batch-filter-start-time 2023-06-24 --batch-filter-end-time 2023-06-25
yutto --batch https://space.bilibili.com/21060026 -n 1 -q 120 --output-format mp4 -d /root/video_download/bili -c 25ae6104%2C1703209865%2Ceff30%2A61T12ccqWBkcccaWqYaWMTRi5uWeD-TYCas46A5sbfdsgQsZVe02TUjmrheRO_kAjLL22EbQAAKQA --no-danmaku -tp {username}/{pubdate}/{name} --batch-filter-start-time 2023-06-24 --batch-filter-end-time 2023-06-25
if [ $? -eq 0 ]; then
    echo ${endday}" up id: 1480975816 bili download video success "
else
    echo ${endday}" up id: 1480975816 bili download video failed "
fi
sleep 19m
yutto --batch https://space.bilibili.com/3494358099692362 -n 1 -q 120 --output-format mp4 -d /root/video_download/bili -c 25ae6104%2C1703209865%2Ceff30%2A61T12ccqWBkcccaWqYaWMTRi5uWeD-TYCas46A5sbfdsgQsZVe02TUjmrheRO_kAjLL22EbQAAKQA --no-danmaku -tp {username}/{pubdate}/{name} --batch-filter-start-time ${beginday} --batch-filter-end-time ${endday}
if [ $? -eq 0 ]; then
    echo ${endday}" up id: 3494358099692362 bili download video success "
else
    echo ${endday}" up id: 3494358099692362 bili download video failed "
fi
sleep 19m
yutto --batch https://space.bilibili.com/500525892 -n 1 -q 120 --output-format mp4 -d /root/video_download/bili -c 25ae6104%2C1703209865%2Ceff30%2A61T12ccqWBkcccaWqYaWMTRi5uWeD-TYCas46A5sbfdsgQsZVe02TUjmrheRO_kAjLL22EbQAAKQA --no-danmaku -tp {username}/{pubdate}/{name} --batch-filter-start-time ${beginday} --batch-filter-end-time ${endday}
if [ $? -eq 0 ]; then
    echo ${endday}" up id: 500525892 bili download video success "
else
    echo ${endday}" up id: 500525892 bili download video failed "
fi

# video 流水线处理
python3 BiliVideoCrop.py ${beginday}
if [ $? -eq 0 ]; then
    echo ${endday}" bili corp video success "
else
    echo ${endday}" bili corp video failed "
fi


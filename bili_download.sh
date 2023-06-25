#!/bin/bash
###
 # @Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 # @Date: 2023-06-25 12:40:21
 # @LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 # @LastEditTime: 2023-06-25 19:03:57
 # @FilePath: /tiktok/download_corp_video.sh
 # @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
### 

# # bili
yutto --batch https://space.bilibili.com/21060026 -n 1 -q 120 --output-format mp4 -d /root/video_download/bili -c 25ae6104%2C1703209865%2Ceff30%2A61T12ccqWBkcccaWqYaWMTRi5uWeD-TYCas46A5sbfdsgQsZVe02TUjmrheRO_kAjLL22EbQAAKQA --no-danmaku -tp {username}/{pubdate}/{name} --batch-filter-start-time 2023-06-24 --batch-filter-end-time 2023-06-25


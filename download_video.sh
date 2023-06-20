#!/bin/bash
video_dir=/root/video_download/douyin
# modify md5


# douyin
python3 DouYinCommand.py -C False --config beauty >> "/$(date +%Y-%m-%d).log" 2>&1

# bili
yutto --batch https://space.bilibili.com/651386960/video -n 1 -q 120 --output-format mp4 -d /root/video_download/bili -c 37583ff3%2C1700489464%2C32014%2A51 --no-danmaku --no-subtitle -tp {username}/{pubdate}/{name} --batch-filter-start-time 2023-05-01 --batch-filter-end-time 2023-06-01
sleep 19m


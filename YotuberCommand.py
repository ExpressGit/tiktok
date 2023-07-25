#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@FileName   : BiliCommand.py
@Project    : apiproxy
@Description: 
@Author     : imgyh
@Mail       : admin@imgyh.com
@Github     : https://github.com/imgyh
@Site       : https://www.imgyh.com
@Date       : 2023/5/12 16:01
@Version    : v1.0
@ChangeLog 
------------------------------------------------

------------------------------------------------
'''

import argparse
import os
import sys,datetime
import json
import yaml,tqdm
import time

from apiproxy.common import utils
import subprocess
from apiproxy.common.YoutuberVideo import YoutuberVideo

configModel = {
    "link": [],
    "logops":[],
    "num_works": 1,
    "config_name":"youtube",
    "subpath_template":"{username}\/{pubdate}\/{name}",
    "path": "/root/video_download/youtube",
    "output-format":"mp4",
    "begin":None,
    "temp_dir":"/root/video_download/temp_video",
}


def argument():
    parser = argparse.ArgumentParser(description='B站批量下载工具 使用帮助')
    parser.add_argument("--cmd", "-C", help="使用命令行(True)或者配置文件(False), 默认为False",
                        type=utils.str2bool, required=False, default=False)
    parser.add_argument("--config_name", "-config",
                        help="配置文件名称",
                        type=str, required=False, default="youtube")
    parser.add_argument("--link", "-l",
                        help="个人主页的分享链接或者电脑浏览器网址, 可以设置多个链接(删除文案, 保证只有URL, https://space.bilibili.com/100969474 或者 https://www.douyin.com/开头的)",
                        type=str, required=False, default=[], action="append")
    parser.add_argument("--logops", "-pos",
                        help="视频logo位置：rightbottom,righttop,lefttop,leftbottom",
                        type=str, required=False, default=[], action="append")
    parser.add_argument("--begin",  help="开始时间",
                        type=str, required=False, default=None)
    parser.add_argument("--num_works", "-n", help="下载执行线程",
                        type=int, required=False, default=1)
    parser.add_argument("--output_format", "-of", help="指定下载视频文件格式",
                        type=str, required=False, default="mp4")
    parser.add_argument("--subpath_template", "-tp", help="文件保存风格, 默认为True",
                        type=str, required=False, default="")
    parser.add_argument("--path", "-p", help="视频下载根目录",
                        type=str, required=False, default="/root/video_download/youtube")
    parser.add_argument("--temp_dir", "-temp", help="视频下载临时目录",
                        type=str, required=False, default="/root/video_download/temp_dir")

    args = parser.parse_args()

    return args


def yamlConfig(config_name):
    curPath = os.path.dirname(os.path.realpath(sys.argv[0]))
    yamlPath = os.path.join(curPath,'config',config_name+"_config.yml")
    print(yamlPath)
    f = open(yamlPath, 'r', encoding='utf-8')
    cfg = f.read()
    configDict = yaml.load(stream=cfg, Loader=yaml.FullLoader)

    try:
        if configDict["link"] != None:
            configModel["link"] = configDict["link"]
    except Exception as e:
        print("[  警告  ]:link未设置, 程序退出...\r\n")
    try:
        if configDict["logops"] != None:
            configModel["logops"] = configDict["logops"]
    except Exception as e:
        print("[  警告  ]:logops未设置, 程序退出...\r\n")
    try:
        if configDict["path"] != None:
            configModel["path"] = configDict["path"]
    except Exception as e:
        print("[  警告  ]:path未设置, 使用当前路径...\r\n")
    try:
        if configDict["num_works"] != None:
            configModel["num_works"] = configDict["num_works"]
    except Exception as e:
        print("[  警告  ]:num_works, 使用默认值1...\r\n")
    try:
        if configDict["output_format"] != None:
            configModel["output_format"] = configDict["output_format"]
    except Exception as e:
        print("[  警告  ]:output_format, 使用默认值mp4...\r\n")
    try:
        if configDict["subpath_template"] != None:
            configModel["subpath_template"] = configDict["subpath_template"]
    except Exception as e:
        print("[  警告  ]:subpath_template, 使用默认值...\r\n")
    try:
        if configDict["temp_dir"] != None:
            configModel["temp_dir"] = configDict["temp_dir"]
    except Exception as e:
        print("[  警告  ]:temp_dir, 使用默认值...\r\n")
   

def main():
    start = time.time()  # 开始时间

    args = argument()

    if args.cmd:
        configModel["link"] = args.link
        configModel["path"] = args.path
        configModel["logops"] = args.logops
        configModel["num_works"] = args.num_works
        configModel["subpath_template"] = args.subpath_template
        configModel["output_format"] = args.output_format
        configModel["temp_dir"] = args.temp_dir

    else:
        yamlConfig(args.config_name)

    if configModel["link"] == []:
        return
    
    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d')
    delta = datetime.timedelta(days=-1)
    yestoday = now + delta
    yestoday_str = yestoday.strftime('%Y%m%d')

    if configModel['begin'] == None:
        configModel['begin'] = yestoday_str


    configModel["path"] = os.path.abspath(configModel["path"])
    print("[  提示  ]:数据保存路径 " + configModel["path"])
    if not os.path.exists(configModel["path"]):
        os.mkdir(configModel["path"])

    num_len = len(configModel["link"])
    
    youtubevideo = YoutuberVideo()
    
    # configModel["begin"]='20230717'
    
    for i in tqdm.tqdm(range(0, num_len)):
        print("--------------------------------------------------------------------------------")
        link = configModel["link"][i]
        print("[  提示  ]:正在YouTube请求的链接: " + link + "\r\n")
        result = youtubevideo.download_from_youtube_up_space(configModel['output_format'],configModel['num_works'],link,configModel["begin"])
        if result :
            print("link 链接download success ~~~",link)
        # 每次下载一个 暂定 10s
        time.sleep(3)    
    end = time.time()  # 结束时间
    print('\n' + '[下载完成]:总耗时: %d分钟%d秒\n' % (int((end - start) / 60), ((end - start) % 60)))  # 输出下载用时时间


if __name__ == "__main__":
    main()

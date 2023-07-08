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

configModel = {
    "link": [],
    "logops":[],
    "sleep": 10,
    "num_works": 1,
    "video_quality": 120,
    "cookie": None,
    "cookie2": None,
    "cookie3": None,
    "danmaku": False,
    "config_name":"bili",
    "subpath_template":"{username}\/{pubdate}\/{name}",
    "path": "/root/video_download/bili",
    "output-format":"mp4",
    "begin":None,
    "end":None,
}


def argument():
    parser = argparse.ArgumentParser(description='B站批量下载工具 使用帮助')
    parser.add_argument("--cmd", "-C", help="使用命令行(True)或者配置文件(False), 默认为False",
                        type=utils.str2bool, required=False, default=False)
    parser.add_argument("--config_name", "-config",
                        help="配置文件名称",
                        type=str, required=False, default="bili")
    parser.add_argument("--link", "-l",
                        help="个人主页的分享链接或者电脑浏览器网址, 可以设置多个链接(删除文案, 保证只有URL, https://space.bilibili.com/100969474 或者 https://www.douyin.com/开头的)",
                        type=str, required=False, default=[], action="append")
    parser.add_argument("--logops", "-pos",
                        help="视频logo位置：rightbottom,righttop,lefttop,leftbottom",
                        type=str, required=False, default=[], action="append")
    parser.add_argument("--sleep", "-sl", help="休眠时间",
                        type=int, required=False, default=10)
    parser.add_argument("--begin",  help="开始时间",
                        type=str, required=False, default=None)
    parser.add_argument("--end",  help="结束时间",
                        type=str, required=False, default=None)
    parser.add_argument("--num_works", "-n", help="下载执行线程",
                        type=int, required=False, default=1)
    parser.add_argument("--video_quality", "-q", help="指定下载视频清晰度",
                        type=int, required=False, default=120)
    parser.add_argument("--danmaku", "-d", help="是否下载视频的弹幕(True/False)",
                        type=utils.str2bool, required=False, default=False)
    parser.add_argument("--output_format", "-of", help="指定下载视频文件格式",
                        type=str, required=False, default="mp4")
    parser.add_argument("--subpath_template", "-tp", help="文件保存风格, 默认为True",
                        type=str, required=False, default="")
    parser.add_argument("--path", "-p", help="视频下载根目录",
                        type=str, required=False, default="/root/video_download/bili")
    parser.add_argument("--cookie", "-c",help="设置cookie, 格式: \"name1=value1; name2=value2;\" 注意要加冒号",
                        type=str, required=False, default='')
    args = parser.parse_args()

    return args


def yamlConfig(config_name):
    curPath = os.path.dirname(os.path.realpath(sys.argv[0]))
    yamlPath = os.path.join(curPath, config_name+"_config.yml")
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
        if configDict["sleep"] != None:
            configModel["sleep"] = configDict["sleep"]
    except Exception as e:
        print("[  警告  ]:sleep未设置, 使用默认值10...\r\n")
    try:
        if configDict["num_works"] != None:
            configModel["num_works"] = configDict["num_works"]
    except Exception as e:
        print("[  警告  ]:num_works, 使用默认值1...\r\n")
    try:
        if configDict["video_quality"] != None:
            configModel["video_quality"] = configDict["video_quality"]
    except Exception as e:
        print("[  警告  ]:video_quality, 使用默认值120...\r\n")
    try:
        if configDict["danmaku"] != None:
            configModel["danmaku"] = configDict["danmaku"]
    except Exception as e:
        print("[  警告  ]:danmaku, 使用默认值False...\r\n")
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
        if configDict["cookie"] != None:
            configModel["cookie"] = configDict["cookie"]
    except Exception as e:
        print("[  警告  ]:cookie未设置, 使用默认值5...\r\n")
    try:
        if configDict["cookie2"] != None:
            configModel["cookie2"] = configDict["cookie2"]
    except Exception as e:
        print("[  警告  ]:cookie2未设置, 使用默认值5...\r\n")
    try:
        if configDict["cookie3"] != None:
            configModel["cookie3"] = configDict["cookie3"]
    except Exception as e:
        print("[  警告  ]:cookie3未设置, 使用默认值5...\r\n")
   
def build_bili_download_command(link,path,n,q,output_format,tp,cookie,danmuku,beginday,endday):
        #yutto --batch https://space.bilibili.com/314480501 -n 1 -q 120 --output-format mp4 -d /root/video_download/bili -c 25ae6104%2C1703209865%2Ceff30%2A61T12ccqWBkcccaWqYaWMTRi5uWeD-TYCas46A5sbfdsgQsZVe02TUjmrheRO_kAjLL22EbQAAKQA --no-danmaku -tp {username}_{owner_uid}/{pubdate}/{name} --batch-filter-start-time 2023-06-21 --batch-filter-end-time 2023-06-28
        """
        添加视频字幕
        :param deposit:添加字幕后另存为路径，为空则覆盖
        :return: True/False
        """
        
        strcmd = r'yutto --batch "{}" -n {} -q {} --output-format "{}" '\
                 r' -d "{}" -c "{}" --no-danmaku -tp "{}" '\
                 r' --batch-filter-start-time "{}" --batch-filter-end-time "{}"'.format(
                    link, n,q,output_format,path,cookie,tp.replace("\\",""),beginday,endday)
        print(strcmd)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        if not result:
            print("link downlaod video failed:",link)
        return True

def main():
    start = time.time()  # 开始时间

    args = argument()

    if args.cmd:
        configModel["link"] = args.link
        configModel["path"] = args.path
        configModel["logops"] = args.logops
        configModel["sleep"] = args.sleep
        configModel["num_works"] = args.num_works
        configModel["video_quality"] = args.video_quality
        configModel["cookie"] = args.cookie
        configModel["danmaku"] = args.danmaku
        configModel["subpath_template"] = args.subpath_template
        configModel["output_format"] = args.output_format
        configModel["begin"] = args.begin
        configModel["end"] = args.end
    else:
        yamlConfig(args.config_name)

    if configModel["link"] == []:
        return
    
    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d')
    delta = datetime.timedelta(days=-1)
    yestoday = now + delta
    yestoday_str = yestoday.strftime('%Y-%m-%d')

    if configModel['begin'] == None:
        configModel['begin'] = yestoday_str
    if configModel['end'] == None:
        configModel['end'] = now_str

    configModel["path"] = os.path.abspath(configModel["path"])
    print("[  提示  ]:数据保存路径 " + configModel["path"])
    if not os.path.exists(configModel["path"]):
        os.mkdir(configModel["path"])

    num_len = len(configModel["link"])
    
    for i in tqdm.tqdm(range(0, num_len, 3)):
        print("--------------------------------------------------------------------------------")
        link1 = configModel["link"][i]
        print("[  提示  ]:正在BILI请求的链接: " + link1 + "\r\n")
        if i+1 <= (num_len - 1 ):
            link2 = configModel["link"][i+1]
            time.sleep(10)
            result = build_bili_download_command(link2,configModel["path"], configModel["num_works"],configModel["video_quality"],
                                    configModel["output_format"],configModel["subpath_template"],configModel["cookie2"],configModel["danmaku"],
                                    configModel['begin'],configModel['end'])
        if i+2 <= (num_len - 1):
            link3 = configModel["link"][i+2]
            time.sleep(10)
            result = build_bili_download_command(link3,configModel["path"], configModel["num_works"],configModel["video_quality"],
                                    configModel["output_format"],configModel["subpath_template"],configModel["cookie3"],configModel["danmaku"],
                                    configModel['begin'],configModel['end'])
        if result :
            print("link 链接download success ~~~",link1)
        # 每次下载一个 暂定 12min
        time.sleep(int(configModel["sleep"])*60)    
    end = time.time()  # 结束时间
    print('\n' + '[下载完成]:总耗时: %d分钟%d秒\n' % (int((end - start) / 60), ((end - start) % 60)))  # 输出下载用时时间


if __name__ == "__main__":
    main()

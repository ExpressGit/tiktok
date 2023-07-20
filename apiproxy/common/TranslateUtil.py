'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2023-06-22 13:56:18
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2023-07-15 20:36:07
FilePath: /tiktok/apiproxy/common/TranslateUtil.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#!/usr/bin/env python  
# encoding: utf-8  


# import tkinter.messagebox  
# from tkinter import *

from PIL import Image
from translatepy.translators.google import GoogleTranslate
import os
import time

def translate_text(content,lang):
    translator = GoogleTranslate()
    print(content)
    res = translator.translate(content,lang)
    # res = translator.translate('안녕하세요.',dest='en')
    print(res.result)
    return res.result

if __name__ == '__main__':
    images = ['/root/video_download/douyin/user_00后的窝/post/2023-01-07/2023-01-07 17.21.40_感谢喜欢你们要的一镜到底来啦你们是喜欢我/2023-01-07 17.21.40_感谢喜欢你们要的一镜到底来啦你们是喜欢我_cover.jpeg']
    # judge_zimu_exist(images)
    content='안녕하세요.'
    lang='en'
    translate_text(content,lang)
'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2023-06-22 13:56:18
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2023-07-08 16:11:38
FilePath: /tiktok/apiproxy/common/TranslateUtil.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#!/usr/bin/env python  
# encoding: utf-8  


# import tkinter.messagebox  
# from tkinter import *

import pytesseract
from PIL import Image
from googletrans import Translator
import os

def judge_zimu_exist(image_list):
    """
    判断图片中是否有字母
    """
    img_temp = '/root/workspace/imgtemp'
    new_img = []
    for img_pth in image_list:
        img = Image.open(img_pth)
        w,h = img.size
        box = (0,h/2,w,h)
        print(img.size)
        region = img.crop(box)
        img_path = os.path.join(img_temp,'crop.jpg')
        new_img.append(img_path)
        region.save(img_path)
    # 识别 是否有字幕
    for image_path in new_img:
        text = pytesseract.image_to_string(Image.open(image_path), lang='eng')
        print(text)

def translate_text(content,lang):
    translator = Translator()
    print(content)
    res = translator.translate(content,dest=lang)
    # res = translator.translate('안녕하세요.',dest='en')
    print(res.text)
    return res.text

if __name__ == '__main__':
    images = ['/root/video_download/douyin/user_00后的窝/post/2023-01-07/2023-01-07 17.21.40_感谢喜欢你们要的一镜到底来啦你们是喜欢我/2023-01-07 17.21.40_感谢喜欢你们要的一镜到底来啦你们是喜欢我_cover.jpeg']
    # judge_zimu_exist(images)
    content='안녕하세요.'
    lang='en'
    translate_text(content,lang)
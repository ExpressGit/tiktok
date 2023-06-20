#!/usr/bin/env python  
# encoding: utf-8  


# import tkinter.messagebox  
# from tkinter import *

import pytesseract
from PIL import Image
from googletrans import Translator
import os

# def get_clip_image():
#     """
#     从剪切板获取图片，保存到本地
#     :return:
#     """
#     image_result = None
#     img = ImageGrab.grabclipboard()
#     if img and isinstance(img, Image.Image):
#         print(img.size)
#         print(img.mode)
#         image_result = './temp.png'
#         img.save(image_result)
#     return image_result


# def image_ocr(image_path):
#     """
#     识别图像中的英文
#     :return:
#     """
#     # 英文：lang='eng'
#     # 中文：lang='chi_sim'
#     return pytesseract.image_to_string(Image.open(image_path), lang='eng')


# def trans_eng(content_eng):
#     """
#     英文-中文
#     :param content:
#     :return:
#     """
#     translator = Translator(service_urls=['translate.google.cn'])
#     return translator.translate(content_eng, src='en', dest='zh-cn').text


# image_path = get_clip_image()

# if image_path:
#     # 获取文本
#     content_eng = image_ocr(image_path).replace("\r", " ").replace("\n", " ")

#     # 翻译
#     if content_eng:
#         content_chinese = trans_eng(content_eng)
#         print(content_chinese)

#         # 实现主窗口隐藏
#         root = Tk()
#         root.withdraw()
#         tkinter.messagebox.showinfo('翻译结果', content_chinese)

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
    res = translator.translate(content,dest=lang)
    # res = translator.translate('안녕하세요.',dest='en')
    print(res.text)

if __name__ == '__main__':
    images = ['/root/video_download/douyin/user_00后的窝/post/2023-01-07/2023-01-07 17.21.40_感谢喜欢你们要的一镜到底来啦你们是喜欢我/2023-01-07 17.21.40_感谢喜欢你们要的一镜到底来啦你们是喜欢我_cover.jpeg']
    judge_zimu_exist(images)
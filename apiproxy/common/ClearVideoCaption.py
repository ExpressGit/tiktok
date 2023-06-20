#!/usr/bin/env python  
# encoding: utf-8  

#https://github.com/weiyinfu/learnImageVideo/blob/master/learnMoviepy/33-%E7%9C%9F%E9%A6%99%E5%8E%BB%E6%8E%89%E5%AD%97%E5%B9%95.py

from os.path import *

import numpy as np
import pylab as plt
from moviepy.editor import VideoFileClip
from skvideo import io

"""
去掉字幕
"""
folder = dirname(__file__)
filepath = join(folder, "../imgs/delicious.gif")
a = io.vread(filepath)
f = VideoFileClip(filepath)
print(f.fps, f.duration, f.fps * f.duration)  # 一共有51张图片
print(a.shape)


def one():
    for i in range(len(a) - 1):
        x, y = a[i], a[i + 1]
        print(x.shape, y.shape)
        mask = np.zeros_like(x)
        mask[150:, :, :] = 1
        same = np.logical_and(np.abs(x - y) < 1e-4, mask)
        x[same] = 255
        y[same] = 255
        fig, axes = plt.subplots(2, 1)
        xx, yy = axes.reshape(-1)
        xx.imshow(x)
        yy.imshow(y)
        plt.show()


def find_split():
    # 分析每句话对应的帧数
    """
    0,8
    13,23
    26,35
    37,50
    :return:
    """
    fig, axes = plt.subplots(7, 8)
    axes = axes.reshape(-1)
    for i in range(len(a)):
        img = a[i]
        ax = axes[i]
        ax.imshow(img)
        ax.set_title(f"{i}")
    plt.show()


find_split()
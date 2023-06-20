#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@FileName   : WebApi.py
@Project    : apiproxy
@Description: 
@Author     : imgyh
@Mail       : admin@imgyh.com
@Github     : https://github.com/imgyh
@Site       : https://www.imgyh.com
@Date       : 2023/5/12 18:52
@Version    : v1.0
@ChangeLog 
------------------------------------------------

------------------------------------------------
'''

from flask import *
from apiproxy.douyin.douyinapi import DouyinApi
from apiproxy.douyin import douyin_headers
import argparse


def douyinwork(share_link, max_cursor, mode, cookie):
    dy = DouyinApi()

    if cookie is not None and cookie != "":
        douyin_headers["Cookie"] = cookie

    url = dy.getShareLink(share_link)
    key_type, key = dy.getKey(url)

    data = None
    rawdata = None
    cursor = None
    has_more = None
    if key_type == "user":
        if mode == 'post' or mode == 'like':
            data, rawdata, cursor, has_more = dy.getUserInfoApi(sec_uid=key, mode=mode, count=35,
                                                                max_cursor=max_cursor)
        elif mode == 'mix':
            data, rawdata, cursor, has_more = dy.getUserAllMixInfoApi(sec_uid=key, count=35, cursor=max_cursor)
        elif mode == 'detail':
            rawdata = dy.getUserDetailInfoApi(sec_uid=key)
            data = rawdata
    elif key_type == "mix":
        data, rawdata, cursor, has_more = dy.getMixInfoApi(mix_id=key, count=35, cursor=max_cursor)
    elif key_type == "music":
        data, rawdata, cursor, has_more = dy.getMusicInfoApi(music_id=key, count=35, cursor=max_cursor)
    elif key_type == "aweme":
        data, rawdata = dy.getAwemeInfoApi(aweme_id=key)
    elif key_type == "live":
        data, rawdata = dy.getLiveInfoApi(web_rid=key)

    datadict = {}


    datadict["data"] = data
    datadict["rawdata"] = rawdata
    datadict["cursor"] = cursor
    datadict["has_more"] = has_more

    return datadict


def deal(mode=None):
    usefuldict = {}
    if request.headers.get("content_type") == "application/json":
        result = request.get_json(force=True)
    else:
        result = request.form

    share_link = None
    cursor = 0
    cookie = None

    try:
        share_link = result["share_link"]
        cursor = result["cursor"]
        cookie = result["cookie"]
    except Exception as e:
        usefuldict["status_code"] = 500

    try:
        if share_link is not None and share_link != "":
            usefuldict = douyinwork(share_link, cursor, mode, cookie)
            usefuldict["status_code"] = 200
    except Exception as e:
        usefuldict["status_code"] = 500
    return jsonify(usefuldict)


app = Flask(__name__)
# 设置编码
app.config['JSON_AS_ASCII'] = False


def argument():
    parser = argparse.ArgumentParser(description='抖音去水印工具 使用帮助')
    parser.add_argument("--port", "-p", help="Web端口",
                        type=int, required=False, default=5000)
    args = parser.parse_args()

    return args


@app.route("/douyin/music", methods=["POST"])
def douyinMusic():
    return deal()


@app.route("/douyin/mix", methods=["POST"])
def douyinMix():
    return deal()


@app.route("/douyin/user/mix", methods=["POST"])
def douyinUserMix():
    return deal(mode="mix")


@app.route("/douyin/user/like", methods=["POST"])
def douyinUserLike():
    return deal(mode="like")


@app.route("/douyin/user/post", methods=["POST"])
def douyinUserPost():
    return deal(mode="post")

@app.route("/douyin/user/detail", methods=["POST"])
def douyinUserDetail():
    return deal(mode="detail")

@app.route("/douyin/aweme", methods=["POST"])
def douyinAweme():
    return deal()


@app.route("/douyin/live", methods=["POST"])
def douyinLive():
    return deal()


@app.route("/douyin", methods=["POST"])
def douyin():
    return deal()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    args = argument()
    app.run(debug=False, host="0.0.0.0", port=args.port)

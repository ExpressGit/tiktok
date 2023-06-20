#!/usr/bin/env python  
# encoding: utf-8  
from moviepy.editor import *
import whisper

#参考： https://www.jianshu.com/p/349000f6048c

def mp4_to_mp3(video_path):
    try:
       video = VideoFileClip(video_path)
       audio = video.audio
       # 设置生成的mp3文件路径
       newPath = video_path[:-4]+'.mp3'
       audio.write_audiofile(newPath)
       return newPath
    except Exception as e:
        print(e)
        return None


def reg_audo_text(video_path):
    # new_audio_path = mp4_to_mp3(video_path)
    new_audio_path = '/root/video_download/douyin/user_00后的窝/post/2023-04-12/2023-04-12 17.00.44_选对一个好花洒幸福感翻一翻装修花洒水爱花/2023-04-12 17.00.44_选对一个好花洒幸福感翻一翻装修花洒水爱花_video.mp3'
    # 语音识别
    model = whisper.load_model("small")
    result = model.transcribe(new_audio_path, language='chinese')
    print(result["text"])

    # 翻译
    # translator = Translator(from_lang="Chinese",to_lang="Japanese")

    # 提取字幕[起始时间，持续时间，字幕]
    segments = result['segments']
    l_subtitle = []
    for seg in segments:
        start = seg['start']
        end = seg['end']
        text = seg['text']
        # subtitle = [round(start,2), round(end-start, 2), translator.translate(text)]
        subtitle = [round(start,2), round(end-start, 2), text]
        print(subtitle)
        l_subtitle.append(subtitle)
    return l_subtitle

def videocaption(src_mp4, dst_mp4, subtitle):
    video = VideoFileClip(src_mp4)
    position = 'bottom'
    txts = []
    FONT_URL = 'apiproxy/font/HYBiRanTianTianQuanW-2.ttf'
    for start, duration, text in subtitle:
        txt = (TextClip(text, fontsize=40,font=FONT_URL, size=(1900, 40),
                        align='center', color='red')
                        .set_position(position)
                        .set_duration(duration).set_start(start))
        txts.append(txt)

    # 合成字幕
    video = CompositeVideoClip([video, *txts])
    # 合成音频
    # videos = video.set_audio(AudioFileClip('Python.mp3'))
    # 保存视频，注意加上参数audio_codec，否则音频无声音
    video.write_videofile(dst_mp4, audio_codec='mp3')

if __name__ == '__main__':
    src_mp4 = '/root/video_download/douyin/user_00后的窝/post/2023-04-12/2023-04-12 17.00.44_选对一个好花洒幸福感翻一翻装修花洒水爱花/2023-04-12 17.00.44_选对一个好花洒幸福感翻一翻装修花洒水爱花_video.mp4'
    dst_mp4 = '/root/video_download/douyin/user_00后的窝/post/2023-04-12/2023-04-12 17.00.44_选对一个好花洒幸福感翻一翻装修花洒水爱花/2023-04-12 17.00.44_选对一个好花洒幸福感翻一翻装修花洒水爱花_video_新字幕.mp4'
    l_subtitle = reg_audo_text(src_mp4)
    videocaption(src_mp4,dst_mp4,l_subtitle)

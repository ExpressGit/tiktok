'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2023-06-23 21:59:40
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2023-06-25 12:28:52
FilePath: /tiktok/apiproxy/common/AudioRecUtil.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import whisperx
import gc,re,sys,os
import torch
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.tools import cvsecs
# print(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from apiproxy.common.TranslateUtil import *
from apiproxy.common.FFmpegUtil import FFmpeg
# from TranslateUtil import *
# from FFmpegUtil import FFmpeg
#来源：whisperX:https://github.com/m-bain/whisperX

audio_file = '/root/video_download/douyin/user_00后的窝/post/2023-04-12/2023-04-12 17.00.44_选对一个好花洒幸福感翻一翻装修花洒水爱花/a.mp3'

def audio_to_text(audio_file):
    device = "cpu" 
    model_type='medium'
    batch_size = 2
    compute_type = "int8"
    model = whisperx.load_model(model_type, device=device, compute_type=compute_type)
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size,language='zh')
    print(result["segments"]) # before alignment
    # delete model if low on GPU resources
    gc.collect(); torch.cuda.empty_cache(); del model
    return result["segments"]

# 1. Transcribe with original whisper (batched)
# model = whisperx.load_model(model_type, device=device, compute_type=compute_type)

# audio = whisperx.load_audio(audio_file)
# result = model.transcribe(audio, batch_size=batch_size,language='zh')
# print(result["segments"]) # before alignment

# delete model if low on GPU resources
# import gc; gc.collect(); torch.cuda.empty_cache(); del model

# c2. Align whisper output
# model_a, metadata = whisperx.load_align_model(language_code='zh', device=device)
# result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

# print(result["segments"]) # after alignment

# # delete model if low on GPU resources
# import gc; gc.collect(); torch.cuda.empty_cache(); del model_a

# # 3. Assign speaker labels
# diarize_model = whisperx.DiarizationPipeline(use_auth_token=YOUR_HF_TOKEN, device=device)

# # add min/max number of speakers if known
# diarize_segments = diarize_model(audio_file)
# # diarize_model(audio_file, min_speakers=min_speakers, max_speakers=max_speakers)

# result = whisperx.assign_word_speakers(diarize_segments, result)
# print(diarize_segments)
# print(result["segments"]) # segments are now assigned speaker ID

def create_srt_file(segments, output_file):
    with open(output_file, 'w') as f:
        for i, segment in enumerate(segments):
            start_time = _format_time(segment['start'])
            end_time = _format_time(segment['end'])
            text = segment['text']
            subtitle = '{}\n{} --> {}\n{}\n\n'.format(i+1, start_time, end_time, text)
            f.write(subtitle)

def _format_time(time):
    m, s = divmod(int(time), 60)
    h, m = divmod(m, 60)
    return '{:02d}:{:02d}:{:02d},000'.format(h, m, s)


def get_audio_file(video_path,audio_file):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    # audio_clip.write_audiofile('output.wav')
    audio_clip.write_audiofile(audio_file)

def file_to_subtitles(filename):
    """ Converts a srt file into subtitles.

    The returned list is of the form ``[((ta,tb),'some text'),...]``
    and can be fed to SubtitlesClip.

    Only works for '.srt' format for the moment.
    """
    times_texts = []
    current_times = None
    current_text = ""
    with open(filename,'r') as f:
        for line in f:
            times = re.findall("([0-9]*:[0-9]*:[0-9]*,[0-9]*)", line)
            if times:
                current_times = [cvsecs(t) for t in times]
            elif line.strip() == '':
                times_texts.append((current_times, current_text.strip('\n')))
                current_times, current_text = None, ""
            elif current_times:
                current_text += line
    return times_texts

def ch_translate_to_en(segments):
    '''
    将中文字幕转为英文字幕
    输入([197.5, 199.159], '因为跑那边那条路线')
    '''
    en_segments = []
    if len(segments)==0:
        print("字幕 文件 为空")
        return
    for seg in segments:
        times = seg[0]
        seg_en = {'start':times[0],'end':times[1],'text':translate_text(seg[1],'en')}
        en_segments.append(seg_en)
    return en_segments

def add_subtitle_in_video(video_path,srt_file,output_video_path):
    ffmpeg_util = FFmpeg(video_path) 
    ffmpeg_util.add_video_subtitle(srt_file,output_video_path)
    print(" 视频 字幕 添加完成 done")

if __name__ == '__main__':
    pass
    video_file = '/root/video_download/bili/大山的农村人/2023-06-18/弟弟想和朋友合伙买车，被我反对了，现在又想一个人单干.mp4'
    audio_file = '/root/video_download/bili/大山的农村人/2023-06-18/a.mp3'
    origin_srt_file = '/root/video_download/bili/大山的农村人/2023-06-18/didi.srt'
    srt_file = '/root/video_download/bili/大山的农村人/2023-06-18/didi_en.srt'
    video_output_file = '/root/video_download/bili/大山的农村人/2023-06-18/a_subtitle.mp4'
    get_audio_file(video_file,audio_file)
    segments = audio_to_text(audio_file)
    print(segments)
    
    #构建字幕文件
    # segments = file_to_subtitles(origin_srt_file)
    # segments_en = ch_translate_to_en(segments)
    # create_srt_file(segments_en,srt_file)
    
    # add_subtitle_in_video(video_file,srt_file,video_output_file)
'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2023-06-23 21:59:40
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2023-07-18 20:37:18
FilePath: /tiktok/apiproxy/common/AudioRecUtil.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import gc,re,sys,os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.tools import cvsecs
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from apiproxy.common.FFmpegUtil import FFmpeg
from faster_whisper import WhisperModel
from apiproxy.common.TranslateUtil import translate_text
from tqdm import tqdm
#来源：https://github.com/guillaumekln/faster-whisper



def audio_to_text_by_fastwhisper(audio_file):
    # model_size = "large-v1"
    model_size = "small"
    # Run on GPU with FP16
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments_info = []
    segments, info = model.transcribe(audio_file, beam_size=5,vad_filter=True,vad_parameters=dict(min_silence_duration_ms=500))
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    for segment in segments:
        # print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        #[((ta,tb),'some text'),...]
        item = [(segment.start,segment.end),segment.text]
        segments_info.append(item)
    return segments_info
    

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
    for seg in tqdm(segments):
        times = seg[0]
        if len(seg[1])>0:
            seg_en = {'start':times[0],'end':times[1],'text':translate_text(seg[1],'en')}
            en_segments.append(seg_en)
    return en_segments

def add_subtitle_in_video(video_path,srt_file,output_video_path):
    ffmpeg_util = FFmpeg(video_path) 
    ffmpeg_util.add_video_subtitle(srt_file,output_video_path)
    print(" {}视频 字幕 添加完成 done, 输出地址{}".format(video_path,output_video_path))

if __name__ == '__main__':
    video_file = '/root/video_download/bili/【up】大山的农村人_1480975816/2023-07-07/万事俱备，只欠东风。今天带弟弟去把工具这些跟他备好.mp4'
    # audio_file = '/root/video_download/bili/大山的农村人_1480975816/2023-06-21/a.wav'
    audio_file = '/root/video_download/bili/【up】大山的农村人_1480975816/2023-07-07/万事俱备，只欠东风。今天带弟弟去把工具这些跟他备好.wav'
    # origin_srt_file = '/root/video_download/bili/我才是熊猫大G_267776898/2023-07-07/韩国人掏出烬中单，大G嘴都笑歪了，12分钟直接推门牙，对面人都傻了！_P01_中文（自动生成）.srt'
    srt_file = '/root/video_download/bili/【up】大山的农村人_1480975816/2023-07-07/万事俱备，只欠东风。今天带弟弟去把工具这些跟他备好.srt'
    video_output_file = '/root/video_download/bili/【up】大山的农村人_1480975816/2023-07-07/a_subtitle.mp4'
    # get_audio_file(video_file,audio_file)
    # segments = audio_to_text(audio_file)
    # print(segments)
    # audio_to_text_whisper(audio_file)
    # audio_to_text_google_api(audio_file)
    #构建字幕文件
    # segments = file_to_subtitles(origin_srt_file)
    # segments_en = ch_translate_to_en(segments)
    # create_srt_file(segments_en,srt_file)
    
    # add_subtitle_in_video(video_file,srt_file,video_output_file)
    
    # 利用whisper 生成 英文視頻
    get_audio_file(video_file,audio_file)
    segments = audio_to_text_by_fastwhisper(audio_file)
    segments_en = ch_translate_to_en(segments)
    create_srt_file(segments_en,srt_file)
    add_subtitle_in_video(video_file,srt_file,video_output_file)
    
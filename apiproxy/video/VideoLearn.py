# 导入需要的库
from moviepy.editor import *
import random,io,glob,os
# from moviepy.video.tools.drawing import circle
import string
import warnings
import asyncio
import aiohttp,aiofiles
from tiktokapipy import TikTokAPIWarning
warnings.filterwarnings("ignore", category=TikTokAPIWarning)
# from tiktokapipy.api import TikTokAPI
from tiktokapipy.async_api import AsyncTikTokAPI
from tiktokapipy.models.video import Video
import urllib.request
from os import path
import requests
from TikTokApi import TikTokApi
directory='/root/video_download/tiktok'


# async def save_video(video: Video, api: AsyncTikTokAPI):
#     origin_cookies = await api.context.cookies()
#     print(origin_cookies)
#     cookies = {
#         "msToken" : "YtYL2oW2KqUGtFqiObQ3Ljtpej0f1X4U7_WYo3_eYB2q5plplnTrsBGYYohRp7qfCwDTL1fL01j_wpjL5OcGADCl3ruYxyapGPNrm41JXlyXvzju1pyzRcnlBgKVLVpOwO2dlYNlhFiN0ymvgA==",
#         "tt_chain_token" : "1KTDxti9qQ1zO4fJ6MJzig==",
#         "sessionid" : "cca9cf0838caddddc18fa615682a4456",
#         "tt_webid" : "6913027209393473025",
#         "sid_guard" : "cca9cf0838caddddc18fa615682a4456%7C1686717917%7C15552000%7CMon%2C+11-Dec-2023+04%3A45%3A17+GMT",
#         "tt_csrf_token" : "08nUDmVt-TA5q2CMHZpriC0wxpUwGIQ0gCk0",
#         "ttwid" : "1%7CGMpPsH8-2YJhpqARFG7NzdLJnrPQZL7mSuxSxRMV_Ns%7C1689642137%7Ca795d7610f314797c3a4b4cb1e9658a0a19b3d8d7249aa1afcb4a7dd686d287f"
#     }
#     headers = {
#         'Host': 't.tiktok.com',
#         'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
#         'Referer': 'https://www.tiktok.com/',
#         'Origin' : 'https://www.tiktok.com',
#         'Cookie': cookies,
#         "region": 'JP',
#         "tt-web-region": 'JP',
#         "language": 'zh-CN',
#         "verifyFp": "verify_kjf974fd_y7bupmR0_3uRm_43kF_Awde_8K95qt0GcpBk"
#     }
#     async with aiohttp.ClientSession(cookies=cookies) as session:
#     # Creating this header tricks TikTok into thinking it made the request itself
#       async with session.get(video.video.play_addr, headers=headers) as resp:
#         print(video.desc)
#         return await resp.read()

# async def save_slideshow(video: Video):
#     # this filter makes sure the images are padded to all the same size
#     vf = "\"scale=iw*min(1080/iw\,1920/ih):ih*min(1080/iw\,1920/ih)," \
#          "pad=1080:1920:(1080-iw)/2:(1920-ih)/2," \
#          "format=yuv420p\""

#     for i, image_data in enumerate(video.image_post.images):
#         url = image_data.image_url.url_list[-1]
#         # this step could probably be done with asyncio, but I didn't want to figure out how
#         urllib.request.urlretrieve(url, path.join(directory, f"temp_{video.id}_{i:02}.jpg"))

#     urllib.request.urlretrieve(video.music.play_url, path.join(directory, f"temp_{video.id}.mp3"))

#     # use ffmpeg to join the images and audio
#     command = [
#         "ffmpeg",
#         "-r 2/5",
#         f"-i {directory}/temp_{video.id}_%02d.jpg",
#         f"-i {directory}/temp_{video.id}.mp3",
#         "-r 30",
#         f"-vf {vf}",
#         "-acodec copy",
#         f"-t {len(video.image_post.images) * 2.5}",
#         f"{directory}/temp_{video.id}.mp4",
#         "-y"
#     ]
#     ffmpeg_proc = await asyncio.create_subprocess_shell(
#         " ".join(command),
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE,
#     )
#     _, stderr = await ffmpeg_proc.communicate()
#     generated_files = glob.glob(path.join(directory, f"temp_{video.id}*"))

#     if not path.exists(path.join(directory, f"temp_{video.id}.mp4")):
#         # optional ffmpeg logging step
#         # logging.error(stderr.decode("utf-8"))
#         for file in generated_files:
#             os.remove(file)
#         raise Exception("Something went wrong with piecing the slideshow together")

#     with open(path.join(directory, f"temp_{video.id}.mp4"), "rb") as f:
#         ret = io.BytesIO(f.read())

#     for file in generated_files:
#         os.remove(file)

#     return ret

async def save_video(video: Video,api:AsyncTikTokAPI,cookies):
     async with aiohttp.ClientSession(cookies=cookies) as session:
        # Creating this header tricks TikTok into thinking it made the request itself
        async with session.get(video.video.download_addr, headers={"referer": "https://www.tiktok.com/"}) as resp:
            return await resp.read()


async def get_tiktok_trend_video():
    async with AsyncTikTokAPI() as api:
        user = await api.user("odapolf", video_limit=10)
        async for video in user.videos:
            print(video)
            video_bytes  = await save_video(video,api,{cookie['name']: cookie['value'] for cookie in api.context.cookies()})
            print("video_bytes:" + video_bytes.decode())
            file_path = os.path.join(directory,'{}.mp4'.format(video.desc))
            print(file_path)
            async with aiofiles.open(file_path, 'wb') as file:
                    await file.write(video_bytes)
        return "OK"



def get_tiktok_video_video():
    with TikTokApi() as api:
        video = api.video(id="7041997751718137094")

        # Bytes of the TikTok video
        video_data = video.bytes()

        with open("out.mp4", "wb") as out_file:
            out_file.write(video_data)





def get_video_basic_info(video_path):
    """
    获取视频的基础信息
    1、获取视频编辑对象
    2、视频宽、高、帧率
    3、分离音频
    """
    video_raw_clip = VideoFileClip(video_path)
    #宽、高
    video_width,video_height = video_raw_clip.w,video_raw_clip.h
    #视频时长
    duration = video_raw_clip.duration
    #帧率
    fps = video_raw_clip.fps
    #分离出audio
    audio_clip = video_raw_clip.audio
    
    return video_raw_clip,duration,video_width,video_height,fps,audio_clip

def video_add_random_transition(clip):
        """
        给视频增加特效
        """
        transitions = [
            # lambda c:c.fadein(3),  # 淡入特效 持续3秒
            # lambda c:c.fadeout(3), # 淡出特效 持续3秒
            # lambda c:vfx.freeze(c,freeze_duration=2),  # 冻结特效 持续2秒
            # lambda c:c.crossfadein(3), # #淡入淡出交叉 持续3秒
            # lambda c:vfx.invert_colors(c), # 色彩反转
            # lambda c:vfx.colorx(c,0.5),
            # lambda c:vfx.speedx(c,1.3),
            # lambda c:vfx.rotate(c,3), # 旋转3度
            # lambda c:vfx.painting(c,1.5), # 油画特效3秒
            lambda c:vfx.resize(c,0.5) #尺寸等比缩放0.5 #注意：只有写入文件后才有效果
            # lambda c:vfx.loop(c,n=2),  # 循环1次
            # lambda c:vfx.time_symmetrize(c), #倒放
            # lambda c:clip[::-1] #倒放
        ]
        # fl_time(lambda t: self.duration - t - 1, keep_duration=True)
        transition_func = random.choice(transitions)
        return transition_func(clip)


def video_add_end_transition(clip_origin):
    clip = clip_origin.\
           add_mask()
    # The mask is a circle with vanishing radius r(t) = 800-200*t               
    clip.mask.get_frame = lambda t: circle(screensize=(clip.w,clip.h),
                                        center=(clip.w/2,clip.h/2),
                                        radius=max(0,int((clip.duration+3)*100-100*t)),
                                        col1=1.0, col2=0, blur=4)


    # # Make the text. Many more options are available.
    txt_clip = (TextClip("The End",size=(900, 900), color="yellow", font='../font/STHeiti Medium.ttc',method='label')
                .set_position('center')
                .set_duration(clip_origin.duration+1))

    
    final_clip = CompositeVideoClip([txt_clip,clip],
                            size =clip.size)
    return final_clip
   

def video_add_Video_Text(text_content,video_clip,postion):
        """
        给视频增加文本
        #https://blog.itblood.com/2297.html
        """
        # print(TextClip.list("font"))
        FONT_URL = 'apiproxy/font/HYBiRanTianTianQuanW-2.ttf'
        txt_clip = (TextClip(text_content,fontsize=100,font=FONT_URL,color='yellow',method='label')
                    .set_position(postion)
                    .set_duration(video_clip.duration))
        
        final_clip = CompositeVideoClip([video_clip,txt_clip])
        return final_clip
    
def video_add_image(img_path,video_clip,postion):
    """
     增加图片loggo
     # https://blog.itblood.com/2295.html
    """
    logo = (ImageClip(img_path)
            # 水印持续时间
            .set_duration(video_clip.duration)
            # 水印高度，等比缩放
            .resize(height=300)
            # 水印的位置
            .set_position(postion)
            # 水印边距和透明度
            .margin(left=30, top=30,opacity=0))
    
    final_clip = CompositeVideoClip([video_clip,logo])
    return final_clip

def generate_mask_cover(video_path,video_title,postion,font_size):
        """
        生成视频的封面
        """
        img_temp_dir = '/root/workspace/imgtemp'
        FONT_URL = 'apiproxy/font/HYBiRanTianTianQuanW-2.ttf'
        video_clip = VideoFileClip(video_path)
        cover_video_png = video_path[:-4]+'_new_cover.png'
        img_save_path = os.path.join(img_temp_dir,"frame.png")
        #保存第一帧
        video_clip.save_frame(img_save_path)
        #设置封面标题
        # 读取视频
        img_clip = ImageClip(img_save_path).set_duration(1)
        # 文字视频
        text_clip = (TextClip(video_title,fontsize=font_size,font=FONT_URL,color='yellow',method='caption')
                    .set_position(postion)
                    .set_duration(1))

        # 合成视频
        composite_video_clip = CompositeVideoClip([img_clip,text_clip],size =img_clip.size)
        composite_video_clip.save_frame(cover_video_png)
        # 导出视频
        # finalclip = concatenate_videoclips(composite_video_clip,video_clip)
        return composite_video_clip
    
if __name__ == '__main__':
    video_path = '/root/video_download/douyin/user_小透明/post/2023-06-07/2023-06-07 19.12.41_考完了咱主打一个反差反差/2023-06-07 19.12.41_考完了咱主打一个反差反差_video.mp4'
    # video_raw_clip,duration,video_width,video_height,fps,audio_clip = get_video_basic_info(video_path)
    # clip = video_add_random_transition(video_raw_clip)
    # clip = video_add_end_transition(video_raw_clip)
    text_content = "思想杰出艺术之花\n思想杰出艺术之花"
    img_path = 'apiproxy/img/day09.jpg'
    # clip = video_add_Video_Text(text_content,video_raw_clip,postion=("center","top"))
    # clip = video_add_image(img_path,video_raw_clip,('left', 'top'))
    # clip = generate_mask_cover(video_path,text_content,("center"),font_size=150)
    # new_video_path = video_path[:-4]+"_cover_bg.mp4"
    # clip.write_videofile(new_video_path,fps=30)

    #tiktok
    result = get_tiktok_video_video()
    print(result)
   
    
# 导入需要的库
from moviepy.editor import *
import random
from moviepy.video.tools.drawing import circle
    
# # 从本地载入视频myHolidays.mp4并截取00:00:50 - 00:00:60部分
# clip = VideoFileClip(video_path).subclip(2,7)
 
# # 调低音频音量 (volume x 0.8)
# clip = clip.volumex(0.8)
 
# # 做一个txt clip. 自定义样式，颜色.
# txt_clip = TextClip("My Holidays 2013",fontsize=70,color='black')
 
# # 文本clip在屏幕正中显示持续10秒
# txt_clip = txt_clip.set_pos('center').set_duration(6)
 
# # 把 text clip 的内容覆盖 video clip
# video = CompositeVideoClip([clip, txt_clip])
 
# 把最后生成的视频导出到文件内
# video.write_videofile("/root/video_download/douyin/myHolidays_edited.mp4")

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
    video_raw_clip,duration,video_width,video_height,fps,audio_clip = get_video_basic_info(video_path)
    # clip = video_add_random_transition(video_raw_clip)
    # clip = video_add_end_transition(video_raw_clip)
    text_content = "思想杰出艺术之花\n思想杰出艺术之花"
    img_path = 'apiproxy/img/day09.jpg'
    # clip = video_add_Video_Text(text_content,video_raw_clip,postion=("center","top"))
    # clip = video_add_image(img_path,video_raw_clip,('left', 'top'))
    clip = generate_mask_cover(video_path,text_content,("center"),font_size=150)
    # new_video_path = video_path[:-4]+"_cover_bg.mp4"
    # clip.write_videofile(new_video_path,fps=30)

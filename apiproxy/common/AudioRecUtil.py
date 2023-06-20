import whisperx
import gc 
import torch

#来源：whisperX:https://github.com/m-bain/whisperX

device = "cpu" 
model_type='small'
audio_file = '/root/video_download/douyin/user_00后的窝/post/2023-04-12/2023-04-12 17.00.44_选对一个好花洒幸福感翻一翻装修花洒水爱花/2023-04-12 17.00.44_选对一个好花洒幸福感翻一翻装修花洒水爱花_video.mp3'
batch_size = 6 # reduce if low on GPU mem
compute_type = "int8" # change to "int8" if low on GPU mem (may reduce accuracy)

def audio_to_text(audio_file):
    device = "cpu" 
    model_type='small'
    batch_size = 6
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
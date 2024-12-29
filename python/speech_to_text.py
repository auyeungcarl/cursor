import speech_recognition as sr
import os
from pydub import AudioSegment
import tempfile
import math

def optimize_audio(audio):
    """优化音频质量"""
    # 转换为单声道
    audio = audio.set_channels(1)
    
    # 设置采样率为16kHz（语音识别的推荐采样率）
    audio = audio.set_frame_rate(16000)
    
    # 标准化音量
    audio = audio.normalize()
    
    # 提高音量
    audio = audio + 10
    
    return audio

def convert_mp3_to_wav(mp3_path):
    """将MP3文件转换为WAV格式"""
    try:
        # 读取MP3文件
        print("正在读取音频文件...")
        audio = AudioSegment.from_mp3(mp3_path)
        
        # 优化音频质量
        print("正在优化音频质量...")
        audio = optimize_audio(audio)
        
        # 创建临时文件
        temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_wav_path = temp_wav.name
        temp_wav.close()
        
        # 导出为WAV格式
        audio.export(temp_wav_path, format="wav")
        return temp_wav_path, len(audio)
    except Exception as e:
        print(f"转换音频格式时出错：{e}")
        return None, 0

def process_audio_chunk(recognizer, audio_chunk):
    """处理音频片段"""
    try:
        # 调整识别器参数
        recognizer.energy_threshold = 300  # 降低能量阈值，使其更容易检测到语音
        recognizer.dynamic_energy_threshold = True  # 动态调整能量阈值
        recognizer.pause_threshold = 0.8  # 设置较短的停顿阈值
        
        # 尝试多次识别
        for attempt in range(2):
            try:
                text = recognizer.recognize_google(audio_chunk, language='zh-CN')
                if text:
                    return text
            except sr.UnknownValueError:
                if attempt == 0:
                    print("第一次识别失败，正在重试...")
                continue
            except sr.RequestError as e:
                print(f"无法连接到语音识别服务；{e}")
                return ""
        
        print("无法识别此段音频内容")
        return ""
    except Exception as e:
        print(f"处理音频片段时出错：{e}")
        return ""

def convert_audio_file(file_path):
    """转换音频文件为文字"""
    # 创建识别器对象
    recognizer = sr.Recognizer()
    
    try:
        # 如果是MP3文件，先转换为WAV
        wav_path = file_path
        audio_length = 0
        if file_path.lower().endswith('.mp3'):
            print("正在将MP3转换为WAV格式...")
            wav_path, audio_length = convert_mp3_to_wav(file_path)
            if not wav_path:
                return None
        
        # 读取音频文件
        print("正在准备处理音频...")
        audio = AudioSegment.from_wav(wav_path)
        
        # 将音频分成较短的片段（10秒）
        chunk_length_ms = 10000  # 10秒
        chunks = math.ceil(len(audio) / chunk_length_ms)
        
        full_text = []
        
        print("正在转换为文字...")
        for i in range(chunks):
            start_time = i * chunk_length_ms
            end_time = min((i + 1) * chunk_length_ms, len(audio))
            
            # 提取音频片段
            chunk = audio[start_time:end_time]
            
            # 如果片段太短，跳过
            if len(chunk) < 1000:  # 小于1秒的片段
                continue
            
            # 保存临时文件
            temp_chunk = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            chunk.export(temp_chunk.name, format="wav")
            temp_chunk.close()
            
            # 处理音频片段
            with sr.AudioFile(temp_chunk.name) as source:
                # 调整环境噪音
                recognizer.adjust_for_ambient_noise(source, duration=min(0.5, len(chunk)/1000))
                
                # 读取音频数据
                audio_chunk = recognizer.record(source)
                text = process_audio_chunk(recognizer, audio_chunk)
                if text:
                    full_text.append(text)
                    print(f"片段 {i+1}/{chunks} 识别结果：{text}")
            
            # 删除临时文件
            os.unlink(temp_chunk.name)
        
        if full_text:
            final_text = " ".join(full_text)
            print("\n完整识别结果：", final_text)
            return final_text
        else:
            print("未能成功识别音频内容")
            
    except Exception as e:
        print(f"处理音频文件时出错：{e}")
    finally:
        # 如果是临时文件，则删除
        if wav_path != file_path and os.path.exists(wav_path):
            os.unlink(wav_path)
    
    return None

def main():
    print("=== 音频文件转文字工具 ===")
    print("请输入音频文件路径（支持MP3和WAV格式）：")
    file_path = input().strip()
    
    if not os.path.exists(file_path):
        print("文件不存在！")
        return
    
    if not (file_path.lower().endswith('.wav') or file_path.lower().endswith('.mp3')):
        print("目前只支持WAV和MP3格式的音频文件！")
        return
        
    convert_audio_file(file_path)

if __name__ == "__main__":
    main() 
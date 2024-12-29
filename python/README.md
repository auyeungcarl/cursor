# 语音转文字工具 (Speech to Text Tool)

这是一个简单的语音转文字工具，可以将语音文件或麦克风输入转换为文字。

## 功能特点
- 支持从麦克风实时录音并转换为文字
- 支持读取音频文件（WAV, AIFF, AIFF-C, FLAC）并转换为文字
- 使用Google Speech Recognition API进行语音识别
- 支持中文和英文语音识别

## 使用方法

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行程序：
```bash
python speech_to_text.py
```

3. 选择输入方式：
   - 输入1：使用麦克风录音
   - 输入2：转换音频文件

## 注意事项
- 使用麦克风录音时，请确保系统已正确配置麦克风设备
- 转换音频文件时，请确保文件格式正确（支持WAV, AIFF, AIFF-C, FLAC）
- 需要连接互联网才能使用Google Speech Recognition服务 
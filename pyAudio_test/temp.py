# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
import numpy as np
from datetime import datetime
import wave
from aip import AipSpeech
import time

APP_ID = '15106702'#百度AI开放平台的密匙
API_KEY = 'Ic6aB2jjXZvE9lzbtiAMqUDX'
SECRET_KEY = 'jEOqATCXa8auAZe2OmPNjlxwT59kzLgN'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def Voice_Recognition(WavFile):
    try:
        recognition_result = client.asr(get_file_content('%s'%WavFile), 'pcm', 16000, {'dev_pid': 1536,})
        print(recognition_result["result"])
    except Exception as e:
        print(e)


# 将data中的数据保存到名为filename的WAV文件中
def save_wave_file(filename, data):
    SAMPLING_RATE = 16000
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)#单声道
    wf.setsampwidth(2)#
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes(b"".join(data))
    wf.close()

def Voice_record_By_Time(TIME):
    NUM_SAMPLES = 2000
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1, rate=16000, input=True, frames_per_buffer=2000)
    save_buffer=[]
    count=0
    print('.')
    while count<TIME*10:#控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        save_buffer.append(string_audio_data)
        count+=1
    filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".wav"
    save_wave_file(filename, save_buffer)
    stream.close()
    print(filename, "saved")
    return filename

def Voice_Record_by_Quality():
    NUM_SAMPLES = 2000      # pyAudio内部缓存的块的大小
    SAMPLING_RATE = 16000    # 取样频率
    LEVEL = 2000            # 声音保存的阈值
    COUNT_NUM = 60          # NUM_SAMPLES个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
    SAVE_LENGTH = 8         # 声音记录的最小长度：SAVE_LENGTH * NUM_SAMPLES 个取样16000
    # 开启声音输入
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True,
                    frames_per_buffer=NUM_SAMPLES)

    save_count = 0
    save_buffer = []


    while True:
        string_audio_data = stream.read(NUM_SAMPLES)# 读入NUM_SAMPLES个取样
        audio_data = np.fromstring(string_audio_data, dtype=np.short)# 将读入的数据转换为数组
        large_sample_count = np.sum(audio_data > LEVEL) # 计算大于LEVEL的取样的个数:large_sample_count
        print(np.max(audio_data))
        if large_sample_count > COUNT_NUM:# 如果个数大于COUNT_NUM，则至少保存SAVE_LENGTH个块
            save_count = SAVE_LENGTH
        else:
            save_count -= 1

        if save_count < 0:
            save_count = 0

        if save_count > 0:
            # 将要保存的数据存放到save_buffer中
            save_buffer.append(string_audio_data)
        else:
            # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
            if len(save_buffer) > 0:
                filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".wav"
                save_wave_file(filename, save_buffer)
                save_buffer = []
                print(filename, "saved")
                break
    return filename


def main():
    # while True:
    #     WavFile = Voice_Record_by_Quality()
    #     Voice_Recognition(WavFile)
    #     time.sleep(10)

    WavFile = Voice_record_By_Time(5)
    Voice_Recognition(WavFile)
    time.sleep(10)

main()
# strs = ["三年多前我提出了一带一路倡议三年多来", "已经有一百多个国家和国际组织积极响应支持四十多个国家和国际组织中国签署合作协议一带一路的朋友圈正在扩大可以说一带一路倡议来自中国半城汇集世界"]
# str11 = ["中国"]
# str11.extend(strs)
# print(str11)
# result = "\n".join(strs)
# print(result)
'''
def my_record():
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    count=0
    print('.')
    while count<TIME*10:#控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count+=1

    save_wave_file('01.wav',my_buf)
    stream.close()
'''




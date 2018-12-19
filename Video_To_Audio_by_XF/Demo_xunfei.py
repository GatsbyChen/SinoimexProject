import os
import subprocess
from aip import AipSpeech
import urllib.request
import time
import urllib
import json
import hashlib
import base64
from urllib import parse

def Video_File_To_Audio(filepath):
    filelist = os.listdir(filepath)
    for files in filelist:
        if os.path.splitext(files)[1] == ".wav":
            os.remove(files)
    validlist = []
    for i in filelist:
        if os.path.splitext(i)[1] == ".mp4":#TODO:这里要考虑多种视频格式的兼容
            wg = subprocess.Popen(['ffmpeg.exe', '-i', '%s'%i], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            (standardout, junk) = wg.communicate()
            ans = str(standardout)
            num = ans.find("Duration:")
            out = ans[num + 10:num + 18]
            print(out)
            time_length = out.strip().split(":")
            print(int(time_length[0]))#视频时长
            minute = int(time_length[1])
            second = int(time_length[2])
            os.rename(i, 'temp.mp4')
            getmp = 'ffmpeg -i temp.mp4 -f wav -vn -ab 16 -ac 1 -ar 16000 temp.wav'
            returnget = subprocess.call(getmp, shell=True)
            print(returnget)
            count_min = 0
            while minute >= count_min:
                cutmp = "ffmpeg -i temp.wav -ss 00:0{0}:00 -to 00:0{1}:00 -acodec copy tempcut.wav".format(count_min,count_min+1)
                returncut = subprocess.call(cutmp, shell=True)
                os.rename('tempcut.wav', os.path.splitext(i)[0] + '_{0}.wav'.format(count_min))
                count_min += 1
                validlist.append(count_min)
                print(returncut)
    os.remove('temp.wav')
    return validlist

def Get_Audio_Filelist(filepath):
    filelist = os.listdir(filepath)
    Audiolist = []
    for i in filelist:
        if os.path.splitext(i)[1] == ".wav":
            Audiolist.append(i)
    print(Audiolist)
    return Audiolist

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def Xunfei_Audio_Recognization(file_content):
    # f = open("C:\\Users\\232\\PycharmProjects\\SinoimexProject\\Larger_Video_File\\2min.wav", 'rb')
    # file_content = f.read()
    base64_audio = base64.b64encode(file_content)
    body = parse.urlencode({'audio': base64_audio})

    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    api_key = 'd613d6609b0b8755bfa9f3402841cb62'
    param = {"engine_type":"sms16k","aue":"raw", "vad_eos ":"10000", "scene":"main"}#scene=main热词功能

    x_appid = '5c10b8ee'
    json_str = json.dumps(param).replace(' ', '')
    print('json_str:{}'.format(json_str))
    x_param = base64.b64encode(bytes(json_str, 'ascii'))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum_str = api_key + str( x_time ) + str(x_param)[2:-1]
    print('x_checksum_str:[{}]'.format(x_checksum_str))
    x_checksum = hashlib.md5(x_checksum_str.encode(encoding='ascii')).hexdigest()
    print('x_checksum:{}'.format(x_checksum))
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}

    start_time = time.time()
    req = urllib.request.Request(url, bytes(body, 'ascii'), x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    print( "used time: {}s".format( round( time.time() - start_time, 2 ) ) )
    print('result:'+str(result.decode(encoding='UTF8')))
    recognition_result = eval(result.decode(encoding='UTF8'))["data"]
    return recognition_result


def Audio_To_Words(filepath):
    Audio_Files = Get_Audio_Filelist(filepath)
    Re_Result_save = []
    for file in Audio_Files:
        try:
            recognition_result = Xunfei_Audio_Recognization(get_file_content('{0}'.format(file)))
            Re_Result_save.extend(recognition_result)
        except Exception as e:
            print(e)
    print(Re_Result_save)
    Text_save = "\n".join(Re_Result_save)
    with open("Recognization_Text.txt", "w", encoding="utf-8") as f:
        f.write(Text_save)

if __name__ == "__main__":
    filepath = "C:\\Users\\2067\\PycharmProjects\\test1\\baidu_api_tech_\\pyAudio_test\\"
    Video_File_To_Audio(filepath)
    Get_Audio_Filelist(filepath)
    Audio_To_Words(filepath)



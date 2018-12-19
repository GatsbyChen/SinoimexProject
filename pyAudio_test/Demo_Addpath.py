import os
import subprocess
import time
from aip import AipSpeech

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

def Audio_To_Words(client, filepath):
    Audio_Files = Get_Audio_Filelist(filepath)
    Re_Result_save = []
    for file in Audio_Files:
        try:
            recognition_result = client.asr(get_file_content('{0}'.format(file)), 'pcm', 16000, {'dev_pid': 1536, })
            print(recognition_result["result"][0])
            Re_Result_save.extend(recognition_result["result"])
        except Exception as e:
            print(e)
    print(Re_Result_save)
    Text_save = "\n".join(Re_Result_save)
    with open("Recognization_Text.txt", "w", encoding="utf-8") as f:
        f.write(Text_save)

if __name__ == "__main__":
    APP_ID = '15106702'#百度AI开放平台的密匙
    API_KEY = 'Ic6aB2jjXZvE9lzbtiAMqUDX'
    SECRET_KEY = 'jEOqATCXa8auAZe2OmPNjlxwT59kzLgN'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    filepath = "C:\\Users\\2067\\PycharmProjects\\test1\\baidu_api_tech_\\pyAudio_test\\"
    Video_File_To_Audio(filepath)
    Get_Audio_Filelist(filepath)
    Audio_To_Words(client, filepath)



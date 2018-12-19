import os
import subprocess
current = os.getcwd()
dirs = os.listdir(current)
# for i in dirs:
#     if os.path.splitext(i)[1] == ".mp4":
#         # bname = str(os.path.splitext(i)[0].encode('utf-8')).replace('\\','%').replace(' ','_')
#         os.rename(i, 'temp.mp4')
#         getmp3 = 'ffmpeg -i temp.mp4 -f wav -vn -ab 16 -ac 1 -ar 16000 temp.wav'
#         cutmp3 = 'ffmpeg -i temp.wav -ss 00:00:20 -to 00:00:59 -acodec copy tempcut.wav'
#         returnget = subprocess.call(getmp3, shell=True)
#         returncut = subprocess.call(cutmp3, shell=True)
#         os.remove('temp.wav')
#         os.rename('tempcut.wav', os.path.splitext(i)[0] + '.wav')
#         os.rename('temp.mp4', i)
#         print(returnget, returncut)

for i in dirs:
    if os.path.splitext(i)[1] == ".pcm":
        cutmp3 = 'ffmpeg -i 5min.pcm -ss 00:01:00 -to 00:01:59 -acodec copy 2min.wav'
        returncut = subprocess.call(cutmp3, shell=True)
        print(returncut)

# for i in dirs:
#     if os.path.splitext(i)[1] == ".mp4":
#         get_video_time = "ffmpeg -i video/sampleVideo.mp4 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//"
#         returnget = subprocess.call(get_video_time, shell=True)
#         print(returnget)

# # def getTime():
#    # #file_str = '1.flv'
#    # file_str = flvpath
# wg = subprocess.Popen(['ffmpeg.exe', '-i', 'sampleVideo.mp4'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# (standardout, junk) = wg.communicate()
# ans = str(standardout)
# num = ans.find("Duration:")
# print(num)
# out = ans[num+10:num+18]
# print(out.strip().split(":"))
#    # fid.write(file_str + "<| time is |>" + out)
#    # fid.write("\r\n")
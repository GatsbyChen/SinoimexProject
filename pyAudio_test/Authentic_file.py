#!/usr/bin/python
# -*- coding: UTF-8 -*-
#语音识别核心技术由科大讯飞提供
import urllib.request
import time
import urllib
import json
import hashlib
import base64
from urllib import parse

def main():
    f = open("C:\\Users\\232\\PycharmProjects\\SinoimexProject\\temp.wav", 'rb')
    file_content = f.read()
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
    print(result)
    print(type(result))
    result = result.read()
    print( "used time: {}s".format( round( time.time() - start_time, 2 ) ) )
    print(result)
    print(type(result))
    print('result:'+str(result.decode(encoding='UTF8')))
    print(eval(result.decode(encoding='UTF8'))["data"])
    return

if __name__ == '__main__':
    main()

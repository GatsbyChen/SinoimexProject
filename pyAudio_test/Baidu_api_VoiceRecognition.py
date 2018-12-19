import pandas as pd
import datetime
from aip import AipSpeech
import codecs

APP_ID = '15106702'#百度AI开放平台的密匙
API_KEY = 'Ic6aB2jjXZvE9lzbtiAMqUDX'
SECRET_KEY = 'jEOqATCXa8auAZe2OmPNjlxwT59kzLgN'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def Voice_Recognition():
    try:
        recognition_result = client.asr(get_file_content('temp_0.wav'), 'pcm', 16000, {'dev_pid': 1536,})
        print(recognition_result["result"])

    except Exception as e:
        print(e)

Voice_Recognition()
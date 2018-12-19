#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用于测试语音识别系统语音模型的程序

"""
import platform as plat
import os
import sys
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from keras.utils import multi_gpu_model

from SpeechModel_DFCNN import ModelSpeech
#from SpeechModel_old import ModelSpeech
'''
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
#进行配置，使用90%的GPU
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.9
#config.gpu_options.allow_growth=True   #不全部占满显存, 按需分配
set_session(tf.Session(config=config))
'''
iters_num = sys.argv[1]
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0, 1"
#进行配置，使用70%的GPU
config = tf.ConfigProto(allow_soft_placement=True)
config.gpu_options.per_process_gpu_memory_fraction = 0.95
#config.gpu_options.allow_growth=True   #不全部占满显存, 按需分配
set_session(tf.Session(config=config))

datapath = ''
modelpath = 'model_speech'


if(not os.path.exists(modelpath)): # 判断保存模型的目录是否存在
	os.makedirs(modelpath) # 如果不存在，就新建一个，避免之后保存模型的时候炸掉

system_type = plat.system() # 由于不同的系统的文件路径表示不一样，需要进行判断
if(system_type == 'Windows'):
	datapath = 'E:\\语音数据集'
	modelpath = modelpath + '\\'
elif(system_type == 'Linux'):
	datapath = 'dataset'
	modelpath = modelpath + '/'
else:
	print('*[Message] Unknown System\n')
	datapath = 'dataset'
	modelpath = modelpath + '/'

ms = ModelSpeech(datapath)

ms.LoadModel(modelpath + 'm_dfcnn/speech_model_dfcnn_e_0_step_'+iters_num+'000.model')
#ms.LoadModel(modelpath + 'm_DFCNN/speech_model_DFCNN_e_0_step_84000.model')
ms.TestModel(datapath, str_dataset='test', data_count = 64, out_report = True)

r = ms.RecognizeSpeech_FromFile('dataset/data_aishell/wav/dev/S0733/BAC009S0733W0234.wav')
#r = ms.RecognizeSpeech_FromFile('E:\\语音数据集\\ST-CMDS-20170001_1-OS\\20170001P00020I0087.wav')
#r = ms.RecognizeSpeech_FromFile('E:\\语音数据集\\wav\\train\\A11\\A11_167.WAV')
#r = ms.RecognizeSpeech_FromFile('E:\\语音数据集\\wav\\test\\D4\\D4_750.wav')
print('*[提示] 语音识别结果：\n',r)



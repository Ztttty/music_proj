# -*- coding: utf-8 -*-
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import pyaudio
import wave
import numpy as np
import pygame
from threading import Timer
import time
def Monitor():
    time_start=time.time()
    CHUNK = 512
    max_temp = 0
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 48000
    RECORD_SECONDS = 5
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    timecost=time.time()-time_start
    large_sample_count=0
    temp=0
    max_temp=0
    while (timecost<0.9):#持续读取音流
        timecost=time.time()-time_start
        data = stream.read(CHUNK)
#         for i in range(0, 100):
#             data = stream.read(CHUNK*100)
#             frames.append(data)
#             print (data)
        audio_data = np.fromstring(data, dtype=np.short)
#         print(audio_data)
#         large_sample_count = np.sum( audio_data > 800 )
#         t=audio_data[audio_data>=10] #取均值 采样出错
#         avg= np.mean(t)
            
        temp = np.max(audio_data)
        if(temp>max_temp):
            max_temp = temp
#         print (large_sample_count,temp,max_temp)
#     print (temp,max_temp)
#     print (temp,max_temp,avg)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return int(max_temp)

def if_under_control(a):
    a = time.time()
    if(volume.GetMasterVolumeLevel()>=-50 and volume.GetMasterVolumeLevel()<=-23):
        return True#好着
    else :
        return False

def play_music():
        filepath = r"calmsoul.mp3";
        pygame.mixer.init()
        # 加载音乐
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play(start=0.0)
        


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))        


#pygame.mixer.music.pause()
from threading import Timer
import time
time_begin=time.time()
volume.SetMasterVolumeLevel(-34, None)#22
play_music()
def func():
    if(not pygame.mixer.music.get_busy()):
        play_music()
    x1= Monitor()
    sumtime=time.time()-time_begin
    print(int(sumtime))
    a = time_begin
    if(((int(sumtime)%10==0) or (int(sumtime)%10==1))  and volume.GetMasterVolumeLevel()>=-50):#一定时间内  控制一下 改变之减少音量
        print('sumtime=',int(sumtime),'满10  减少咯当前音率',volume.GetMasterVolumeLevel())
        a = time.time()
        volume.SetMasterVolumeLevel(volume.GetMasterVolumeLevel()-1, None)
#         t.cancel()
    if(sumtime>3600):#时间过久(>1h)强制停止 
        t.cancel()
    x2= Monitor()
    change = x2-x1
    #条件为 将音律值映射到 0 - 25 区间 根据音量大小调节bias 0-250     25---最高可达400 --平均大致200-300
    if((abs(change))>(25+((volume.GetMasterVolumeLevel()+50)*10)) and volume.GetMasterVolumeLevel()<=-23):#变化不小了，改变之增大音量  
        volume.SetMasterVolumeLevel(volume.GetMasterVolumeLevel()+1, None)
        print("增大后 当前音率",volume.GetMasterVolumeLevel())
class RepeatingTimer(Timer): 
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)
# t = RepeatingTimer(0.95,Monitor)
t = RepeatingTimer(2,func)

t.start()


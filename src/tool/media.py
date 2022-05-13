# -*- encoding: utf-8 -*-
'''
@File    :   media.py
@Time    :   2022/05/13 10:19:00
@Author  :   Fenn 
@Version :   1.0.0b
@Contact :   realHifenn@outlook.com
'''

# here put the import lib
from requests import get as download
from time import sleep
from os import path, rename, remove
from pygame import mixer
from tool.FileType import getFileType
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal
fileList = []

def get(word, pauseTime = 5, accentType = 1):
    global fileList
    
    Path = path.abspath('.')
    # 使用 requests 从 youdaoDict 下载 media
    url = 'http://dict.youdao.com/dictvoice?audio=' + word + '&type=' + accentType
    
    # 判断是否已经存在，若存在则直接打开
    if not path.exists(Path + '\\' + word + '.MP3'):
        fileName = Path + '\\' + word + '.wav'
        if not path.exists(Path + '\\' + word + '.wav'):
            media = download(url)
            open(fileName, 'wb').write(media.content)  # 将 media 保存
    else:
        fileName = Path + '\\' + word + '.mp3'
    
    if getFileType(fileName) == 'unknown':  # 如果不是 wav 格式，则为 MP3
        try:
            rename(fileName, Path + '\\' + word + '.mp3')
            fileName = Path + '\\' + word + '.mp3'
        except FileExistsError:
            remove(fileName)
            fileName = Path + '\\' + word + '.mp3'
        except:
            print("[WARNING] Can't rename " + fileName + '!')

    play(fileName, pauseTime)
        
    fileList.append(fileName)
    return

def play(fileName, pauseTime):
    try:
        mixer.init()
        track = mixer.music.load(fileName)
        
        mixer.music.play()
        if pauseTime > 0:
            sleep(pauseTime)
        
        mixer.music.stop()
        print("[INFO] Played " + fileName)
    except:
        msg_box = QMessageBox(QMessageBox.Information, '遇到错误：', fileName + '\n播放时出现问题。\n请重试。')
        msg_box.exec_()
        print("[ERROR] Unknown when playing " + fileName + '!')
    return
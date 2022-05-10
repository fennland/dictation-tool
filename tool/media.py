# -*- encoding: utf-8 -*-
'''
@File    :   media.py
@Time    :   2022/05/10 22:14:14
@Author  :   Fenn 
@Version :   
@Contact :   realHifenn@outlook.com
'''

# here put the import lib
import time
import os
import pygame
import requests  # 用于下载音频文件
from tool.FileType import getFileType
from PyQt5.QtWidgets import QMessageBox
fileList = []

def get(word, ui, pauseTime):
    global fileList
    
    Path = os.path.abspath('.')
    
    # 使用 requests 从 youdaoDict 下载 media
    if ui.radioButton.isChecked() == True:
        url = 'http://dict.youdao.com/dictvoice?audio=' + word + '&type=1'
    else:
        url = 'http://dict.youdao.com/dictvoice?audio=' + word + '&type=2'
    
    # 判断是否已经存在，若存在则直接打开
    fileName = Path + '\\' + word + '.wav'
    if not os.path.exists(fileName):
        media = requests.get(url)
        open(fileName, 'wb').write(media.content)  # 将 media 保存
    
    if getFileType(fileName) == 'unknown':  # 如果不是 wav 格式，则为 MP3
        try:
            os.rename(fileName, Path + '\\' + word + '.mp3')
            fileName = Path + '\\' + word + '.mp3'
        except FileExistsError:
            os.remove(fileName)
            fileName = Path + '\\' + word + '.mp3'
        except:
            print("[WARNING] Can't rename " + fileName + '!')
    
    play(fileName, pauseTime, ui)
        
    fileList.append(fileName)
    return

def play(fileName, pauseTime, ui):
    try:
        pygame.mixer.init()
        track = pygame.mixer.music.load(fileName)
        
        pygame.mixer.music.play()
        if pauseTime > 0:
            time.sleep(pauseTime)
        
        pygame.mixer.music.stop()
        print("[INFO] Played " + fileName)
    except:
        msg_box = QMessageBox(QMessageBox.Information, '遇到错误：', fileName + '\n播放时出现问题。\n请重试。')
        msg_box.exec_()
        ui.statusbar.clearMessage()
        ui.statusbar.showMessage("错误：播放时遇到问题。", 2000)
        print("[ERROR] Unknown when playing " + fileName + '!')
    return
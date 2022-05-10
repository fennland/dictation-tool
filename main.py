# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2022/05/10 22:13:54
@Author  :   Fenn 
@Version :   
@Contact :   realHifenn@outlook.com
'''

# here put the import lib
import sys
import ui.Ui_randomDictation as Ui_randomDictation
import tool.media as media
import os
import atexit  # 退出前清空下载的声音
from random import shuffle  # 乱序
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from functools import partial


def clickDictate(ui):
    ui.pushButton.setEnabled(False)  # 暂时禁止点击
    ui.spinBox.setEnabled(False)
    
    vocabulary = ui.plainTextEdit.toPlainText()
    pauseTime = ui.spinBox.value()
    ui.statusbar.showMessage("解析词汇...")
    
    if len(vocabulary) != 0:
        vocabulary = vocabulary.split("\n")
        print('[INFO] Vocabulary List: ' + str(vocabulary))
    
        if ui.checkBox.isChecked() == True:  # 乱序
            shuffle(vocabulary)
            ui.statusbar.clearMessage()
            ui.statusbar.showMessage("乱序排列...")

        counts = 0
        for word in vocabulary:
            ui.statusbar.clearMessage()
            counts += 1
            ui.statusbar.showMessage("正在朗读 #" + str(counts) +": " + word + "...")
            sys.stdout.flush()  # 刷新缓冲区
            media.get(word, ui, pauseTime)

            if word == vocabulary[-1]:  # 最后一个
                ui.statusbar.clearMessage()
                ui.statusbar.showMessage("就绪")
        
    else:
        msg_box = QMessageBox(QMessageBox.Information, '遇到错误：', '请输入单词。')
        msg_box.exec_()
        ui.statusbar.clearMessage()
        ui.statusbar.showMessage("就绪")
    
    ui.pushButton.setEnabled(True)  # 暂时禁止点击
    return

def beforeExit():  # 删除
    print("[INFO] Removing files...")
    for item in media.fileList:
        try:
            os.remove(item)
        except:
            print("[WARNING] Can't remove " + item + '!')

def aboutGithub():
    os.system("explorer https://github.com/F3nn/dictation-tool")
    return

def aboutThanks():
    msg_box = QMessageBox(QMessageBox.Information, '鸣谢：', '暂时还没有鸣谢捏。\n感谢我自己！感谢互联网！')
    msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_randomDictation.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    ui.pushButton.clicked.connect(partial(clickDictate, ui))  # 传参 partial(func, arg1, arg2...)
    ui.statusbar.showMessage("就绪")
    ui.actionGithub.triggered.connect(aboutGithub)
    ui.actionGithub.triggered.connect(aboutThanks)
    
    atexit.register(beforeExit)
    sys.exit(app.exec_())


# tempfile 模块用法：http://c.biancheng.net/view/2560.html
# pygame 播放音乐用法：https://www.cnblogs.com/ocean1100/p/9319891.html
# requests 下载用法：https://zhuanlan.zhihu.com/p/162965342
# PyQt5 用法：https://blog.csdn.net/AzureMouse/article/details/90338961
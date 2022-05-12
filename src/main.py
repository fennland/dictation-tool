# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2022/05/12 23:32:11
@Author  :   Fenn 
@Version :   1.0.1a
@Contact :   realHifenn@outlook.com
'''

# here put the import lib
import sys
import atexit

import ui.Ui_randomDictation as Ui_randomDictation
import tool.media as media
import tool.constants as constants

from os import remove
from random import shuffle
from functools import partial
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal


class MainWindow(QMainWindow, Ui_randomDictation.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        atexit.register(self.beforeExit)
        
        self.pushButton.clicked.connect(self.clickDictate)  # 传参 partial(func, arg1, arg2...)
        self.pushButton_2.clicked.connect(self.plainTextEdit.clear)
        self.statusbar.showMessage("就绪")
        self.actionGithub.triggered.connect(partial(self.about, 'Github'))
        self.actionThanks.triggered.connect(partial(self.about, 'Thanks'))
        self.actionLog.triggered.connect(partial(self.about, 'log'))

    def clickDictate(self):
        vocabulary = self.plainTextEdit.toPlainText()
        pauseTime = self.spinBox.value()
        readTimes = self.spinBox_2.value()
        
        if len(vocabulary) != 0:
            vocabulary = vocabulary.split("\n")
            self.flushStatus("解析词汇...", '[INFO] Vocabulary List: ' + str(vocabulary))

            self.plainTextEdit.clear()  # 清除内容
            if self.checkBox.isChecked():  # 乱序
                shuffle(vocabulary)
                self.flushStatus("乱序排列...", '[INFO] Change the order of the vocabulary List: ' + str(vocabulary))
            
            if self.radioButton.isChecked():
                accentType = '1'
            else:
                accentType = '2'
            
            self.thread = dictationThread(vocabulary, pauseTime, accentType, readTimes)
            self.thread.statusSignal.connect(self.flushStatus)  # 将子线程的状态信号与 flushStatus 连接
            self.thread.start()

        else:
            msg_box = QMessageBox(QMessageBox.Information, '遇到错误：', '请输入单词。')
            msg_box.exec_()
            self.flushStatus("就绪", '[WARNING] Empty input!')
        return

    def beforeExit(self):  # 删除
        self.flushStatus("退出...", '[INFO] Removing files...')
        for item in media.fileList:
            try:
                remove(item)
            except:
                print("[WARNING] Can't remove " + item + '!')

    def about(self, mode: str):
        if mode == 'Github':
            title = '重定向至 Github......'
            content = constants.github
        elif mode == 'Thanks':
            title = '鸣谢:'
            content = constants.thanks
        elif mode == 'log':
            title = '更新日志 ' + constants.version
            content =  constants.publishedDate + '\n' + constants.log
        msg_box = QMessageBox(QMessageBox.Information, title, content)
        msg_box.exec_()
        return

    def flushStatus(self, status: str, commandMessage = ''):
            self.statusbar.clearMessage()
            self.statusbar.showMessage(status)
            if len(commandMessage) != 0:
                print(commandMessage)
            if status == '就绪':
                self.pushButton.setEnabled(True)  # 恢复
            else:
                self.pushButton.setEnabled(False)
            return

class dictationThread(QThread):
    statusSignal = pyqtSignal(str, str)  # 发送状态信号
    
    def __init__(self, vocabulary: list, pauseTime: int, accentType: int, readTimes: int):
        super (dictationThread, self).__init__()
        self.vocabulary = vocabulary
        self.pauseTime = pauseTime
        self.accentType = accentType
        self.readTimes = readTimes
        
    def run(self):
        counts = 0
        for word in self.vocabulary:
            print(word)
            counts += 1
            self.statusSignal.emit("正在朗读 #" + str(counts) +": " + word + "...", '')
            media.get(word, self.pauseTime, self.accentType, self.readTimes)

            if word == self.vocabulary[-1]:  # 最后一个
                self.statusSignal.emit("就绪", '')
                self.quit()
                self.wait()
                self.deleteLater()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
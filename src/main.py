# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2022/05/14 00:18:10
@Author  :   Fenn 
@Version :   1.1.0a
@Contact :   realHifenn@outlook.com
'''

# here put the import lib
import sys
import atexit

import ui.Ui_randomDictation as Ui_randomDictation
import tool.media as media
import tool.constants as constants
import tool.file as file

from os import remove
from random import shuffle
from functools import partial
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow, Ui_randomDictation.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        
        atexit.register(self.beforeExit)
        self.File = file.fileProcess(self)
        
        self.pushButton.clicked.connect(self.clickDictate)  # 传参 partial(func, arg1, arg2...)
        self.pushButton_2.clicked.connect(self.plainTextEdit.clear)
        
        self.statusbar.showMessage("就绪")
        
        self.listWidget.itemDoubleClicked.connect(self.listDoubleClicked)
        
        self.actionGithub.triggered.connect(partial(self.about, 'Github'))
        self.actionThanks.triggered.connect(partial(self.about, 'Thanks'))
        self.actionLog.triggered.connect(partial(self.about, 'log'))
        
        self.actionFileSave.setEnabled(False)
        self.actionFileSavedAs.setEnabled(False)
        self.actionFileOpen.triggered.connect(partial(self.fileAction, 'open'))
        self.actionFileSave.triggered.connect(partial(self.fileAction, 'save'))
        self.actionFileSavedAs.triggered.connect(partial(self.fileAction, 'savedAs'))
        self.plainTextEdit.textChanged.connect(partial(self.fileAction, 'edited'))  # TODO
        self.actionExpert.triggered.connect(partial(self.fileAction, 'expert'))  # TODO
        self.actionExpertAll.triggered.connect(partial(self.fileAction, 'expertAll'))  # TODO


    def clickDictate(self):
        self.vocabulary = self.plainTextEdit.toPlainText()
        self.pauseTime = self.spinBox.value()
        self.readTimes = self.spinBox_2.value()
        
        if len(self.vocabulary) != 0:
            self.vocabulary = self.vocabulary.split("\n")
            self.flushStatus("解析词汇...", '[INFO] Vocabulary List: ' + str(self.vocabulary))

            if self.checkBox.isChecked():  # 乱序
                shuffle(self.vocabulary)
                self.flushStatus("乱序排列...", '[INFO] Change the order of the vocabulary List: ' + str(self.vocabulary))
            
            self.plainTextEdit.clear()  # 清除内容
            counts = 0
            for word in self.vocabulary:  # 逐个添加列表框
                item = QListWidgetItem()
                item.setText(word)
                self.listWidget.addItem(item)
                counts += 1
                
            
            if self.radioButton.isChecked():
                self.accentType = '1'
            else:
                self.accentType = '2'
            
            self.thread = dictationThread(self.vocabulary, self.pauseTime, self.accentType, self.readTimes)
            self.thread.statusSignal.connect(self.flushStatus)  # 将子线程的状态信号与 flushStatus 连接
            self.thread.start()

        else:
            msg_box = QMessageBox(QMessageBox.Information, '遇到错误：', '请输入单词。')
            msg_box.exec_()
            self.flushStatus("就绪", '[WARNING] Empty input!')
        return


    def listDoubleClicked(self):
        word = [(self.listWidget.selectedItems())[0].text()]  # TODO: multiple items selected, read them
        self.thread = dictationThread(word, self.pauseTime, self.accentType, self.readTimes)
        self.thread.statusSignal.connect(self.flushStatus)  # 将子线程的状态信号与 flushStatus 连接
        self.thread.start()


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


    def flushStatus(self, status: str, commandMessage = '', time = 0):
            self.statusbar.clearMessage()
            if time == 0:
                self.statusbar.showMessage(status)
            else:
                self.statusbar.showMessage(status, time)
                
            if len(commandMessage) != 0:
                print(commandMessage)
            if status == '就绪' or status == '已保存':
                self.pushButton.setEnabled(True)  # 恢复
            else:
                self.pushButton.setEnabled(False)
            return


    def fileAction(self, mode: str):  # TODO
        if mode == "open":
            self.File.open()
        elif mode == "save":
            self.File.save()
        elif mode == "savedAs":
            self.File.savedAs()
        elif mode == "edited":
            if self.File.fileName != '':
                self.setWindowTitle(constants.productName + ' ' + constants.version + ' - ' + self.File.fileName + '*')
            else:
                self.setWindowTitle(constants.productName + ' ' + constants.version + ' - untitled.txt*')
            self.actionFileSave.setEnabled(True)
            self.actionFileSavedAs.setEnabled(True)
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
        
    
class ExpertThread(QThread):  # TODO
    statusSignal = pyqtSignal(str, str)  # 发送状态信号
    
    def __init__(self, mode = False):
        super (ExpertThread, self).__init__()
        self.mode = mode
    
    def run(self):
        pass

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon("../media/favicon.ico"))
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
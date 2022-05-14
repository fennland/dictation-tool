# -*- encoding: utf-8 -*-
'''
@File    :   file.py
@Time    :   2022/05/14 12:21:58
@Author  :   Fenn 
@Version :   1.1.0a
@Contact :   realHifenn@outlook.com
'''

# here put the import lib
import struct
import tool.constants as constants
from PyQt5.QtWidgets import QFileDialog

class fileProcess():  # TODO
    def __init__(self, ui):
        self.ui = ui
        self.filePath = ''
        self.fileName = ''
        self.fileType = ''
        self.savePath = ''
    
    
    def open(self):
        self.filePath, self.fileType = QFileDialog.getOpenFileName(None,
                                    "选取文件",
                                    "./",
                                    "Text Files (*.txt);;All Files (*)")   #设置文件扩展名过滤,注意用双分号间隔
        if self.filePath != '':
            try:
                self.content = open(self.filePath, 'r+').read()
            except FileNotFoundError:
                self.ui.flushStatus("错误: 未能找到 " + self.filePath +"!", '[ERROR]: No such file or directory: ' + self.filePath)
            else:
                self.fileName = (self.filePath.split("/"))[-1]
            
                self.ui.plainTextEdit.setPlainText(self.content)
                self.ui.actionFileSave.setEnabled(True)
                self.ui.actionFileSavedAs.setEnabled(True)
                self.ui.setWindowTitle(constants.productName + ' ' + constants.version + ' - ' + self.fileName + '*')
                self.ui.flushStatus("就绪", "[INFO]: Opening " + self.filePath, 3000)
    
    
    def save(self):
        if self.filePath != '':
            with open(self.filePath, 'w', encoding='utf-8') as f:  #使用with open()新建对象f
                self.ui.flushStatus("保存: " + self.filePath, "[INFO]: Saving " + self.filePath, 5000)
                for char in self.ui.plainTextEdit.toPlainText():
                    f.write(char)
            self.ui.flushStatus("已保存", "[INFO]: Saved!", 2000)
            self.ui.setWindowTitle(constants.productName + ' ' + constants.version + ' - ' + self.fileName + '*')
        else:
            self.savedAs()
    
    
    def savedAs(self):
        self.savePath, status = QFileDialog.getSaveFileName(None,
                                    "文件保存",
                                    "./",
                                    "Text Files (*.txt);;All Files (*)")
        if self.filePath != '':
            with open(self.savePath, 'w', encoding='utf-8') as f:  #使用with open()新建对象f
                self.ui.flushStatus("保存为: " + self.savePath, "[INFO]: Saving as " + self.savePath + " with status: " + status, 3)
                for char in self.ui.plainTextEdit.toPlainText():
                    f.write(char)
            self.filePath = self.savePath
            self.fileName = (self.filePath.split("/"))[-1]
            self.ui.flushStatus("已保存", "[INFO]: Saved!")
            self.ui.setWindowTitle(constants.productName + ' ' + constants.version + ' - ' + self.fileName)
    
    def close(self):  # TODO
        pass


type_dict = {
    '57415645': 'wav',
    '52494646': 'wav'
}
max_len = len(max(type_dict, key=len)) // 2


def getFileType(filename):
    # 读取二进制文件开头一定的长度
    with open(filename, 'rb') as f:
        byte = f.read(max_len)
    # 解析为元组
    byte_list = struct.unpack('B' * max_len, byte)
    # 转为16进制
    code = ''.join([('%X' % each).zfill(2) for each in byte_list])
    # 根据标识符筛选判断文件格式
    result = list(filter(lambda x: code.startswith(x), type_dict))
    if result:
        return type_dict[result[0]]
    else:
        return 'unknown'
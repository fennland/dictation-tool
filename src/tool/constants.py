# -*- encoding: utf-8 -*-
'''
@File    :   constants.py
@Time    :   2022/05/13 00:16:20
@Author  :   Fenn 
@Version :   1.0.1a
@Contact :   realHifenn@outlook.com
'''

# here put the import lib


version = '1.0.1a'
publishedDate = '2022/05/12'

github = 'https://github.com/F3nn/dictation-tool'
thanks = """在开发过程中，参考了以下技术分享：\n
tempfile 模块用法：
http://c.biancheng.net/view/2560.html
pygame 播放音乐用法：
https://www.cnblogs.com/ocean1100/p/9319891.html
requests 下载用法：
https://zhuanlan.zhihu.com/p/162965342
PyQt5 用法：
https://blog.csdn.net/AzureMouse/article/details/90338961
多线程与信号槽：
https://blog.csdn.net/qq_40784418/article/details/105398870\n
感谢所有人对 DictationNow! 的支持！"""
log =   """优化 架构调整
修复 播放时界面无响应
新增 最高 3 次重复播放
新增 版本日志"""

"""
TODO:
#0: 将音频统一保存到文件夹
#1: "关于"链接跳转
#2: 架构调整，将 media、FileType 整合为 tools 类
#3: 精简包体积
#4: 中文翻译播报
#5: 优化界面、添加 ICON
#6: 拼写测试
#7: 多语言听写支持
"""
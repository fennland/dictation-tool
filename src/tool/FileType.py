# -*- encoding: utf-8 -*-
'''
@File    :   FileType.py
@Time    :   2022/05/12 23:32:11
@Author  :   Fenn 
@Version :   1.0.1a
@Contact :   realHifenn@outlook.com
'''

# here put the import lib
import struct

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

# 来源：https://blog.csdn.net/wanglb465/article/details/124493878
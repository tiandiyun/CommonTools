# -*- coding:utf8 -*-

import os
import codecs
import chardet


def ConvertBytesToUtf8(bytes, encoding=''):
    def __GetEncoding(bytes):
        char_info = chardet.detect(bytes)
        ec = char_info['encoding']
        return ec

    if not encoding:
        encoding = __GetEncoding(bytes)
        if encoding.lower() == 'gb2312':
            encoding = 'gbk'

    return bytes.decode(encoding), encoding


def ReadFileWithUtf8(file_path):
    try:
        with codecs.open(file_path, mode='rb') as fp:
            lines = fp.readlines()

            encoding = ''
            for idx, line in enumerate(lines):
                try:
                    line, encoding = ConvertBytesToUtf8(line, encoding)
                except:
                    line, encoding = ConvertBytesToUtf8(line, '')
                lines[idx] = line

        return lines, encoding

    except Exception as e:
        print(e, file_path)
        return None, None


def TryGetEncoding(file):
    try:
        with open(file, 'rb') as fp:
            char_info = chardet.detect(fp.read())
            ec = char_info['encoding']
            return ec
    except Exception as e:
        print(e)


def ReadLines(file, ec=None):
    if not ec:
        ec = TryGetEncoding(file)

    try:
        with open(file, 'r', encoding=ec) as fp:
            return fp.readlines()
    except Exception as e:
        print(e, file)
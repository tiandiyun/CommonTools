# -*- coding:utf8 -*-

import os
import re
import time
import codecs
import chardet
import argparse

class FileCheck:

    __counting_time = 0

    @classmethod
    def FindLogError(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument("dir", help="input a directory")
        args = parser.parse_args()
        if not args.dir:
            return

        for dir, subList, files in os.walk(args.dir):
            # print(dir, subList, files)
            for file in files:
                _, ext = os.path.splitext(file)
                if ext == '.log' and file.find('Gate') >= 0:
                    file_path = os.path.join(dir, file)

                    cls.__StartCounting()
                    cls.__FindError(file_path)
                    cls.__EndCounting('Check file <<{}>> cost time:   '.format(file))


    @classmethod
    def __FindError(cls, file_path):

        def __GetEncoding(bytes):
            char_info = chardet.detect(bytes)
            ec = char_info['encoding']
            return ec

        try:
            with codecs.open(file_path, mode='rb') as fp:
                lines = fp.readlines()

            ec = None
            for line in lines:
                if not ec:
                    ec = __GetEncoding(line)

                try:
                    str_data = line.decode(ec)
                except:
                    ec = __GetEncoding(line)
                    str_data = line.decode(ec)

                result = re.search(r".*FATAL.*", str_data, re.IGNORECASE)
                if result:
                    print(result.group(0))

        except Exception as e:
            print(e, file_path)

    @classmethod
    def __StartCounting(cls, info=None):
        cls.__counting_time = time.time()
        if info:
            print(info, cls.__counting_time)

    @classmethod
    def __EndCounting(cls, info=None):
        tm = time.time()
        dt = tm - cls.__counting_time

        if info:
            print(info, dt)
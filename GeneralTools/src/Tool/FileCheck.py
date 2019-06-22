# -*- coding:utf8 -*-

import os
import re
import time
import codecs
import chardet
import argparse
import shutil


class FileCheck:
    __counting_time = 0

    @classmethod
    def FindLogError(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument("-sd", "--search_dir", help="missing path to search")
        parser.add_argument("-fp", "--file_pattern", default="*")
        parser.add_argument("-kp", "--key_pattern", help="missing key words pattern for searching")
        args = parser.parse_args()
        if not args.search_dir:
            return

        file_pattern = args.file_pattern if args.file_pattern else '*'
        rr = re.compile(file_pattern, re.IGNORECASE)
        for dir, subList, files in os.walk(args.search_dir):
            for file in files:
                if rr.search(file):
                    src_path = os.path.join(dir, file)
                    cls.__StartCounting()
                    cls.__FindError(src_path, args.key_pattern)
                    cls.__EndCounting('Check file <<{}>> cost time:   '.format(file))


    @classmethod
    def __FindError(cls, src_path, key_pattern):

        def __GetEncoding(bytes):
            char_info = chardet.detect(bytes)
            ec = char_info['encoding']
            return ec

        try:
            rr = re.compile(key_pattern, re.IGNORECASE)

            with codecs.open(src_path, mode='rb') as fp:
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

                result = rr.search(str_data)
                if result:
                    print(str_data)
                    # print(result.group(0))

        except Exception as e:
            print(e, src_path)


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


    @classmethod
    def CheckFilesStat(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument("-sd", "--search_dir", help="missing path to search")
        args = parser.parse_args()

        checkDirName = 'NewFishBuild'  # 'trunk'
        bakDir = None
        idx = args.search_dir.find(checkDirName)
        if idx >= 0:
            chkDir = args.search_dir[:idx]
            bakDir = os.path.join(chkDir, checkDirName + '_bak')
            os.chdir(os.path.join(chkDir, checkDirName))

        now_time = time.time()
        for mainDir, subList, files in os.walk('.'):
            for file in files:
                src_path = os.path.join(mainDir, file)
                statinfo = os.stat(src_path)
                if statinfo.st_mtime > now_time:
                    print(src_path)

                    if bakDir:
                        bakSubDir = os.path.join(bakDir, mainDir)
                        if not os.path.isdir(bakSubDir):
                            os.makedirs(bakSubDir)

                        dst_path = os.path.join(bakSubDir, file)
                        shutil.move(src_path, dst_path)

# -*- coding:utf8 -*-

import os
import re
import time
import codecs
import chardet
import random
import argparse
import shutil

random.seed(time.time())

def SelectNameFromFile():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="input a name file", required=True)
    parser.add_argument("-c", "--count", help="input count to select", required=True)
    parser.add_argument("-ds", "--delete_source", help="delete the name from source", action="store_true", default=False)
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        return

    selectList = []
    with open(args.file, 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        count = min(int(args.count), len(lines))
        for i in range(count):
            idx = random.randrange(0, len(args.count))
            selectList.append(lines[idx])
            del(lines[idx])

        f.seek(0)
        f.truncate()

    _, srcFile = os.path.split(args.file)
    srcName, srcExt = os.path.splitext(srcFile)
    outputFile = os.path.join(os.path.dirname(args.file), srcName + '_output' + srcExt)
    with open(outputFile, 'w', encoding='utf-8') as f:
        f.writelines(selectList)
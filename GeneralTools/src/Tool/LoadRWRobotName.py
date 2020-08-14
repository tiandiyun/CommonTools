# -*- coding:utf8 -*-

import os
import re
import time
import random
import argparse
from Util.CommonFunction import ReadLines

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


def ImportRobot(importFile, itemsCount, partsCount):
    if not os.path.isfile(importFile):
        print('not found file: ' + importFile)
        return

    _, fileName = os.path.split(importFile)
    name, tail = os.path.splitext(fileName)

    exportFiles = {}
    exportDir = os.path.dirname(importFile)

    lines = ReadLines(importFile, 'ansi')
    linesCount = len(lines)
    splitParts = (linesCount + itemsCount - 1) / itemsCount
    parts = min(splitParts, partsCount)

    for pi in range(parts):
        exportPath = os.path.join(exportDir, name + '_30' + str(pi + 1) + tail)
        exportFiles[exportPath] = lines[pi * itemsCount : min((pi + 1) * itemsCount, linesCount)]

    pattern = re.compile('(\d+?)(\s{4})(.*)(\n|\r\n)')
    for path, lines in exportFiles.items():
        if os.path.isfile(path):
            os.remove(path)

        with open(path, 'w', encoding='utf-8') as fp:
            fp.write('ID\tName\tFaceID\n')
            for l in lines:
                newL = pattern.sub(r'\1\t\3\t100\4', l)
                fp.write(newL)
            print('Export success: ' + path)

    print('Done !!')

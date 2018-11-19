# -*- coding:utf8 -*-

import os
import re
import sys
import codecs
import shutil
import zipfile
import argparse
from Util.CommonFunction import ReadFileWithUtf8


__SRC_OBJ_NAME = 'RoomTemplate'
__SRC_MACRO_DEFINITION = 'ROOM_TEMPLATE'


def UnZipFile(zipFile, dstDir, quietly=False):
    if not os.path.isfile(zipFile):
        print('Zip File %s is not exists' % zipFile)
        return False

    if os.path.isdir(dstDir):
        if not quietly:
            print('The destination directory is exists, will you delete it ?')
            inputStr = input().lower()
            if inputStr == 'y' or inputStr == 'yes':
                shutil.rmtree(dstDir)
            else:
                return False
        else:
            shutil.rmtree(dstDir)

    print("Unzip files to " + dstDir)
    with zipfile.ZipFile(zipFile, "r") as srcZip:
        for srcFile in srcZip.namelist():
            print("\t" + srcFile)

            dstFile = os.path.normpath(os.path.join(dstDir, srcFile))
            subDir = os.path.dirname(dstFile)
            if not os.path.exists(subDir):
                os.makedirs(subDir)

            with open(dstFile, "wb") as fd:
                fd.write(srcZip.read(srcFile))

    return True


def RenameFilesName(projDir, appName):
    def TryRenameFD(dir, srcObj, appName):
        srcExt = ''
        if os.path.isfile(os.path.join(dir, srcObj)):
            srcName, srcExt = os.path.splitext(srcObj)
        else:
            srcName = srcObj

        if srcName.find(__SRC_OBJ_NAME) >= 0:
            dstName = srcName.replace(__SRC_OBJ_NAME, appName)
            if dstName != srcName:
                dstObj = dstName + srcExt
                shutil.move(os.path.join(dir, file), os.path.join(dir, dstObj))
                print('\t' + srcObj + ' -> ' + dstObj)

    print('\nRename files name with "%s"' % appName)
    if not os.path.isdir(projDir):
        print('directory is not exists')
        return True

    for dir, subList, files in os.walk(projDir):
        parentDir, dirName = os.path.split(dir)
        TryRenameFD(parentDir, dirName, appName)

        for file in files:
            TryRenameFD(dir, file, appName)

    return True


def ModifyFiles(projDir, appName, projName=''):
    print('\nModfiy files with "%s"' % appName)

    if not os.path.isdir(projDir):
        print('directory is not exists')
        return False

    # 修改文件中的宏定义和字段名
    if not projName:
        projName = appName

    checkList = ['.h', '.cpp', '.vcxproj', '.filters']
    vcxprojFile = '%s.vcxproj' % appName
    for dir, subList, files in os.walk(projDir):
        for file in files:
            fileName, ext = os.path.splitext(file)
            filePath = os.path.join(dir, file)
            if ext in checkList:
                lines, encoding = ReadFileWithUtf8(filePath)
                if not lines:
                    print('Read file error : ' + filePath)
                    continue

                for idx, line in enumerate(lines):
                    if file == vcxprojFile:
                        line = re.sub(r'(<ProjectName>)(.*)(</ProjectName>)', r'\1%s\3' % projName, line) # 修改工程名
                    line = re.sub(__SRC_MACRO_DEFINITION, appName.upper(), line) # 替换宏定义
                    line = re.sub(__SRC_OBJ_NAME, appName, line)    #替换类名和变量名
                    lines[idx] = line

                with codecs.open(filePath, mode='wb', encoding=encoding) as fd:
                    fd.writelines(lines)

    return True


def CreateNewRoom():
    parser = argparse.ArgumentParser()
    parser.add_argument("app_name", help="the application name")
    parser.add_argument('-t', '--template', help='the project as a template', required=False)
    parser.add_argument('-o', '--output_dir', help='the new project directory', required=False)
    parser.add_argument('-p', '--project', help='project name in the file which name with *.vcxproj', required=False)
    parser.add_argument('-q', '--quietly', help='delete it while the file is exists', action='store_true')
    args = parser.parse_args()

    projDir = os.path.realpath(os.path.join(sys.path[0], os.path.pardir))
    dataDir = os.path.join(projDir, 'data')

    if not args.template:
        template = os.path.join(dataDir, __SRC_OBJ_NAME + '.zip')
    else:
        template = args.template

    if not args.output_dir:
        outDir = os.path.join(os.path.dirname(template), args.app_name)
    else:
        outDir = args.output_dir

    r = UnZipFile(template, outDir, args.quietly)
    if not r:
        print('UnZipFile failed')
        return False

    r = RenameFilesName(outDir, args.app_name)
    if not r:
        print('RenameFilesName failed')
        return False

    r = ModifyFiles(outDir, args.app_name, args.project)
    if not r:
        print('ModifyFiles failed')
        return False

    return True


# -*- coding:utf8 -*-

import sys
sys.path.append(sys.path[0])

from Test.TestArgparse import TestArgparse
from Tool.FileCheck import FileCheck
from Tool.ProjectManager import CreateNewRoom
from Tool.LoadRWRobotName import SelectNameFromFile, ImportRobot
from Tool.Xls2Xml import ConvertXlsToXml

if __name__ == "__main__":

    if len(sys.argv) < 2:
        sys.exit(0)

    cmd = sys.argv[1]
    del sys.argv[1]

    if cmd == 'Test':
        TestArgparse()
    elif cmd == 'CheckFile':
        FileCheck.FindLogError()
    elif cmd == 'CreateRoom':
        CreateNewRoom()
    elif cmd == 'CheckStat':
        FileCheck.CheckFilesStat()
    elif cmd == 'SelectNameFromFile':
        SelectNameFromFile()
    elif cmd == 'ImportRobot':
        ImportRobot(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
        # ImportRobot(r'E:\Project\Python\GeneralTools\data\id.txt', 1000, 2)
    elif cmd == 'Xls2Xml':
        ConvertXlsToXml()
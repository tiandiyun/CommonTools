# -*- coding:utf8 -*-

import os
import sys
import xlrd
import argparse
from xml.etree.ElementTree import Element, SubElement, ElementTree


class XlsItemColumn:
    def __init__(self):
        self.name = ''
        self.desc = ''
        self.type = ''
        self.values = []

    def ParseValue(self, strV):
        strT = self.type.lower()
        if strT == 'int':
            return int(strV)
        elif strT == 'float' or strT == 'double':
            return float(strV)
        elif strT == 'string':
            return self.ParseString(strV)
        else:
            return strV

    def ParseString(self, strV):
        if strV.find('/') > 0:
            return strV.split('/')
        else:
            return strV


def LoadXls(xlsPath):
    if not os.path.isfile(xlsPath):
        print('not found "%s"' % xlsPath)
        return

    reader = xlrd.open_workbook(xlsPath)
    sheetSize = len(reader.sheets())
    print('Size of sheets is ' + str(sheetSize))

    # 获取sheet
    sheetIdx = 0
    sheet = reader.sheet_by_index(sheetIdx)  # 索引的方式，从0开始
    # sheet = readbook.sheet_by_name('sheet2')  # 名字的方式

    print('rows: %d, cols: %d of sheet %d' % (sheet.nrows, sheet.ncols, sheetIdx))
    if sheet.ncols < 2:
        print('cols smaller than 2')
        return


    titles = []
    for col in range(sheet.ncols):
        values = sheet.col_values(col)
        item = XlsItemColumn()
        item.desc = values[0]
        item.name = values[1]
        item.type = values[2]
        titles.append(item)

    xlsData = []
    for row in range(5, sheet.nrows):
        values = sheet.row_values(row)
        item = {}
        for i, v in enumerate(values):
            title = titles[i]
            k = title.name
            item[k] = title.ParseValue(v)
        xlsData.append(item)

    return xlsData


def SplitXlsItems(item):
    attr = {}
    children = {}
    for key, value in item.items():
        if isinstance(value, list):
            children[key] = value
        else:
            attr[key] = str(value)
    return attr, children


# 增加换行符
def FormatXmlWithIndent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            FormatXmlWithIndent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def SaveXml(xlsData, xmlPath):
    root = Element('root')
    for item in xlsData:
        attr, children = SplitXlsItems(item)
        child = SubElement(root, "item", attr)
        for key, value in children.items():
            if isinstance(value, list):
                subChild = SubElement(child, key, {})
                for subItem in value:
                    SubElement(subChild, "item", {'value' : str(subItem)})
            else:
                value = str(value)
                child.set(key, value)

    FormatXmlWithIndent(root)
    tree = ElementTree(root)
    tree.write(xmlPath, encoding="utf-8",xml_declaration=True,)


def ConvertXlsToXml():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", help="enter source xls file", required=True)
    parser.add_argument("-d", "--destination", help="enter destination xml file")
    args = parser.parse_args()

    if not os.path.isfile(args.source):
        print('not found source xls file')
        return
    xlsPath = args.source

    if not args.destination:
        xlsDir, xlsFile = os.path.split(xlsPath)
        xlsName, _ = os.path.splitext(xlsFile)
        xmlPath = os.path.join(xlsDir, xlsName+".xml")
    else:
        xmlPath = args.destination

    xlsData = LoadXls(xlsPath)
    if not xlsData:
        return

    SaveXml(xlsData, xmlPath)
    print("Convert success : " + xmlPath)



# if __name__ == "__main__":
#     xlsPath = r'E:\Work\py3d\design\游戏策划案\游乐园\一跳到底配置表\JumpDownLevelConfig.xlsx'
#     xmlPath = r'E:\Work\py3d\design\游戏策划案\游乐园\一跳到底配置表\JumpDownLevelConfig.xml'
#     xlsData = LoadXls(xlsPath)
#     SaveXml(xlsData, xmlPath)
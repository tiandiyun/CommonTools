#-*- coding:utf8 -*-

import os, sys
import xlrd
from collections import OrderedDict

if __name__ == "__main__":

    if len(sys.argv) == 3:
        excelPath = sys.argv[1]
        txtPath = sys.argv[2]
    else:
        excelPath = r'E:\Work\FishGame\File\虚拟卡\VirtualCard.xlsx'
        txtPath = r'E:\Work\FishGame\File\虚拟卡\VirtualCard.txt'

    if not os.path.isfile(excelPath):
        print('not found "%s"' % excelPath)
        sys.exit()

    # 获取数据
    readbook = xlrd.open_workbook(excelPath)

    sheetSize = len(readbook.sheets())
    print('Size of sheets is ' + str(sheetSize))

    sheetIdx = 0

    # 获取sheet
    sheet = readbook.sheet_by_index(sheetIdx)  # 索引的方式，从0开始
    # sheet = readbook.sheet_by_name('sheet2')  # 名字的方式

    print('rows: %d, cols: %d of sheet %d' % (sheet.nrows, sheet.ncols, sheetIdx))
    if sheet.ncols < 2:
        print('cols smaller than 2')
        sys.exit()

    # # 获取一行的数值，例如第5行
    # rowvalue = sheet.row_values(5)
    #
    # # 获取一列的数值，例如第6列
    # col_values = sheet.col_values(1)
    #
    # # 获取一个单元格的数值，例如第5行第6列
    # cell_value = sheet.cell(5, 1).value

    rawData = OrderedDict()
    for rowIndex in range(sheet.nrows):
        rowValue = sheet.row_values(rowIndex)
        if rowValue[0] in rawData:
            print('repeated: ' + str(rowValue))
            break
        rawData[rowValue[0]] = rowValue[1]


    with open(txtPath, 'r+') as f:
        lines = f.readlines()
        for l in lines:
            pass
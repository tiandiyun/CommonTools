# -*- coding:utf8 -*-

import os, sys
import xlrd
from collections import OrderedDict

if __name__ == "__main__":

	if len(sys.argv) == 4:
		excelPath = sys.argv[1]
		txtPath = sys.argv[2]
		itemType = sys.argv[3]
	else:
		excelPath = r'E:\Work\FishGame\File\虚拟卡\VirtualCard.xlsx'
		txtPath = r'E:\Work\FishGame\File\虚拟卡\VirtualCard.txt'
		# excelPath = r'D:\Work\Project\Python\CommonTools\虚拟卡\VirtualCard.xlsx'
		# txtPath = r'D:\Work\Project\Python\CommonTools\虚拟卡\VirtualCard.txt'
		itemType = None

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

		key = rowValue[0]
		if key[-1] == ',':
			key = key[:-1]

		if key in rawData:
			print('repeated: ' + str(key))
			break
		rawData[key] = rowValue[1]


	mode = 'r+' if os.path.isfile(txtPath) else 'w+'
	with open(txtPath, mode) as f:
		lines = f.readlines()
		f.seek(0, os.SEEK_END)

		if len(lines) > 0:
			l = lines[-1]
			items = l.split()
			lastId = int(items[0])

			if itemType == None:
				itemType = items[1]
		else:
			lastId = 10000

			# if itemType == None:
			# 	itemType = 0

			title = 'ID\tType\tAccount\tPassword\tCredence\tState\n'
			f.write(title)


		for k, v in rawData.items():
			lastId += 1
			strLine = '%(id)d\t%(type)s\t%(account)s\t%(password)s\t%(credence)s\t1\n' % {
				'id': lastId, 'type': itemType, 'account': k, 'password': v, 'credence': 0}
			f.write(strLine)

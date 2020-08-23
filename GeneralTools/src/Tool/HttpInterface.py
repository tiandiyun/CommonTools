# -*- coding:utf8 -*-

import sys
sys.path.append(sys.path[0])

import json
import requests


def GetPhpAgent():
	header = {}
	header['p_pradar_traceid'] = '112211'
	header['Proxy-Client-IP'] = '10.1.3.47'
	header['X-Forwarded-For'] = '192.168.1.5'
	return requests.get('http://localhost:8900/work/phptest/main.php', headers=header)


if __name__ == "__main__":

	result = GetPhpAgent()
	print(result.text)

	# result = requests.get('http://jsonip.com')
	# ipInfo = json.loads(result.text)
	# print(ipInfo['ip'])


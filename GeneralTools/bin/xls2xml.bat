@echo off

goto desc
	%~dp0: 当前文件目录;
	%~dp1: 引入文件目录
	%~nx1: 文件全名;
	%~n1: 文件名; 
	%~x1: 扩展名
:desc

D:\Tools\Python37\python.exe %~dp0..\src\Main.py Xls2Xml -s %~dp1%~nx1

rem cd %~dp0
rem ImportRobot.exe -f %~dp1%~nx1 -i 1000 -p 2

pause
import win32com.client

import pywinauto
from pywinauto import findwindows
import time
import os

os.system('taskkill /IM coStarter* /F /T')
# 해당 인수는 '이미지명이 coStarter로 시작하는 프로세스를 강제로(/F) 종료하라(/T)는 뜻.'

os.system('taskkill /IM CpStart* /F /T')
os.system(r'wmic process where "name like \'%coStarter%\'" call terminate')
# wimc는 윈도우 시스템 정보를 조회하거나 변경할 때 사용하는 명령어.
# 크레온 프로그램은 강제 종료 신호를 받으면 확인 창을 띄우기 때문에 강제로 한 번 더 프로세스를 종료해야 한다.

os.system(r'wmic process where "name like \'%CpStart%\'" call terminate')
time.sleep(5)

app = pywinauto.Application()
app.start(r'C:\DAISHIN\STARTER\ncStarter.exe /prj:cp /id:**** /pwd:**** /pwdcert:**** /autostart')
# pywinauto를 이용하여 크레온 프로그램(coStarter.exe)을 크레온 플러스 모드(/prj:cp)로 자동으로 시작한다.
time.sleep(60)
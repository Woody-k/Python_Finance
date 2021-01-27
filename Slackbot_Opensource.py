import win32com.client

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

# 현재가 객체 구하기
objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")
objStockMst.SetInputValue(0, 'A091990')  # 종목 코드 - 셀트리온헬스케어
objStockMst.BlockRequest()

# 현재가 통신 및 통신 에러 처리
rqStatus = objStockMst.GetDibStatus()
rqRet = objStockMst.GetDibMsg1()
print("통신상태", rqStatus, rqRet)
if rqStatus != 0:
    exit()

# 현재가 정보 조회
name = objStockMst.GetHeaderValue(1)  # 종목명
cprice = objStockMst.GetHeaderValue(11)  # 종가
diff = objStockMst.GetHeaderValue(12)  # 대비
open = objStockMst.GetHeaderValue(13)  # 시가
high = objStockMst.GetHeaderValue(14)  # 고가
low = objStockMst.GetHeaderValue(15)  # 저가
vol = objStockMst.GetHeaderValue(18)  # 거래량

# 셀트리온헬스케어 차트
attach01_dict = {
    'color': '#ff0000',
    'author_name': "Today's Stock Market",
    'autohr_link': 'github.com/Woody-k',
    'title': "셀트리온헬스케어(091990)",
    'title_link': 'https://finance.naver.com/item/main.nhn?code=091990',
    'image_url': 'https://ssl.pstatic.net/imgfinance/chart/item/area/day/091990.png?sidcode=1611684736546',
}

attach01_list = [attach01_dict]

# KOSDAQ 지수
attach_dict = {
    'color': '#ff0000',
    'author_name': "Today's Stock Market",
    'autohr_link': 'github.com/Woody-k',
    'title': "KOSDAQ Index",
    'title_link': 'https://finance.naver.com/',
    'image_url': 'https://ssl.pstatic.net/imgfinance/chart/main/KOSDAQ.png?sidcode=1611684420449',
}

attach_list = [attach_dict]

from slacker import Slacker

slack = Slacker('<your-slack-api-token-goes-here>')

# Send a message to #general channel
slack.chat.post_message('#general', name)
slack.chat.post_message('#general', '종가: ' + str(cprice))
slack.chat.post_message('#general', '전일대비: ' + str(diff))
slack.chat.post_message('#general', '시가: ' + str(open))
slack.chat.post_message('#general', '고가: ' + str(high))
slack.chat.post_message('#general', '저가: ' + str(low))
slack.chat.post_message('#general', '거래량: ' + str(vol))

slack.chat.post_message('#general', attachments=attach01_list)
slack.chat.post_message('#general', attachments=attach_list)
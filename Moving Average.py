# 2. NAVER(035420) Candle Chart + Moving Average

import pandas as pd
import requests
from bs4 import BeautifulSoup
import mplfinance as mpf

# 맨 뒤 페이지 숫자 구하기
url = 'https://finance.naver.com/item/sise_day.nhn?code=035420&page=1'
with requests.get(url) as doc:
    html = BeautifulSoup(requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text, "lxml")
    pgrr = html.find('td', class_='pgRR')
    s = str(pgrr.a['href']).split('=')
    last_page = s[-1]

# 전체 페이지 읽어오기
df = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=035420'
for page in range(1, int(last_page)+1):
    page_url = '{}&page={}'.format(sise_url, page)
    df = df.append(pd.read_html(requests.get(page_url, headers={'User-agent': 'Mozilla/5.0'}).text)[0])

# 차트 출력을 위해 데이터프레임 가공하기
df = df.dropna()
df = df.iloc[0:180] # 행을 나타냄. 즉, 180 거래일.
df = df.rename(columns={'날짜':'Date', '시가':'Open', '고가':'High', '저가':'Low', '종가':'Close', '거래량':'Volume'})
df = df.sort_values(by='Date') # 'naver_finance' 종가 정보는 내림차순으로 되어 있으므로, 오름차순으로 변경.
df.index = pd.to_datetime(df.Date)
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

# mplfinance cancle chart 그리기
# mpf.plot(df, title='NAVER(035420) candle chart', type='candle')
# mpf.plot(df, title='NAVER(035420) ohlc chart', type='ohlc'). Totally, in the USA, use the ohlc instead of the candle.

# 아래 코드로, 캔들색상 변경, 거래량 추가, 이동평균성 지정 가능.
# kwargs는 keyword arguments의 약자이며, mpf.plot() 함수를 호출할 때 쓰이는 여러인수를 담는 Dictionary.

kwargs = dict(title="NAVER(035420) daily's chart ", type='candle',
    mav=(20, 60, 120), volume=True, show_nontrading=True)
# Moving Average: [Blue = '20', Yellow = '60', Green = '120']
# Non-trading days can be displayed with the 'show_nontrading' keyword.
mc = mpf.make_marketcolors(up='r', down='b', inherit=True) # 양봉, 음봉 color 지정.
s  = mpf.make_mpf_style(marketcolors=mc)
mpf.plot(df, **kwargs, style=s)
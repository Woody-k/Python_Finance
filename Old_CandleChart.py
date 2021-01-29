# 2. NAVER(035420) Old Candle Chart.

import pandas as pd
import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
#from mpl_finance import candlestick_ohlc
from mplfinance.original_flavor import candlestick_ohlc
from datetime import datetime

url = 'https://finance.naver.com/item/sise_day.nhn?code=035420&page=1'
with requests.get(url) as doc:
    html = BeautifulSoup(requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text, "lxml")
    pgrr = html.find('td', class_='pgRR')
    s = str(pgrr.a['href']).split('=')
    last_page = s[-1]

df = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=035420'
for page in range(1, int(last_page)+1):
    page_url = '{}&page={}'.format(sise_url, page)
    df = df.append(pd.read_html(requests.get(page_url, headers={'User-agent': 'Mozilla/5.0'}).text)[0])

df = df.dropna()
df = df.iloc[0:20]
df = df.sort_values(by='날짜')
for idx in range(0, len(df)):
    dt = datetime.strptime(df['날짜'].values[idx], '%Y.%m.%d').date()
    # 날짜 칼럼의 %Y.%m.%d 형식 문자열을 datetime 형으로 변환한다.
    df['날짜'].values[idx] = mdates.date2num(dt)
    # 시간데이터를 매번 float 형으로 변경해야한다. Why? time 은 반드시 float 형으로 넘겨줘야 하기 떄문.
ohlc = df[['날짜','시가','고가','저가','종가']]

plt.figure(figsize=(9, 6))
ax = plt.subplot(1, 1, 1)
plt.title('NAVER(035420)')
candlestick_ohlc(ax, ohlc.values, width=0.7, colorup='red', colordown='blue')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)
plt.grid(color='gray', linestyle='--')
plt.show()
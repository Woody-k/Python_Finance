# 1. NAVER(035420) 종가차트
# 미국에서는 OHLC 차트를 사용하지만, 국내는 캔들 차트를 사용한다. (양/음봉)

import pandas as pd
import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt

url = f"https://finance.naver.com/item/sise_day.nhn?code=035420&page=1"
with requests.get(url) as doc:
    html = BeautifulSoup(requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text, "lxml")
    pgrr = html.find('td', class_='pgRR')
    s = str(pgrr.a['href']).split('=')
    last_page = s[-1]

df = pd.DataFrame()
sise_url = f"https://finance.naver.com/item/sise_day.nhn?code=035420"
for page in range(1, int(last_page)+1):
    page_url = '{}&page={}'.format(sise_url, page)
    df = df.append(pd.read_html(requests.get(page_url, headers={'User-agent': 'Mozilla/5.0'}).text)[0])

df = df.dropna()
df = df.iloc[0:20] # 행을 나타냄. 즉, 20 거래일.
df = df.sort_values(by='날짜') # 'naver_finance' 종가 정보는 내림차순으로 되어 있으므로, 오름차순으로 변경.

plt.title('NAVER (close)')
plt.xticks(rotation=45) # X축 레이블의 날짜가 겹쳐셔 보기에 어려우므로 45도로 회전하여 표시한다.
plt.plot(df['날짜'], df['종가'], 'co-')
plt.grid(color='gray', linestyle='--')
plt.show()
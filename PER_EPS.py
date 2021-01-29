import win32com.client

# Create Object
instMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")

# SetInputValue
instMarketEye.SetInputValue(0, (4, 67, 70, 111))
instMarketEye.SetInputValue(1, 'A035420')

# BlockRequest
instMarketEye.BlockRequest()

# GetData
Price = instMarketEye.GetDataValue(0, 0)
PER = instMarketEye.GetDataValue(1, 0)
EPS = instMarketEye.GetDataValue(2, 0)
Month_year = instMarketEye.GetDataValue(3, 0)

# Create Object_01
objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")

# SetInputValue_01
objStockMst.SetInputValue(0, 'A035420')

# BlockRequest_01
objStockMst.BlockRequest()

# GetData_01
name = objStockMst.GetHeaderValue(1)

from slacker import Slacker
slack = Slacker('<your-slack-api-token-goes-here>')

# Send a message to #general channel
slack.chat.post_message('#general', name)

slack.chat.post_message('#general', '현재가: ' + str(Price))
slack.chat.post_message('#general', '최근분기(년월): ' + str(Month_year))
slack.chat.post_message('#general', 'PER(배): ' + str(PER))
slack.chat.post_message('#general', 'EPS(원): ' + str(EPS))
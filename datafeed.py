import time

import backtrader as bt
import datetime
import akshare as ak
import okx.MarketData as okmd
import okx.PublicData as okpd
import pandas as pd

dtype_dict = {'代码': str}

df = pd.read_csv('datasource/stock/a_stock_list.csv', dtype=dtype_dict)
ddf = pd.DataFrame()
for index, row in df.iterrows():
    symbol = f"{row['代码']}"
    print(f"{index} {symbol}")
    ddd = ak.stock_individual_info_em(symbol=symbol)
    ddd = ddd.T
    ddd.columns = ["股票代码", "股票简称", "总股本", "流通股", "总市值", "流通市值", "行业", "上市时间"]
    ddd.drop('item', inplace=True)
    ddf = pd.concat([ddf, ddd], ignore_index=True)

ddf.to_csv('datasource/stock_info/stock_list.csv', index=False)
# ddf = ak.stock_zh_a_hist(symbol=symbol, start_date='20240101')
# ddf.to_csv(f"datasource/stock/his_{symbol}.csv")
# df = ak.stock_zh_a_spot_em()
# df.to_csv('datasource/stock/a_stock_list.csv',index=False)
# ak.fund_etf_spot_em().to_csv('stocks.csv')
# ak.stock_zh_a_hist(symbol='600845').to_csv('600845.csv', index=False)

# def get_history_candlesticks(before='', after=''):
#     marketAPI = okmd.MarketAPI(flag='0')
#     for i in range(5):
#         try:
#             resp = marketAPI.get_history_candlesticks(instId='DOGE-USDT', bar='1H', before=before, after=after)
#             if resp['code'] != '0':
#                 time.sleep(1)
#                 continue
#             return resp
#         except Exception as e:
#             print(f"发生了一个异常: {e}")
#             time.sleep(1)
#             continue
#     raise RuntimeError("retry exhausted")


# publicAPI = okpd.PublicAPI()
# resp = publicAPI.get_instruments(instType='SPOT')
# df = pd.DataFrame(resp['data'])
# df.to_csv('okx_instruments.csv', index=False)

# 获取2021年1月1日至今的15分钟K线数据
# resp = get_history_candlesticks()
# df = pd.DataFrame(resp['data'])
# while len(resp['data']) > 0:
#     ts = resp['data'][-1][0]
#     resp = get_history_candlesticks(after=ts, before='1640966400000')
#     df = pd.concat([df, pd.DataFrame(resp['data'])])
# #
# df.to_csv('doge_usdt_1H.csv', index=False)
#
# def timestamp_to_datetime_millis(timestamp_millis):
#     """
#     将Unix时间戳（毫秒为单位）放大转换为'YYYY-MM-DD HH:MM:SS'格式的日期时间字符串
#     """
#     timestamp_seconds = timestamp_millis / 1000.0
#     dt = datetime.datetime.fromtimestamp(timestamp_seconds)
#     return dt.strftime('%Y-%m-%d %H:%M:%S')
#
#
# df = pd.read_csv('doge_usdt_1H.csv')
# df = df.sort_values(by='0', ascending=True)
# df['0'] = df['0'].apply(timestamp_to_datetime_millis)
# df.columns = ['ts', 'open', 'high', 'low', 'close', 'volume', 'volCcy', 'volCcyQuote', 'confirm']
# df.to_csv('doge_usdt_1H_formated.csv', index=False)

import pandas as pd
import datetime


class Stock:

    def __init__(self):
        self.symbol = ""
        self.name = ""
        self.start_date = None
        self.data = None


def load_stock_data(symbol):
    dtype_dict = {'日期': str}
    df = pd.read_csv(f"datasource/stock/his_{symbol}.csv", dtype=dtype_dict)
    return df


def get_stock_list():
    list = []
    dtype_dict = {'股票代码': str}
    df = pd.read_csv('datasource/stock_info/stock_list.csv', dtype=dtype_dict)
    for index, row in df.iterrows():
        s = Stock()
        s.symbol = row['股票代码']
        s.name = row['股票简称']
        if row['上市时间'] != '-':
            s.start_date = datetime.datetime.strptime(row['上市时间'], "%Y%m%d")
        s.data = load_stock_data(s.symbol)
        print(f"{index} load stock {s.symbol}")
        if s.data.empty:
            continue
        list.append(s)
    return list


# 科创板
def filter_kcb_stocks(stock_list):
    return [stock for stock in stock_list if stock.symbol[0] != '4' and stock.symbol[0] != '8']


def filter_new_stocks(stock_list, date):
    return [stock for stock in stock_list if stock.start_date is not None and (date - stock.start_date).days >= 250]


def filter_st_stock(stock_list):
    return [stock for stock in stock_list if 'ST' not in stock.name]


def filter_paused_stock(stock_list):
    return stock_list


def get_limit_up_down_stocks(stock_list, date):
    list = []
    datestr = date.strftime("%Y-%m-%d")
    for stock in stock_list:
        rows = stock.data[(stock.data['日期'] == datestr) & (stock.data['涨跌幅'] >= 10)]
        if not rows.empty:
            list.append(stock)
    return list

def get_limit_up_count_df(stock_list, date, days):
    

list = get_stock_list()
list = filter_kcb_stocks(list)
list = filter_new_stocks(list, datetime.datetime.now())
list = filter_st_stock(list)
list = get_limit_up_down_stocks(list, datetime.datetime.now())
print(len(list))

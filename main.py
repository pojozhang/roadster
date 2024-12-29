# 这是一个示例 Python 脚本。
import datetime

# 按 ⌃R 执行或将其替换为您的代码。
# 按 双击 ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。
import pandas as pd
import os as os

import backtrader as bt
import backtrader.feeds as btfeeds
from strategy.ma import SimpleMAStrategy
from strategy.ap import SimpleAPStrategy
from strategy.rsi import SimpleRSIStrategy
from strategy.boll import SimpleBollingerStrategy
from strategy.threema import ThreeMAStrategy
from data.ext import ExtendedCSVData


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 ⌘F8 切换断点。


def trade():
    # data = ExtendedCSVData(
    #     dataname='his.csv',
    #     fromdate=datetime.datetime(2024, 10,8 ),
    #     todate=datetime.datetime(2024, 11, 8),
    #     dtformat=('%Y-%m-%d %H:%M:%S'),
    #     tmformat=('%H.%M.%S'),
    #     nullvalue=0.0,
    #     timeframe=bt.TimeFrame.Minutes,
    #
    #     datetime=0,
    #     time=-1,
    #     high=3,
    #     low=4,
    #     open=1,
    #     close=2,
    #     volume=7,
    #     turnover=8,
    # )

    data = ExtendedCSVData(
        dataname='doge_usdt_30min_formated.csv',
        fromdate=datetime.datetime(2022, 1, 1),
        todate=datetime.datetime(2022, 12, 31),
        dtformat=('%Y-%m-%d %H:%M:%S'),
        tmformat=('%H.%M'),
        nullvalue=0.0,
        timeframe=bt.TimeFrame.Minutes,

        datetime=0,
        time=-1,
        high=2,
        low=3,
        open=1,
        close=4,
        volume=5,
        turnover=6,
    )

    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(SimpleRSIStrategy, stop_loss_percent=0.2,take_profit_percent=0.2)
    # cerebro.optstrategy(SimpleAPStrategy,
    #                     stop_loss_percent=[0.01, 0.02, 0.03, 0.04, 0.05, 0.07, 0.09, 0.1, 0.2, 0.3],
    #                     take_profit_percent=[0.03, 0.04, 0.05, 0.07, 0.09, 0.1, 0.2, 0.3, 0.5, 0.7])
    # cerebro.optstrategy(SimpleAPStrategy, period=[1050])
    # cerebro.addsizer(bt.sizers.FixedSize, stake=200000)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(0.001)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # cerebro.addanalyzer(bt.analyzers.DrawDown, _name="_DrawDown")
    # cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name="_AnnualReturn")
    # cerebro.addanalyzer(bt.analyzers.Returns, _name="_Returns", tann=252, timeframe=bt.TimeFrame.Minutes)

    results = cerebro.run()
    # for result in results:
    #     for strategy in result:
    #         print(
    #             f'stop_loss_percent: {strategy.params.stop_loss_percent},take_profit_percent: {strategy.params.take_profit_percent}, Final Value: {cerebro.broker.getvalue()}')
    #         print(f"收益率：{strategy.analyzers._Returns.get_analysis()['rtot'] * 100}%")
    #         print(f"最大回撤：{strategy.analyzers._DrawDown.get_analysis()['max']['drawdown']}%")
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot(style='candlestick',
            plotstyle = 'bar',  # 选择绘图样式
            figscale = 1.5,  # 增大图表比例
            barup = 'green',  # 上涨 K 线颜色
            bardown = 'red',  # 下跌 K 线颜色
            volume = True)

    # 按装订区域中的绿色按钮以运行脚本。

def trade_600845():
    data = ExtendedCSVData(
        dataname='600845.csv',
        fromdate=datetime.datetime(2024, 1, 1),
        todate=datetime.datetime(2024, 11, 8),
        dtformat=('%Y-%m-%d'),
        tmformat=('%H.%M'),
        nullvalue=0.0,

        datetime=0,
        time=-1,
        high=4,
        low=5,
        open=2,
        close=3,
        volume=6,
        turnover=7,
    )

    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(ThreeMAStrategy, stop_loss_percent=0.02,take_profit_percent=0.08,short_period=5,median_period=15,long_period=30)
    # cerebro.optstrategy(SimpleAPStrategy,
    #                     stop_loss_percent=[0.01, 0.02, 0.03, 0.04, 0.05, 0.07, 0.09, 0.1, 0.2, 0.3],
    #                     take_profit_percent=[0.03, 0.04, 0.05, 0.07, 0.09, 0.1, 0.2, 0.3, 0.5, 0.7])
    # cerebro.optstrategy(SimpleAPStrategy, period=[1050])
    cerebro.addsizer(bt.sizers.FixedSize, stake=1000)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(0.001)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name="_DrawDown")
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name="_AnnualReturn")
    cerebro.addanalyzer(bt.analyzers.Returns, _name="_Returns", tann=252, timeframe=bt.TimeFrame.Minutes)

    results = cerebro.run()
    # for result in results:
    #     for strategy in result:
    #         print(
    #             f'stop_loss_percent: {strategy.params.stop_loss_percent},take_profit_percent: {strategy.params.take_profit_percent}, Final Value: {cerebro.broker.getvalue()}')
    #         print(f"收益率：{strategy.analyzers._Returns.get_analysis()['rtot'] * 100}%")
    #         print(f"最大回撤：{strategy.analyzers._DrawDown.get_analysis()['max']['drawdown']}%")
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot(style='candlestick',
            plotstyle = 'bar',  # 选择绘图样式
            figscale = 1.5,  # 增大图表比例
            barup = 'green',  # 上涨 K 线颜色
            bardown = 'red',  # 下跌 K 线颜色
            volume = True)

    # 按装订区域中的绿色按钮以运行脚本。

if __name__ == '__main__':
    trade()

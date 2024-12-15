import backtrader as bt


class ExtendedCSVData(bt.feeds.GenericCSVData):
    # 指明成交额在CSV文件中的列位置（从0开始计数），这里假设是第6列
    lines = ('turnover',)
    params = (
        # 其他必要的参数设置，比如日期列位置、开盘价列位置等，以下是示例设置，按需调整
        ('dtformat', '%Y-%m-%d'),
        ('date', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('turnover', 6),
    )

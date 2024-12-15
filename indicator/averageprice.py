import backtrader as bt


class AveragePrice(bt.Indicator):
    lines = ('avg_price',)

    def __init__(self):
        self.total_turnover = 0.0
        self.total_volume = 0
        self.trade_date = None

    def next(self):
        trade_date = self.data.datetime.date(0)
        if self.trade_date == trade_date:
            self.total_turnover += self.data.turnover[0]
            self.total_volume += self.data.volume[0]
        else:
            self.trade_date = trade_date
            self.total_turnover = self.data.turnover[0]
            self.total_volume = self.data.volume[0]

        # 计算平均成交价
        if self.total_volume > 0:
            self.lines.avg_price[0] = self.total_turnover / 1 / self.total_volume
        else:
            self.lines.avg_price[0] = 0
import backtrader as bt


class KDJ(bt.Indicator):
    lines = ('k', 'd', 'j')
    params = (
        ('period', 14),
        ('smoothK', 3),
        ('smoothD', 3),
    )

    def __init__(self):
        # 计算 K 值
        self.k = bt.indicators.Stochastic(self.data.high, self.data.low, self.data.close,
                                          period=self.params.period).k

        # 计算 D 值
        self.d = bt.indicators.SimpleMovingAverage(self.k, period=self.params.smoothD)

    def next(self):
        # 计算 J 值
        if self.d[0] != 0:
            self.lines.j[0] = 3 * self.k[0] - 2 * self.d[0]
        else:
            self.lines.j[0] = 0

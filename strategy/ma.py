import backtrader as bt


class SimpleMAStrategy(bt.Strategy):
    params = (
        ('period', 30),
    )

    def __init__(self):
        self.order = None
        self.dataclose = self.datas[0].close
        self.sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.period)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()}: {txt}")

    def next(self):
        # 如果有订单处于等待状态，不能下单
        if self.order:
            return

        # 如果还没有持仓
        k = 0.015
        if not self.position:
            if self.dataclose[0] <= self.sma[0] * (1-k):
                self.log(f"BUY CREATE: price={self.dataclose[0]}, sma={self.sma[0]}")
                self.order = self.buy(exectype=bt.Order.StopTrail)
        else:
            if self.dataclose[0] >= self.sma[0]* (1+k):
                self.log(f"SELL CREATE: price={self.dataclose[0]}, sma={self.sma[0]}")
                self.order = self.sell()

    def notify_order(self, order):
        # 忽略Submitted和Accepted状态
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXECUTED at {order.executed.price:.2f}")
            else:
                self.log(f"SELL EXECUTED at {order.executed.price:.2f}")

        self.order = None

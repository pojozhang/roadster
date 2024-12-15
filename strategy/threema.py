import backtrader as bt
import indicator.threema as threema


class ThreeMAStrategy(bt.Strategy):
    params = (
        ('take_profit_percent', 0.03),
        ('stop_loss_percent', 0.01),
        ('short_period', 10),
        ('median_period', 20),
        ('long_period', 40),
    )

    def __init__(self):
        self.order = None
        self.dataclose = self.datas[0].close
        self.signal = threema.ThreeMASignal(self.datas[0], short_period=self.params.short_period,
                                            median_period=self.params.median_period,
                                            long_period=self.params.long_period)
        self.s_ma = bt.indicators.SMA(period=self.params.short_period)
        self.m_ma = bt.indicators.SMA(period=self.params.median_period)
        self.l_ma = bt.indicators.SMA(period=self.params.long_period)
        self.rsi = bt.indicators.RelativeStrengthIndex(self.data.close, period=7)
        self.buyprice = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()}: {txt}")

    def next(self):
        # 如果有订单处于等待状态，不能下单
        if self.order:
            return

        # 如果还没有持仓
        if not self.position:
            if self.signal == 1:
                self.log(f"BUY CREATE: price={self.dataclose[0]}")
                self.buyprice = self.dataclose[0]
                self.order = self.buy()
        else:
            # 止损
            if self.dataclose[0] <= self.buyprice * (1 - self.params.stop_loss_percent):
                self.order = self.sell()
                self.log(f"SELL CREATE STOP LOSS: price={self.dataclose[0]}")
                return

            if self.dataclose[0] >= self.buyprice * (1 + self.params.take_profit_percent):
                self.order = self.sell()
                self.log(f"SELL CREATE TAKE PROFIT: price={self.dataclose[0]}")
                return

            if self.signal == -1:
                self.log(f"SELL CREATE: price={self.dataclose[0]}")
                self.order = self.sell()

    def notify_order(self, order):
        if order.status == order.Completed:
            if order.isbuy():
                print(f"Buy order executed at {order.executed.price}")
            elif order.issell():
                print(f"Sell order executed at {order.executed.price}")
                # 重置当前订单
            self.order = None

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print(f"Order {order.ref} canceled/margin/rejected.")

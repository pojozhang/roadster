import backtrader as bt

from indicator.averageprice import AveragePrice


class SimpleRSIStrategy(bt.Strategy):
    params = (
        ('period', 20),
        ('take_profit_percent', 0.05),
        ('stop_loss_percent', 0.02),
        ('rsi_overbought', 70),
        ('rsi_oversold', 30),
    )

    def __init__(self):
        self.order = None
        self.dataclose = self.datas[0].close
        self.rsi = bt.indicators.RelativeStrengthIndex(self.data.close, period=self.params.period)
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
            if self.rsi[0] < self.params.rsi_oversold:
                self.log(f"BUY CREATE: price={self.dataclose[0]}, rsi={self.rsi[0]}")
                self.buyprice = self.dataclose[0]
                cash = self.broker.get_cash()*0.5
                size = int(cash / self.data)
                self.order = self.buy(size = size)
        else:
            # 止损
            if self.dataclose[0] <= self.buyprice * (1 - self.params.stop_loss_percent):
                self.order = self.sell(size = self.position.size)
                self.log(f"SELL CREATE STOP LOSS: price={self.dataclose[0]}, rsi={self.rsi[0]}")
                return

            if self.dataclose[0] >= self.buyprice * (1 + self.params.take_profit_percent):
                self.order = self.sell(size = self.position.size)
                self.log(f"SELL CREATE TAKE PROFIT: price={self.dataclose[0]}, rsi={self.rsi[0]}")
                return
                # self.sell(exectype=bt.Order.StopTrailLimit, price=self.buyprice * (1 - self.params.stop_loss_percent))
            if self.rsi[0] >= self.params.rsi_overbought:
                self.log(f"SELL CREATE: price={self.dataclose[0]}, rsi={self.rsi[0]}")
                self.order = self.sell(size = self.position.size)

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

import backtrader as bt


class SimpleBollingerStrategy(bt.Strategy):
    params = (
        ('period', 20),
        ('devfactor', 2),
        ('take_profit_percent', 0.5),
        ('stop_loss_percent', 0.07),
        ('rsi_overbought', 70),
        ('rsi_oversold', 12),
    )

    def __init__(self):
        self.order = None
        self.dataclose = self.datas[0].close
        self.boll = bt.indicators.BollingerBands(self.data.close, period=self.params.period,
                                                 devfactor=self.params.devfactor)
        self.rsi = bt.indicators.RelativeStrengthIndex(self.data.close, period=20)
        self.buyprice = None
        self.reachMidBoll = False

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()}: {txt}")

    def next(self):
        # 如果有订单处于等待状态，不能下单
        if self.order:
            return

        upperShadow = self.data.high[0] - max(self.data.open, self.data.close)
        lowerShadow = min(self.data.open, self.data.close) - self.data.low[0]
        entity = abs(self.data.open - self.data.close)

        # 如果还没有持仓
        if not self.position:

            if self.data.high[0] < self.boll.lines.bot[0] and lowerShadow > 3*entity:
                self.log(
                    f"BUY CREATE: price={self.dataclose[0]}, high={self.data.high[0]}, boll={self.boll.lines.bot[0]}")
                self.buyprice = self.dataclose[0]
                self.order = self.buy()
        else:
            if self.data.high[0] >= self.boll.lines.mid[0]:
                self.reachMidBoll = True

            if self.dataclose[0] <= self.buyprice * (1 - self.params.stop_loss_percent):
                self.order = self.sell()
                self.reachMidBoll = False
                self.log(f"SELL CREATE STOP LOSS: price={self.dataclose[0]}")
                return

            if self.dataclose[0] >= self.buyprice * (1 + self.params.take_profit_percent):
                self.order = self.sell()
                self.reachMidBoll = False
                self.log(f"SELL CREATE TAKE PROFIT: price={self.dataclose[0]}")
                return

            if self.reachMidBoll and self.data.high[0] < self.boll.lines.mid[0]:
                self.order = self.sell()
                self.reachMidBoll = False
                self.log(f"SELL CREATE TAKE PROFIT: price={self.dataclose[0]}")
                return

            # print(f"high: {self.data.high[0]}")
            if self.data.high[0] >= self.boll.lines.top[0]:
                self.log(f"SELL CREATE: price={self.data.high[0]}, boll={self.boll.lines.top[0]}")
                self.order = self.sell()
                self.reachMidBoll = False

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

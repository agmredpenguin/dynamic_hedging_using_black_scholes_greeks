# Trade analyser
import backtrader as bt
import mplfinance as mpl
import matplotlib.pyplot as plt
import pandas as pd

class trade_list(bt.Analyzer):

    def get_analysis(self):

        return self.trades


    def __init__(self):

        self.trades = []
        self.cumprofit = 0.0


    def notify_trade(self, trade):

        if trade.isclosed:

            brokervalue = self.strategy.broker.getvalue()

            dir = 'short'
            if trade.history[0].event.size > 0: dir = 'long'

            pricein = trade.history[len(trade.history)-1].status.price
            priceout = trade.history[len(trade.history)-1].event.price
            datein = bt.num2date(trade.history[0].status.dt)
            dateout = bt.num2date(trade.history[len(trade.history)-1].status.dt)
            timein = bt.num2time(trade.history[0].status.dt)
            timeout = bt.num2time(trade.history[len(trade.history)-1].status.dt)
            if trade.data._timeframe >= bt.TimeFrame.Days:
                datein = datein.date()
                dateout = dateout.date()
                timein = timein.strftime("%H:%M:%S")
                timeout = timeout.strftime("%H:%M:%S")

            pcntchange = 100 * priceout / pricein - 100
            pnl = trade.history[len(trade.history)-1].status.pnlcomm
            pnlpcnt = 100 * pnl / brokervalue
            barlen = trade.history[len(trade.history)-1].status.barlen
            pbar = pnl / barlen
            self.cumprofit += pnl

            size = value = 0.0
            for record in trade.history:
                if abs(size) < abs(record.status.size):
                    size = record.status.size
                    value = record.status.value

            highest_in_trade = max(trade.data.high.get(ago=0, size=barlen+1))
            lowest_in_trade = min(trade.data.low.get(ago=0, size=barlen+1))
            hp = 100 * (highest_in_trade - pricein) / pricein
            lp = 100 * (lowest_in_trade - pricein) / pricein
            if dir == 'long':
                mfe = hp
                mae = lp
            if dir == 'short':
                mfe = -lp
                mae = -hp

            self.trades.append({'TradeIdentifier': trade.ref, 'Ticker': trade.data._name, 'OrderType': dir,
                 'DateIn': datein, 'TimeIn': timein, 'PriceIn': pricein, 'DateOut': dateout, 'TimeOut': timeout, 'PriceOut': priceout,
                 'PctChange%': round(pcntchange, 2), 'Profit|Loss': pnl, 'Profit|LossRatio|BrokerValue': round(pnlpcnt, 3),
                 'PositionSize': size, 'MaxTradeValue': value, 'CummProfitLoss': self.cumprofit,
                 'TradeDurationBars': barlen, 'Profit|Loss/Bar': round(pbar, 2),
                 'MaxFavourableExcrusion': round(mfe, 3), 'MaxAdverseExcrusion': round(mae, 3)})


from botlog import BotLog
from poloniex import poloniex

class BotTrade(object):

	def __init__(self, dateOpen, type, pair, currentPrice, amount, stopLoss, targetPrice, backtest):

		self.output = BotLog()
		self.status = "OPEN"
		self.type = type
		self.pair = pair
		self.exitType = ""
		self.backtest = backtest
		self.dateOpen = dateOpen
		self.dateClosed = ""
		self.entryPrice = currentPrice
		self.exitPrice = ""
		self.profit = 0
		self.fees = amount * 0.0025

		self.quantity = round(amount / currentPrice, 3)

		self.conn = poloniex('W4F5HMHJ-OUT7003S-WQ2Z2DRX-E0YFAGGX', '98cc6233508ab121a0b58585abd3b743215062694f5aee6d5907d236b7872e622d4cf930123ce634ef74d62694c3b38e61618262844c0cf4016b67e150814285')

		if self.backtest == False:
			self.output.log("Trade opened" + self.type)
			orderNumber = self.conn.buy(self.pair, currentPrice*1.0005, self.quantity)

		self.stopLoss = currentPrice * (1-stopLoss)
		self.targetPrice = currentPrice * (1+targetPrice)

	def close(self, dateClosed, currentPrice, exitType):

		self.status = "CLOSED"
		self.dateClosed = dateClosed
		self.exitPrice = currentPrice
		self.exitType = exitType
		self.fees = self.fees + (self.quantity * self.exitPrice * 0.0025)
		self.profit = self.quantity * (self.exitPrice - self.entryPrice) - self.fees
		self.percentage = round(100*((self.exitPrice / self.entryPrice)-1), 2)

		if self.backtest == False:
			self.output.log("Trade closed" + self.type)
			orderNumber = self.conn.sell(self.pair, currentPrice*.9995, self.quantity)

	def showTrade(self):

		tradeStatus = self.dateOpen + " " + self.type + " Buy " + str(self.quantity) + " at " + str(self.entryPrice)

		if (self.status == "CLOSED"):
			tradeStatus = tradeStatus + " Sell " + self.dateClosed + " " + str(self.exitType) + " Exit: "+ str(self.exitPrice) + " Fees: "+ str(self.fees) + " Net Profit: "
			if (self.exitPrice > self.entryPrice):
				tradeStatus = tradeStatus + "\033[92m"
			else:
				tradeStatus = tradeStatus + "\033[91m"

			tradeStatus = tradeStatus+str(self.profit)+ " " + str(self.percentage) + "%" + "\033[0m"

		self.output.log(tradeStatus)

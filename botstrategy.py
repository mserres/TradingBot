import time

from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade

class BotStrategy(object):

	def __init__(self, name, mode, pair, numTrades, startUSD, startUnit, tradeAmount, stopLoss, targetPrice, backtest, output):

		self.output = output
		self.name = name
		self.mode = mode
		self.pair = pair
		self.numTrades = numTrades
		self.startUSD = startUSD
		self.startUnit = startUnit
		self.tradeAmount = tradeAmount
		self.stopLoss = stopLoss
		self.targetPrice = targetPrice
		self.backtest = backtest

		self.prices = []
		self.closes = []
		self.trades = []

		self.upperBBand = []
		self.lowerBBand = []
		self.midBBand = []

		self.MACDDiff = []
		self.MACDSignal = []

		self.rsi = []

		self.date = ""
		self.action = []
		self.dataPoints = []
		self.balancePoints = []
		self.MACDPoints = []
		self.rsiPoints = []
		self.currentPrice = ""
		self.currentClose = ""

		self.holdingsUSD = startUSD
		self.holdingsUnits = startUnit
		self.balance = startUSD
		self.balanceNoTrade = startUSD
		self.profit = 0
		self.fees = 0
		self.indicators = BotIndicators()

		self.priceAverage = 0

	def tick(self,candlestick):

		self.action = []
		self.description = []

		self.currentPrice = float(candlestick.priceAverage)
		self.prices.append(self.currentPrice)

		self.updateBalance(0, self.currentPrice)
		
		#self.currentClose = float(candlestick['close'])
		#self.closes.append(self.currentClose)

		currentUpperBBand, currentLowerBBand, currentMidBBand = self.indicators.bbands(self.prices[-30:])
		self.upperBBand.append(currentUpperBBand)
		self.lowerBBand.append(currentLowerBBand)

		currentMACDSlow, currentMACDFast, currentMACDDiff, currentMACDSignal = self.indicators.MACD(self.prices[-30:])
		self.MACDDiff.append(currentMACDDiff)
		self.MACDSignal.append(currentMACDSignal)

		self.rsi.append(self.indicators.RSI(self.prices[-30:]))

		self.evaluatePositions()

		if self.backtest == "backtest":
			tickdate = candlestick.date
			self.date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tickdate))
		else:
			tickdate = int(time.time())
			self.date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tickdate))

		self.dataPoints.append({'date': str(tickdate * 1000), 'price': str(self.currentPrice), 'upperbb': str(currentUpperBBand), 'lowerbb': str(currentLowerBBand), 'action': 'null', 'description': 'null'})
		self.balancePoints.append({'date': str(tickdate * 1000), 'balance': str(self.balance), 'balanceNoTrade': str(self.balanceNoTrade)})
		self.MACDPoints.append({'date': str(tickdate * 1000), 'MACDDiff': str(self.MACDDiff[-1]), 'MACDSignal': str(self.MACDSignal[-1])})
		self.rsiPoints.append({'date': str(tickdate * 1000), 'RSI': str(self.rsi[-1]), 'RSIHIGH': str(70), 'RSILOW': str(30)})

		if len(self.action) > 0:
			self.dataPoints[-1]['action'] = "'*'"
			self.dataPoints[-1]['description'] = "'" + ', '.join(self.action) + "'"

	def evaluatePositions(self):

		openTrades = []
		for trade in self.trades:
			if (trade.status == "OPEN"):
				openTrades.append(trade)

		if len(openTrades) < self.numTrades and self.holdingsUSD > self.tradeAmount:

			if self.mode in ["MACD", "ALL"] and self.MACDDiff[-1] < self.MACDSignal[-1] and self.MACDDiff[-2] > self.MACDSignal[-2]:

				self.trades.append(BotTrade(self.date, "MACD", self.pair, self.currentPrice, self.tradeAmount, self.stopLoss, self.targetPrice, self.backtest, self.output))
				self.updateBalance(self.tradeAmount / self.currentPrice, self.currentPrice)
				self.action.append('Open MACD=, Amount=' + str(self.tradeAmount) + ', Price=' + str(self.currentPrice))

			elif self.mode in ["MACD2", "ALL"] and self.MACDDiff[-1] < 500 and ((self.MACDDiff[-1] > 0 and self.MACDDiff[-2] < 0) or (self.MACDDiff[-1] < self.MACDSignal[-1] and self.MACDDiff[-2] > self.MACDSignal[-2])):

				self.trades.append(BotTrade(self.date, "MACD2", self.pair, self.currentPrice, self.tradeAmount, self.stopLoss, self.targetPrice, self.backtest, self.output))
				self.updateBalance(self.tradeAmount / self.currentPrice, self.currentPrice)
				self.action.append('Open MACD2=, Amount=' + str(self.tradeAmount) + ', Price=' + str(self.currentPrice))

			elif self.mode in ["MACD3", "ALL"] and self.MACDDiff[-1] > 0 and self.MACDDiff[-2] < 0:

				self.trades.append(BotTrade(self.date, "MACD3", self.pair, self.currentPrice, self.tradeAmount, self.stopLoss, self.targetPrice, self.backtest, self.output))
				self.updateBalance(self.tradeAmount / self.currentPrice, self.currentPrice)
				self.action.append('Open MACD3=, Amount=' + str(self.tradeAmount) + ', Price=' + str(self.currentPrice))

			elif self.mode in ["BBAND", "ALL"] and self.prices[-1] > self.lowerBBand[-1] and self.prices[-2] < self.lowerBBand[-2]:

				self.trades.append(BotTrade(self.date, "BBAND", self.pair, self.currentPrice, self.tradeAmount, self.stopLoss, self.targetPrice, self.backtest, self.output))
				self.updateBalance(self.tradeAmount / self.currentPrice, self.currentPrice)
				self.action.append('Open BBAND, Amount='+ str(self.tradeAmount) + ', Price=' + str(self.currentPrice))

			elif self.mode in ["RSI", "ALL"] and self.rsi[-1] < 30 and self.rsi[-2] > 30:

				self.trades.append(BotTrade(self.date, "RSI", self.pair, self.currentPrice, self.tradeAmount, self.stopLoss, self.targetPrice, self.backtest, self.output))
				self.updateBalance(self.tradeAmount / self.currentPrice, self.currentPrice)
				self.action.append('Open RSI, Amount='+ str(self.tradeAmount) + ', Price=' + str(self.currentPrice))

			elif len(self.prices) > 12:

				if self.mode in ["DROP", "ALL"] and self.prices[-1] < self.prices[-6] *.95 and self.prices[-1] > self.prices[-2]:

					self.trades.append(BotTrade(self.date, "DROP", self.pair, self.currentPrice, self.tradeAmount, self.stopLoss, self.targetPrice, self.backtest, self.output))
					self.updateBalance(self.tradeAmount / self.currentPrice, self.currentPrice)
					self.action.append('Open DROP, Amount='+ str(self.tradeAmount) + ', Price=' + str(self.currentPrice))

		for trade in openTrades:
				
			if (self.currentPrice < trade.stopLoss):
				trade.close(self.date, self.currentPrice, "STOPLOSS")
				self.updateBalance(-trade.quantity, self.currentPrice)
				self.action.append('Close STOPLOSS=' + str(self.currentPrice))

			if trade.type in ["MACD"] and self.MACDDiff[-1] > self.MACDSignal[-1] and self.MACDDiff[-2] < self.MACDSignal[-2] and self.currentPrice > trade.targetPrice:
				
				trade.close(self.date, self.currentPrice, "MACD")
				self.updateBalance(-trade.quantity, self.currentPrice)
				self.action.append('CLOSE MACD=' + str(self.currentPrice))

			elif trade.type in ["MACD2"] and ((self.MACDDiff[-2] > 0 and self.MACDDiff[-1] < 0) or (self.MACDDiff[-1] > self.MACDSignal[-1] and self.MACDDiff[-2] < self.MACDSignal[-2])) and self.currentPrice > trade.targetPrice:

				trade.close(self.date, self.currentPrice, "MACD2")
				self.updateBalance(-trade.quantity, self.currentPrice)
				self.action.append('CLOSE MACD2=' + str(self.currentPrice))

			elif trade.type in ["MACD3"] and self.MACDDiff[-2] > 0 and self.MACDDiff[-1] < 0 and self.currentPrice > trade.targetPrice:

				trade.close(self.date, self.currentPrice, "MACD3")
				self.updateBalance(-trade.quantity, self.currentPrice)
				self.action.append('CLOSE MACD3=' + str(self.currentPrice))

			elif trade.type in ["BBAND"] and self.prices[-1] < self.upperBBand[-1] and self.prices[-2] > self.upperBBand[-2] and self.currentPrice > trade.targetPrice:
				
				trade.close(self.date, self.currentPrice, "BBAND")
				self.updateBalance(-trade.quantity, self.currentPrice)
				self.action.append('CLOSE BBAND=' + str(self.currentPrice))

			elif trade.type in ["RSI"] and self.rsi[-1] > 65 and self.rsi[-2] < 65 and self.currentPrice > trade.targetPrice:
				
				trade.close(self.date, self.currentPrice, "RSI")
				self.updateBalance(-trade.quantity, self.currentPrice)
				self.action.append('CLOSE RSI=' + str(self.currentPrice))

			"""elif trade.type in ["DROP"] and self.currentPrice > trade.targetPrice:

				trade.close(self.date, self.currentPrice, "DROP")
				self.updateBalance(-trade.quantity, self.currentPrice)
				self.action.append('CLOSE DROP=' + str(self.currentPrice))"""

			self.tradeAmount = int((self.holdingsUSD - 1) / self.numTrades)
			#self.output.log(str(self.tradeAmount))

	def showPositions(self):

		for trade in self.trades:
			trade.showTrade()

	def showProfit(self):

		self.profit = 0
		self.fees = 0

		for trade in self.trades:
			self.fees = self.fees + trade.fees
			if (trade.status == "CLOSED"):
				self.profit = self.profit + trade.profit

		tradesOpened = sum(1 for i in self.trades if i.status == "OPEN")
		tradesClosed = sum(1 for i in self.trades if i.status == "CLOSED")

		tradesProfitableNumber = sum(1 for i in self.trades if i.profit > 0 and i.status == "CLOSED")
		tradesProfitableAmount = sum(i.profit for i in self.trades if i.profit > 0 and i.status == "CLOSED")

		tradesLossesNumber = sum(1 for i in self.trades if i.profit < 0 and i.status == "CLOSED")
		tradesLossesAmount = sum(i.profit for i in self.trades if i.profit < 0 and i.status == "CLOSED")

		self.output.log("\nSummary for " + self.name + ", Target / StopLoss " + str(self.targetPrice) + " / " + str(self.stopLoss) + ",  with " + self.mode + " Start with: " + str(self.startUnit) + " unit(s) and " + str(self.startUSD) + " USD")
		self.output.log("Hold: End valuation: " + str(self.balanceNoTrade) + " Units: " + str(self.startUnit) + " USD: " + str(self.startUSD) + " Price: " + str(self.currentPrice))
		self.output.log("Trade: End valuation: " + str(self.balance) + " Units: " + str(self.holdingsUnits) + " USD: " + str(self.holdingsUSD) + ". Price: " + str(self.currentPrice))

		if tradesClosed > 0:
			self.output.log("Profit inc Fees: " + str(self.profit) + ", Fees: " + str(self.fees) + ", " + str(len(self.trades)) + " Trades with " + str(tradesOpened) + " still open\n")
			#self.output.log("Trades > 0: Number: " + str(tradesProfitableNumber) + ", Total: " + str(tradesProfitableAmount))
			#self.output.log("Trades < 0: Number: " + str(tradesLossesNumber) + ", Total: " + str(tradesLossesAmount))

	def updateBalance(self, quantity, price):

		self.holdingsUSD = self.holdingsUSD - (quantity * price)
		self.holdingsUnits =  self.holdingsUnits + quantity
		self.balance = self.holdingsUSD + (self.holdingsUnits * price)
		self.balanceNoTrade = self.startUSD + (self.startUnit * price)

	def drawGraph(self):
		self.output.drawGraph(self.dataPoints, self.balancePoints, self.MACDPoints, self.rsiPoints, self.name, self.mode)

import requests, json

from poloniex import poloniex
from botcandlestick import BotCandlestick

class BotChart(object):

	def __init__(self, exchange, pair, period, backtest):

		self.exchange = exchange
		self.pair = pair
		self.period = period

		#http://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start=1483228800&end=1514764800&period=300

		self.startTime = 1483228800 # 01 JAN 2017
		#self.startTime = 1504224000 # 01 SEP 2017
		#self.endTime = 1506729600 # 30 SEP 2017
		self.endTime = 1514764800 # 1 Jan 2018

		self.data = []

		if (self.exchange == "poloniex"):
			self.conn = poloniex('key goes here', 'Secret goes here')

			if backtest:
				data = self.conn.api_query("returnChartData", {"currencyPair": self.pair, "start": self.startTime, "end": self.endTime, "period": self.period})
				#data = json.loads(open("./data/btc-usd-data.json", "r").readline())

				for d in data:
					if (d['open'] and d['close'] and d['high'] and d['low']):
						self.data.append(BotCandlestick(d['date'], self.period, d['open'], d['close'], d['high'], d['low'], d['weightedAverage']))

		if (self.exchange == "bittrex"):
			if backtest:
				url = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=" + self.pair + "&tickInterval=" + self.period + "&_=" + str(self.startTime)
				response = requests.get(url)
				rawdata = response.json()

				self.data = rawdata["result"]

	def getPoints(self):

		return self.data

	def getCurrentPrice(self):

		currentValues = self.conn.api_query("returnTicker")
		lastPairPrice = currentValues[self.pair]["last"]
		return lastPairPrice

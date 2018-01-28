import sys, getopt, time
from botlog import BotLog

class BotCandlestick(object):

	def __init__(self, output, date, period, open=None, close=None, high=None, low=None, priceAverage=None):

		self.date = date
		self.current = None
		self.open = open
		self.close = close
		self.high = high
		self.low = low
		self.startTime = time.time()
		self.period = period
		self.output = output
		self.priceAverage = priceAverage
		self.prices = []

	def tick(self,price):

		self.current = float(price)
		self.prices.append(self.current)

		if (self.open is None):
			self.open = self.current

		if ( (self.high is None) or (self.current > self.high) ):
			self.high = self.current

		if ( (self.low is None) or (self.current < self.low) ):
			self.low = self.current

		if ( time.time() >= ( self.startTime + self.period) ):
			self.close = self.current
			# self.priceAverage = ( self.high + self.low + self.close ) / float(3)
			self.priceAverage = sum(self.prices) / len(self.prices)

		self.output.log("Open: "+str(self.open)+" Close: "+str(self.close)+" High: "+str(self.high)+" Low: "+str(self.low)+" Current: "+str(self.current)+" Average: "+str(self.priceAverage))

	def isClosed(self):

		if (self.close is not None):
			return True
		else:
			return False

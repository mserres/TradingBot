import numpy as np
import statistics

class BotIndicators(object):

	def __init__(self):

		pass

	def movingAverage(self, dataPoints, period):

		if (len(dataPoints) > 1):
			return sum(dataPoints[-period:]) / float(len(dataPoints[-period:]))
		else:
			return dataPoints[-1]

	def EMA(self, dataPoints, period):

		x = np.asarray(dataPoints)
		weights = None
		weights = np.exp(np.linspace(-1., 0., period))
		weights /= weights.sum()

		a = np.convolve(x, weights, mode='full')[:len(x)]
		a[:period] = a[period]
		return a

	def momentum(self, dataPoints, period=14):

		if (len(dataPoints) > period -1):
			return dataPoints[-1] * 100 / dataPoints[-period]

	def MACD(self, dataPoints, nslow=26, nfast=12):

		if (len(dataPoints) > 26):
			emaslow = self.EMA(dataPoints, nslow)
			emafast = self.EMA(dataPoints, nfast)
			emasignal = self.EMA(emafast - emaslow, 9)
			return emaslow[-1], emafast[-1], emafast[-1] - emaslow[-1], emasignal[-1]
		else:
			return 0, 0, 0, 0

	def standardDeviation(self, dataPoints, period):

		if (len(dataPoints) > period-1):
			return statistics.stdev(dataPoints[-period:])
		else:
			return dataPoints[-1]

	def RSI(self, prices, period=14):

		deltas = np.diff(prices)
		seed = deltas[:period + 1]
		up = seed[seed >= 0].sum() / period
		down = -seed[seed < 0].sum() / period

		if down:

			rs = up / down
			rsi = np.zeros_like(prices)
			rsi[:period] = 100. - 100. / (1. + rs)

			for i in range(period, len(prices)):
				delta = deltas[i - 1]  # cause the diff is 1 shorter
				if delta > 0:
					upval = delta
					downval = 0.
				else:
					upval = 0.
					downval = -delta

				up = (up * (period - 1) + upval) / period
				down = (down * (period - 1) + downval) / period
				rs = up / down
				rsi[i] = 100. - 100. / (1. + rs)

			if len(prices) > period:
				return rsi[-1]
			else:
				return 50  # output a neutral amount until enough prices in list to calculate RSI

		else:
			return 50 # no down

	def bbands(self, price, period=20, numsd=2):

		if len(price) > period:
			ave = self.movingAverage(price, period)
			sd = self.standardDeviation(price, period)

			upband = ave + (sd*numsd)
			dnband = ave - (sd*numsd)

			return (upband, dnband, ave)
		else:
			return (price[-1], price[-1], price[-1])
import sys, getopt, time, urllib
from botchart import BotChart
from botstrategy import BotStrategy
from botlog import BotLog
from botcandlestick import BotCandlestick

def main(argv):

	pairs = ["USDT_BTC"]#, "USDT_ETH", "USDT_LTC"]
	exchanges = ["poloniex"]
	charts = []
	strategies = []
	#modes = ["DROP", "RSI", "BBAND", "MACD", ALL"]
	modes = ["MACD"]
	period = 300

	for pair in pairs:
		for exchange in exchanges:
			charts.append(BotChart(exchange, pair, period))
			for mode in modes:
				strategies.append(BotStrategy(exchange + '-' + pair, mode, 20, 10000, 0, 1000, 0.01, 0.15, False))

	candlesticks = []
	developingCandlestick = BotCandlestick(period)

	for i, chart in enumerate(charts):
		for j, mode in enumerate(modes):
			while True:
				strategy = strategies[len(modes) * i + j]
				try:
					developingCandlestick.tick(chart.getCurrentPrice())
				except urllib.error.URLError:
					time.sleep(int(30))
					developingCandlestick.tick(chart.getCurrentPrice())

				if (developingCandlestick.isClosed()):
					candlesticks.append(developingCandlestick)
					strategy.tick(developingCandlestick)
					developingCandlestick = BotCandlestick(period)

					strategy.showProfit()
					strategy.showPositions()
					strategy.drawGraph()

				time.sleep(int(30))

if __name__ == "__main__":
	main(sys.argv[1:])
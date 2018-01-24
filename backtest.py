import sys, getopt, time
from botchart import BotChart
from botstrategy import BotStrategy

def main(argv):

	start_time = time.time()

	pairs = ["USDT_BTC"]#, "USDT_ETH", "USDT_LTC"]
	exchanges = ["poloniex"]
	charts = []
	strategies = []
	#modes = ["RSI", "BBAND", "MACD", "ALL"]
	#modes = ["RSI", "BBAND", "MACD"]
	modes = ["MACD"]

	for pair in pairs:
		for exchange in exchanges:
			charts.append(BotChart(exchange, pair, 1800))
			for mode in modes:
				strategies.append(BotStrategy(exchange + '-' + pair, mode, 10, 10000, 0, 1000, 0.01, 0.1, True))
				# Parameters: max trades, initial fiat, initial holding, trade amount, stop loss, target

	for i, chart in enumerate(charts):
		for j, mode in enumerate(modes):
			strategy = strategies[len(modes)*i+j]
			for candlestick in chart.getPoints():
				candlestick['priceAverage'] = candlestick['weightedAverage']
				strategy.tick(candlestick)

			strategy.showProfit()
			strategy.showPositions()
			strategy.drawGraph()

	print("\n--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
	main(sys.argv[1:])
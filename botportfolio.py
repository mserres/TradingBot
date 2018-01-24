import sys, getopt, time
from botchart import BotChart
from botstrategy import BotStrategy

### DRAFT ###

def main(argv):

	start_time = time.time()

	pairs = ["USDT_BTC", "USDT_ETH", "USDT_LTC"]
	exchanges = ["poloniex"]
	charts = []

	for pair in pairs:
		for exchange in exchanges:
			charts.append(BotChart(exchange, pair, 1800))

	portfolio_head = ['pair', 'allocation', 'value']
	portfolio_allocation = ['USDT_BTC', 50, 400], ['USDT_ETH', 30, 300], ['USDT_LTC', 20, 180]
	portfolio = []

	for p in portfolio_allocation:
		portfolio.append(dict(zip(portfolio_head, p)))

	print('portfolio:', portfolio)
	rebal = needReBalance(portfolio)
	print('Needs rebalance?', rebal)
	if rebal:
		print(reBalance(portfolio))

	chart_zip = zip(charts)

	for c in charts:
		print(c['weightedAverage'])

	exit()
	#for c in charts:
	for candlestick in zip(charts.getPoints()):
		print(candlestick['weightedAverage'])

	exit()

	for charts[0], charts[1], charts[2] in zip(charts[0], charts[1], charts[2]):
		print(float(charts[0].getpoint()['weightedAverage']))
		print(float(charts[1].getpoint()['weightedAverage']))
		print(float(charts[2].getpoint()['weightedAverage']))

	exit()

	for i, chart in enumerate(charts):
			for candlestick in chart.getPoints():
				tick(portfolio, candlestick)

	print("\n--- %s seconds ---" % (time.time() - start_time))

def needReBalance(portfolio, tolerance=5):
	value = 0
	for p in portfolio:
		value = value + p['value']
	print('Portfolio value =', value)

	ret = False

	for p in portfolio:
		print('Current allocation =', 100 * p['value'] / value, 'Target allocation =', p['allocation'])
		#print('Tolerance lower bound', p['allocation']*(1-tolerance/100), 'Tolerance upper bound', p['allocation']*(1+tolerance/100))
		result = ''
		if(100 * p['value'] / value < p['allocation']*(1-tolerance/100) or 100 * p['value'] / value > p['allocation']*(1+tolerance/100)):
			ret = True
			result = 'NOK'
		print('Tolerance lower bound', p['allocation'] * (1 - tolerance / 100), 'Tolerance upper bound',
			  p['allocation'] * (1 + tolerance / 100), result)

	return ret

def reBalance(portfolio, tolerance=5):
	value = 0
	for p in portfolio:
		value = value + p['value']

	ret = []

	for p in portfolio:
		if (100 * p['value'] / value < p['allocation'] * (1 - tolerance / 100) or 100 * p['value'] / value > p['allocation'] * (1 + tolerance / 100)):
			ret.append('trade ' + str(p['allocation']-(100 * p['value'] / value)) + ' of ' + p['pair'])

	return ret

def tick(portfolio, candlestick):
	currentPrice = float(candlestick['weightedAverage'])
	print(portfolio, candlestick, currentPrice)
	exit()

	self.updateBalance(0, self.currentPrice)

def updateBalance(portfolio, prices):
	name = 0

if __name__ == "__main__":
	main(sys.argv[1:])
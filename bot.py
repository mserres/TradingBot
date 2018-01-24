import sys, getopt, time, urllib

from botchart import BotChart
from botstrategy import BotStrategy
from botcandlestick import BotCandlestick


def main(argv):

    start_time = time.time()

    backTest = True # Use True for backtesting, False for live paper trade
    period = 14400 # Use 1800 for 30 min tick, 300 for 5 min tick

    exchanges = ["poloniex"]
    #pairs = ["USDT_BTC",  "USDT_ETH", "USDT_LTC", "USDT_ZEC"]
    pairs = ["USDT_BTC"]
    #modes = ["RSI"]
    #modes = ["BBAND"]
    #modes = ["MACD"]
    modes = ["RSI", "BBAND", "MACD", "DROP"]

    charts = []
    strategies = []

    for pair in pairs:
        for exchange in exchanges:
            charts.append(BotChart(exchange, pair, period, backTest))
            for mode in modes:
                strategies.append(BotStrategy(exchange + ' | Target +' + str(20) + '% | ' + pair + '', mode, pair, 1, 5000, 0, 4000, 0.6, .6, backTest))
                        # Parameters: max trades, initial fiat, initial holding, trade amount, stop loss, target

    if (backTest):
        for i, chart in enumerate(charts):
            for j, mode in enumerate(modes):
                strategy = strategies[len(modes) * i + j]
                for candlestick in chart.getPoints():
                    strategy.tick(candlestick)

                #strategy.showPositions()
                strategy.showProfit()
                strategy.drawGraph()
                print("\n--- %s seconds ---" % (time.time() - start_time))
    else:
        candlesticks = []
        developingCandlestick = BotCandlestick(int(time.time()), period)

        for i, chart in enumerate(charts):
            for j, mode in enumerate(modes):
                while True:
                    strategy = strategies[len(modes) * i + j]
                    try:
                        developingCandlestick.tick(chart.getCurrentPrice())
                    except urllib.error.URLError:
                        time.sleep(int(period/10))
                        developingCandlestick.tick(chart.getCurrentPrice())

                    if (developingCandlestick.isClosed()):
                        candlesticks.append(developingCandlestick)
                        strategy.tick(developingCandlestick)
                        developingCandlestick = BotCandlestick(int(time.time()), period)

                        strategy.showPositions()
                        strategy.showProfit()
                        strategy.drawGraph()

                    time.sleep(int(period/10))

if __name__ == "__main__":
    main(sys.argv[1:])
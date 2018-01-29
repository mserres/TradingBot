import sys, getopt, time, urllib

from botchart import BotChart
from botstrategy import BotStrategy
from botcandlestick import BotCandlestick
from botlog import BotLog

def main(argv):

    pairs = []

    try:
        opts, args = getopt.getopt(argv, "hm:p:c:", ["mode=", "period=", "currency="])
    except getopt.GetoptError:
        print("bot.py -m <backtest | paper | live> -p <period length in sec> -c <currency pair>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("bot.py -m <backtest | paper | live> -p <period length in sec> -c <currency pair>")
            sys.exit()
        elif opt in ("-m", "--mode"):
            if (arg == "backtest"):
                mode = arg
            elif (arg == "paper"):
                mode = arg
            elif (arg == "live"):
                mode = arg
            else:
                print("Requires mode to be 'backtest', 'paper' or 'live'")
                sys.exit(2)
        elif opt in ("-p", "--period"):
            if (int(arg) in [300, 900, 1800, 7200, 14400, 86400]):
                period = int(arg)
            else:
                print("Requires periods to be 300, 900, 1800, 7200, 14400, or 86400 second increments")
                sys.exit(2)
        elif opt in ("-c", "--currency"):
            pairs.append(arg)

    start_time = time.time()

    output = BotLog()

    exchanges = ["poloniex"]
    #pairs = ["USDT_BTC",  "USDT_ETH", "USDT_LTC", "USDT_ZEC"]
    #modes = ["RSI"]
    #modes = ["BBAND"]
    #modes = ["BBAND", "MACD2", "ALL"]
    algos = ["MACD"]
    #modes = ["RSI", "BBAND", "MACD2", "MACD", "DROP", "ALL"]

    charts = []
    strategies = []

    target = 0.04
    stoploss = 0.18

    for pair in pairs:
        for exchange in exchanges:
            if (mode == "backtest"):
                charts.append(BotChart(exchange, pair, period, mode, output))
            else:
                charts.append(BotChart(exchange, pair, period, "warm", output, int(time.time() - (24*60*60)), int(time.time())))

            for algo in algos:
                if (mode == "backtest"):
                    strategies.append(BotStrategy(exchange + "-" + pair, algo, pair, 1, 5000, 0, int(5000 - 1), stoploss, target, mode, output))
                            # Parameters: max trades, initial fiat, initial holding, trade amount, stop loss, target
                else:
                    strategies.append(BotStrategy(exchange + "-" + pair, algo, pair, 1, 5000, 0, int(5000 - 1), stoploss, target, "warm", output))

    if (mode == "backtest"):
        for i, chart in enumerate(charts):
            for j, algo in enumerate(algos):
                strategy = strategies[len(algos) * i + j]
                for candlestick in chart.getPoints():
                    strategy.tick(candlestick)

                strategy.showPositions()
                strategy.showProfit()
                strategy.drawGraph()
                output.log("\n--- %s seconds ---" % (time.time() - start_time))
    else:
        candlesticks = []
        developingCandlestick = BotCandlestick(output, int(time.time()), period)

        for i, chart in enumerate(charts):
            for j, algo in enumerate(algos):

                strategy = strategies[len(algos) * i + j]

                for candlestick in chart.getPoints():
                    strategy.tick(candlestick)

                strategy.drawGraph()
                strategy.backtest = mode

                while True:
                    try:
                        developingCandlestick.tick(chart.getCurrentPrice())
                    except urllib.error.URLError:
                        time.sleep(int(period/10))
                        developingCandlestick.tick(chart.getCurrentPrice())

                    if (developingCandlestick.isClosed()):
                        candlesticks.append(developingCandlestick)
                        strategy.tick(developingCandlestick)
                        developingCandlestick = BotCandlestick(output, int(time.time()), period)

                        strategy.showPositions()
                        strategy.showProfit()
                        strategy.drawGraph()

                    time.sleep(int(period/10))

    output.close()

if __name__ == "__main__":
    main(sys.argv[1:])

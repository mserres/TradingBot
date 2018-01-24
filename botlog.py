import os

class BotLog(object):

	def __init__(self):

		pass

	def log(self, message):

		print(message)

	def drawGraph(self, graphPoints, balancePoints, MACDPoints, RSIPoints, name, mode):

		self.outputGraph = open(os.path.expanduser("../web/bot/graph/" + name + "-" + mode + "-Graph.html"), 'w')

		self.outputGraph.truncate()
		self.outputGraph.write("""<html>
<head>
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawGraph);
google.charts.setOnLoadCallback(drawMACD);
google.charts.setOnLoadCallback(drawRSI);
google.charts.setOnLoadCallback(drawBalance);

function drawGraph() {
	var data = new google.visualization.DataTable();
	data.addColumn('datetime', 'time');
	data.addColumn('number', 'UpperBBand');
	data.addColumn('number', 'LowerBBand');
	data.addColumn('number', 'Price');
	data.addColumn({type: 'string', role:'annotation'});
	data.addColumn({type: 'string', role:'annotationText'});
	data.addRows([""")

		for point in graphPoints:
			self.outputGraph.write("[new Date(" + point['date'] +  ")," + point['upperbb'] + "," + point['lowerbb'] + "," + point['price'] + "," + point['action']  + "," + point['description'] + "],\n")

		self.outputGraph.write("""]);
var options = {
	title: 'Price Chart',
	legend: { position: 'bottom' }, 
	explorer: { 
		actions: ['dragToZoom', 'rightClickToReset'],
		axis: 'horizontal',
		keepInBounds: true,
		maxZoomIn: 1000.0
	},
};
var chart = new google.visualization.LineChart(document.getElementById('graph_chart_div'));
chart.draw(data, options);}

function drawMACD() {
	var data = new google.visualization.DataTable();
	data.addColumn('datetime', 'time');
	data.addColumn('number', 'MACDDiff');
	data.addColumn('number', 'MACDSignal');
	data.addRows([""")

		for point in MACDPoints:
			self.outputGraph.write("[new Date(" + point['date'] +  ")," + point['MACDDiff'] + "," + point['MACDSignal'] + "],\n")

		self.outputGraph.write("""]);
var options = {
	title: 'MACD Chart',
	legend: { position: 'bottom' }, 
	explorer: { 
		actions: ['dragToZoom', 'rightClickToReset'],
		axis: 'horizontal',
		keepInBounds: true,
		maxZoomIn: 1000.0
	},
};
var chart = new google.visualization.LineChart(document.getElementById('macd_chart_div'));
chart.draw(data, options);}

function drawRSI() {
	var data = new google.visualization.DataTable();
	data.addColumn('datetime', 'time');
	data.addColumn('number', 'RSI');
	data.addColumn('number', 'RSIHIGH');
	data.addColumn('number', 'RSILOW');
	data.addRows([""")

		for point in RSIPoints:
			self.outputGraph.write("[new Date(" + point['date'] +  ")," + point['RSI'] + "," + point['RSIHIGH']  + "," + point['RSILOW']+ "],\n")

		self.outputGraph.write("""]);
var options = {
	title: 'RSI Chart',
	legend: { position: 'bottom' }, 
	explorer: { 
		actions: ['dragToZoom', 'rightClickToReset'],
		axis: 'horizontal',
		keepInBounds: true,
		maxZoomIn: 1000.0
	},
};
var chart = new google.visualization.LineChart(document.getElementById('rsi_chart_div'));
chart.draw(data, options);}

function drawBalance() {
	var data = new google.visualization.DataTable();
	data.addColumn('datetime', 'time');
	data.addColumn('number', 'balance');
	data.addColumn('number', 'balance No Trade');
	data.addRows([""")

		for point in balancePoints:
			self.outputGraph.write("[new Date(" + point['date'] +  ")," + point['balance'] + "," + point['balanceNoTrade'] + "],\n")

		self.outputGraph.write("""]);
var options = {
	title: 'Balance Chart',
	legend: { position: 'bottom' }, 
	explorer: { 
		actions: ['dragToZoom', 'rightClickToReset'],
		axis: 'horizontal',
		keepInBounds: true,
		maxZoomIn: 1000.0
	},
};
var chart = new google.visualization.LineChart(document.getElementById('balance_chart_div'));
chart.draw(data, options);}
</script>
</head>
	<body>
		<div id="graph_chart_div" style="width: 100%; height: 25%"></div>
		<div id="macd_chart_div" style="width: 100%; height: 25%"></div>
		<div id="rsi_chart_div" style="width: 100%; height: 25%"></div>
		<div id="balance_chart_div" style="width: 100%; height: 25%"></div>
	</body>
</html>""")
		self.outputGraph.close()
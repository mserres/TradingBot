import os, datetime

class BotLog(object):

	def __init__(self):

		stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
		self.output = open("../web/bot/" + stamp + "-bot.log", 'w')

	def log(self, message):

		self.output.write(message + "\n")
		print(message)

	def close(self):

		self.output.close()

	def drawGraph(self, graphPoints, balancePoints, MACDPoints, RSIPoints, name, mode):

		self.outputGraph = open(os.path.expanduser("../web/bot/graph/" + name + "-" + mode + "-Graph.html"), 'w')

		self.outputGraph.truncate()
		self.outputGraph.write("""<html>
<head>
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
google.charts.load('current', {'packages':['corechart', 'controls']});
google.charts.setOnLoadCallback(drawDashboard);

function drawDashboard() {
	var data = new google.visualization.DataTable();
	data.addColumn('datetime', 'time');
	data.addColumn('number', 'UpperBBand');
	data.addColumn('number', 'LowerBBand');
	data.addColumn('number', 'Price');
	data.addColumn({type: 'string', role:'annotation'});
	data.addColumn({type: 'string', role:'annotationText'});
	data.addColumn('number', 'MACD Diff');
	data.addColumn('number', 'MACD Signal');
	data.addColumn('number', 'RSI');
	data.addColumn('number', 'RSI High');
	data.addColumn('number', 'RSI Low');
	data.addColumn('number', 'Balance');
	data.addColumn('number', 'Balance No Trade');
	data.addRows([""")

		for point in zip(graphPoints, MACDPoints, RSIPoints, balancePoints):
			self.outputGraph.write("[new Date(" + point[0]['date'] +  ")," + point[0]['upperbb'] + "," + point[0]['lowerbb'] + "," + point[0]['price'] + "," + point[0]['action']  + "," + point[0]['description'] + ",")
			self.outputGraph.write(point[1]['MACDDiff'] + "," + point[1]['MACDSignal'] + ",")
			self.outputGraph.write(point[2]['RSI'] + "," + point[2]['RSIHIGH'] + "," + point[2]['RSILOW'] + ",")
			self.outputGraph.write(point[3]['balance'] + "," + point[3]['balanceNoTrade'] + "],\n")

		self.outputGraph.write("""]);

 	// Create a dashboard.
    var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard_div'));

    // Create a line chart, passing some options
   var chart1 = new google.visualization.ChartWrapper({
        chartType: 'LineChart',
        containerId: 'chart1_div',
        options : {
            height: 400,
            title: 'Price Chart',
			legend: { position: 'bottom' }, 
		},
		view: {'columns': [0, 1, 2, 3, 4, 5]}
      });
      
    // Create a line chart, passing some options
   	var chart2 = new google.visualization.ChartWrapper({
        chartType: 'LineChart',
        containerId: 'chart2_div',
        options : {
			height: 400,
			title: 'MACD Chart',
			legend: { position: 'bottom' }, 
		},
		view: {'columns': [0, 6, 7]}
      });
      
    // Create a line chart, passing some options
   	var chart3 = new google.visualization.ChartWrapper({
        chartType: 'LineChart',
        containerId: 'chart3_div',
        options : {
			height: 400,
			title: 'RSI Chart',
			legend: { position: 'bottom' }, 
		},
		view: {'columns': [0, 8, 9, 10]}
      });
      
	// Create a line chart, passing some options
   	var chart4 = new google.visualization.ChartWrapper({
        chartType: 'LineChart',
        containerId: 'chart4_div',
        options : {
			height: 400,
			title: 'Balance Chart',
			legend: { position: 'bottom' }, 
		},
		view: {'columns': [0, 11, 12]}
      });
      
    // Create a range slider, passing some options
	var control = new google.visualization.ControlWrapper({
        controlType: 'ChartRangeFilter',
        containerId: 'control_div',
        options: {
            filterColumnIndex: 0,
            ui: {
                chartOptions: {
                    height: 50,
                    chartArea: {
                        width: '80%'
                    }
                },
                chartView : {'columns': [0, 3]}
            }
        },
    });

	// Establish dependencies, declaring that 'filter' drives 'pieChart',
	// so that the pie chart will only display entries that are let through
	// given the chosen slider range.
	dashboard.bind(control, chart1);
	dashboard.bind(control, chart2);
	dashboard.bind(control, chart3);
	dashboard.bind(control, chart4);

	// Draw the dashboard.
	dashboard.draw(data);
}
</script>
</head>
	<body>
		<div id="dashboard_div">
      	<!--Divs that will hold each control and chart-->
      		<div id="control_div"></div>
      		<div id="chart1_div"></div>
      		<div id="chart2_div"></div>
      		<div id="chart3_div"></div>
      		<div id="chart4_div"></div>
    	</div>
	</body>
</html>""")
		self.outputGraph.close()
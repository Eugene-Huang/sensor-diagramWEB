$(function () {
	    // Get the data and create the chart
	    $.getJSON('/user/lastweeklight', function (data) {
	    	// if (data == null) {
	    	// 	$(window).load(function(){
	    	// 		$('#lastweek-temp').append("<h1>No Data</h1>");
	    	// 		// alert(data);
	    	// 	});
	    	// }
	    	// else {
		    	Highcharts.setOptions({
	    		    global:{
	    		        useUTC:false
	    		    }
	    	    })
		        $('#lastweek-light').highcharts('StockChart', {
		        	chart: {
		        	    type: 'column'
		        	},
		        	rangeSelector: {
				        enabled: false
				    },
				    navigator: {
				    	enabled: false
				    },
				    scrollbar: {
				    	enabled: false
				    },
				    exporting:{
				    	enabled: true
				    },
				    credits:{
				    	enabled: false
				    },
				    title : {
				     	text: '上周光照值走向'
				    },
				    subtitle: {
				    	useHTML: true,
				    	text: "Source: <a href='/contact' target='_blank'>Zhifeng Studio</a>"
				    },
				    yAxis: {
		                title: {
		                    text: 'Light (Lux)'
		                },
		                crosshair: false
				    },
				    xAxis: {
				    	type: 'datetime',
				    	labels: {
			                formatter: function() {
			                    return Highcharts.dateFormat('%A', this.value);                  
			                }
			            },
			            tickInterval: 1000 * 3600 * 24,
				    	crosshair: false
				    },
		            series: [{
		                name: 'Max',
		                color: 'rgba(223, 83, 83, .5)',
		                data: data[1]
		            },{
		            	name: 'Min',
		                color: 'rgba(119, 152, 191, .5)',
		            	data: data[0]
		            }]
		        });
	    	// }
	    });
	});
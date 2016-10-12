$(function () {
	    // Get the data and create the chart
	    $.getJSON('/user/lastdaytemp', function (data) {
    	   	Highcharts.setOptions({
    		    global:{
    		        useUTC:false
    		    }
    	   })
	        $('#lastday-temp').highcharts("StockChart", {
	        	chart: {
	        		type: "line"
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
			     	text: '昨日温度趋势'
			    },
			    subtitle: {
			    	useHTML: true,
			    	text: "Source: <a href='/contact' target='_blank'>Zhifeng Studio</a>"
			    },
			    xAxis: {
			    	// ordinal: false,
			    	title: {
			    		text: 'Time: H/Min',
			    		align: 'high'
			    	},
			    	type: 'datetime',
			    	labels: {
		                formatter: function() {
		                    return Highcharts.dateFormat('%H:%M', this.value);                  
		                }
		            },
			    	crosshair: {
		                width: 2,
		                color: 'rgba(119, 152, 191, .5)',
		                dashStyle: 'dash'
			        }
			    },
			    yAxis: {
	                title: {
	                    text: 'Temperature (°C)'
	                },
	                crosshair: {
		                width: 2,
		                color: 'rgba(119, 152, 191, .5)',
		                dashStyle: 'dash'
		            }
			    },
			    plotOptions: {
	                line: {
	                    dataLabels: {
	                        enabled: true
	                    }
	                },
	                series: {
	                	marker: {
	                		enabled: true,
	                		radius: 4
	                	}
	                }
			    },
			    tooltip: {
	    			positioner: function(){
	    				return { x: 60, y: 30};
	    			},
	                valueSuffix: 'ºC'
			    },
	            series: [{
	                name: 'temperature',
	                data: data
	            }]
	        });
	    });
	});
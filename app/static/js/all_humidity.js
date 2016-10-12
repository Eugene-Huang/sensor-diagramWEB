$(function () {
	    // Get the data and create the chart
	    $.getJSON('/user/allhum', function (data) {
    	   	Highcharts.setOptions({
    		    global:{
    		        useUTC:false
    		    }
    	   })
	        $('#all-humidity').highcharts("StockChart", {
	        	chart: {
	        		type: "line"
	        	},
	        	rangeSelector: {
			        allButtonsEnabled: true,
	                selected: 2
			    },
			    navigator: {
			    	enabled: true
			    },
			    scrollbar: {
			    	enabled: true
			    },
			    exporting:{
			    	enabled: true
			    },
			    credits:{
			    	enabled: false
			    },
			    title : {
			     	text: '湿度显示汇总'
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
	                    text: 'Humidity (°)'
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
	                valueSuffix: 'º'
			    },
	            series: [{
	                name: 'humidity',
	                data: data
	            }]
	        });
	    });
	});
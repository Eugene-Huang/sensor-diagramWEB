$(function() {
	$('#click2search').bind('click', function() {
		$.getJSON('/user/lastweekhum', {
			'node': $('input[name="node"]').val()
		}, function(data) {
			Highcharts.setOptions({
				global: {
					useUTC: false
				}
			})
			$('#lastweek-humidity').highcharts('StockChart', {
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
				exporting: {
					enabled: true
				},
				credits: {
					enabled: false
				},
				title: {
					text: '上周湿度走向'
				},
				subtitle: {
					useHTML: true,
					text: "Source: <a href='/contact' target='_blank'>Zhifeng Studio</a>"
				},
				yAxis: {
					title: {
						text: 'Humidity (°)'
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
				}, {
					name: 'Min',
					color: 'rgba(119, 152, 191, .5)',
					data: data[0]
				}]
			});
		});
	});
});
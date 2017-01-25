$(function() {
	$('#click2search').bind('click', function() {
		$.getJSON('/user/alllight', {
				'node': $('input[name="node"]').val()
			},
			function(data) {
				Highcharts.setOptions({
					global: {
						useUTC: false
					}
				})
				$('#all-light').highcharts("StockChart", {
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
					exporting: {
						enabled: true
					},
					credits: {
						enabled: false
					},
					title: {
						text: '光照值显示汇总'
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
							text: 'Light (Lux)'
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
						positioner: function() {
							return {
								x: 60,
								y: 30
							};
						},
						valueSuffix: 'Lux'
					},
					series: [{
						name: 'Light',
						data: data
					}]
				});
			});
	});
});
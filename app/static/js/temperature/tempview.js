$(function() {
    $('#click2search').bind('click', function(data) {
        $.ajax({
            type: "GET",
            url: '/user/tempview',
            data: {
                'node': $('input[name="node"]').val()
            },
            dataType: "json",
            success: function(data) {
                Highcharts.setOptions({
                    global: {
                        useUTC: false
                    }
                })
                chart = new Highcharts.StockChart({
                    chart: {
                        renderTo: 'actualtime-temp',
                        type: 'spline',
                        events: {
                            load: st // ajax定时器
                        }
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
                        text: '实时温度监控'
                    },
                    subtitle: {
                        useHTML: true,
                        text: "Source: <a href='/contact' target='_blank'>Zhifeng Studio</a>"
                    },
                    xAxis: {
                        title: {
                            text: 'Time: Min/Sec',
                            align: 'high'
                        },
                        type: 'datetime',
                        labels: {
                            formatter: function() {
                                return Highcharts.dateFormat('%M:%S', this.value);
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
                        valueSuffix: 'ºC'
                    },
                    series: [{
                        name: 'temperature',
                        data: data
                    }]
                });
            }
        });
    });
});
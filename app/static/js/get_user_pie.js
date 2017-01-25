$(function() {
  $.getJSON("/admin/userchart", function(data) {
    $('#user-charts').highcharts({
      chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false
      },
      title: {
        text: '用户权限统计表'
      },
      tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
      },
      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          dataLabels: {
            enabled: true,
            format: '<b>{point.name}</b>: {point.percentage:.1f} %',
            style: {
              color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
            }
          }
        }
      },
      series: [{
        type: 'pie',
        name: 'User statistics',
        data: [{
            name: data[0][0],
            y: data[0][1],
            sliced: true,
            selected: true
          },
          data[1],
          data[2]
        ]
      }]
    });
  });
});
  $(function() {
    $('#click2search').bind('click', function() {
      $.getJSON('/admin/digsensor/line', {
        'node': $('input[name="node"]').val()
      }, function(data) {
        Highcharts.setOptions({
            global: {
              useUTC: false
            }
          })
          //火焰传感器
        $('#fire-line').highcharts('StockChart', {
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
            text: '火焰传感器数据汇总'
          },
          yAxis: {
            title: {
              text: 'ON/OFF'
            },
            crosshair: {
              width: 2,
              color: 'rgba(119, 152, 191, .5)',
              dashStyle: 'dash'
            }
          },
          xAxis: {
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
                radius: 3
              }
            }
          },
          tooltip: {
            formatter: function() {
              if (this.y == 1) {
                tip = "ON"
              } else if (this.y == -1) {
                tip = "OFF"
              }
              var s = '<b>' + "Fire sensor" + '</b>';
              $.each(this.points, function() {
                s += '<br/>' + 'Status' + ': ' +
                  tip;
              });
              return s;
            }
          },
          series: [{
            name: 'Fire sensor',
            data: data[0]
          }]
        });
        //烟雾传感器
        $('#smoke-line').highcharts('StockChart', {
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
            text: '烟雾传感器数据汇总'
          },
          yAxis: {
            title: {
              text: 'ON/OFF'
            },
            crosshair: {
              width: 2,
              color: 'rgba(119, 152, 191, .5)',
              dashStyle: 'dash'
            }
          },
          xAxis: {
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
                radius: 3
              }
            }
          },
          tooltip: {
            formatter: function() {
              if (this.y == 1) {
                tip = "ON"
              } else if (this.y == -1) {
                tip = "OFF"
              }
              var s = '<b>' + "Smoke sensor" + '</b>';
              $.each(this.points, function() {
                s += '<br/>' + 'Status' + ': ' +
                  tip;
              });
              return s;
            }
          },
          series: [{
            name: 'Smoke sensor',
            data: data[1]
          }]
        });
        //人体红外
        $('#human-line').highcharts('StockChart', {
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
            text: '人体红外传感器数据汇总'
          },
          yAxis: {
            title: {
              text: 'ON/OFF'
            },
            crosshair: {
              width: 2,
              color: 'rgba(119, 152, 191, .5)',
              dashStyle: 'dash'
            }
          },
          xAxis: {
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
                radius: 3
              }
            }
          },
          tooltip: {
            formatter: function() {
              if (this.y == 1) {
                tip = "ON"
              } else if (this.y == -1) {
                tip = "OFF"
              }
              var s = '<b>' + "Human infrared sensor" + '</b>';
              $.each(this.points, function() {
                s += '<br/>' + 'Status' + ': ' +
                  tip;
              });
              return s;
            }
          },
          series: [{
            name: 'Human infrared sensor',
            data: data[2]
          }]
        });
      });
    });
  });
//2秒钟刷新一次数据
function st() {
  setInterval("getData()", 3000);
}

//动态更新图表数据
function getData() {
  $.ajax({
    type: "GET",
    url: "/user/newtemp",
    data: {
      'node': $('input[name="node"]').val()
    },
    dataType: "json",
    success: function(data) {
      chart.series[0].addPoint(data, true, true);
    },
    error: function() {
      console.log('Request failed!!');
    },
    cache: false
  });
}
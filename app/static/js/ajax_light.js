//2秒钟刷新一次数据
  function st() {
   setInterval("getData()", 2000);
  }

//动态更新图表数据
  function getData() {
    
   $.ajax({
      type: "get",
      url: "/user/newlight",
      dataType: "json",
      success : function(data){
        chart.series[0].addPoint(data,true,true);
      },
      error: function () {
        alert('Request failed!!');
      },
      cache: false
    });
}
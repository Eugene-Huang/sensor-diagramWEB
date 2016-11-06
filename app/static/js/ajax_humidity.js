
//2秒钟刷新一次数据
  function st() {
   setInterval("getData()", 5000);
  }

//动态更新图表数据
  function getData() {
    
   $.ajax({
      type: "get",
      url: "/user/newhum",
      dataType: "json",
      success : function(data){
        chart.series[0].addPoint(data,true,true);
      },
      error: function () {
        console.log('Request failed!!');
      },
      cache: false
    });
}

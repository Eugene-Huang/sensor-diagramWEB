//2秒钟刷新一次数据
  function st() {
   setInterval("getData()", 2000);
  }

//动态更新数据
  function getData() {
    
   $.ajax({
      type: "get",
      url: "/indexdata",
      dataType: "json",
      success : function(data){
          $("#cur-temperature").text(data[0]);
          $("#cur-humidity").text(data[1]);
      },
      error: function () {
          alert("Request failed!");
      },
      cache: false
    });
}
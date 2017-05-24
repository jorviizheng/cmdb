      $(document).ready(function() {
          // if ($.cookie("user-key") == null) {
          //     window.location.href = 'login.html';
          // }
          initTable();
      });

      function initTable() {
          apiUrl = "http://cmdb.wanda.cn/api/task/gettask";
          $('#taskTable').bootstrapTable('destroy');
          //初始化表格,动态从服务器加载数据  
          $("#taskTable").bootstrapTable({
              method: "GET", //使用get请求到服务器获取数据  
              url: apiUrl,
              striped: true, //表格显示条纹  
              pagination: true, //启动分页  
              pageSize: 5, //每页显示的记录数  
              pageNumber: 1, //当前第几页  
              pageList: [10, 20, 30, 40, 50], //记录数可选列表  
              clickToSelect: true,
              sortOrder: "asc",
              dataType: 'json',
              contentType: "application/json;charset=utf-8",
              search: false, //是否启用查询
              // searchOnEnterKey: true,
              // showColumns: false, //显示下拉框勾选要显示的列  
              // showRefresh: true, //显示刷新按钮 
              uniqueId: "server_id",
              sidePagination: "server", //表示服务端请求
              //设置为undefined可以获取pageNumber，pageSize，searchText，sortName，sortOrder  
              //设置为limit可以获取limit, offset, search, sort, order
              queryParamsType: "limit",
              queryParams: function queryParams(params) {
                  var param = {
                      offset: params.pageNumber,
                      limit: params.pageSize,
                      // search: $('#toolbar').val()
                  };
                  return params;
              },

              // onLoadSuccess: function() { //加载成功时执行  

              // },
              // onLoadError: function() { //加载失败时执行  
              //     alert("加载数据失败", { time: 1500, icon: 2 });
              // }
          });
          $("#taskTable").bootstrapTable('refresh');


      }


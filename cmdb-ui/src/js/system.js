/**
 * Created by pippo on 17-2-17.
 */

$(function() {

    //默认激活
    show_server_name($("#hostname_server_name"));
    //获取并设置主机列表
    $("#server_tag_search_input").val("");
    set_server_group(get_server_name_list());

    //根据标签页初始化信息
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {

        var result_group = $("#sync_result_show_list");
        result_group.empty();

        // 获取已激活的标签页的名称
        var active_tab = $(e.target);
        if (active_tab.attr('href') == "#system_yum_tab"){
            get_yum_source();
            // set_package_input_list();

        }else if (active_tab.attr("href") ==  "#system_firewall"){
            show_server_name($("#firewall_server_name"));
        }

        // // 获取前一个激活的标签页的名称
        // var previousTab = $(e.relatedTarget).text();
        // $(".active-tab span").html(activeTab);
        // $(".previous-tab span").html(previousTab);
    });
//
});

//server_group
function get_servers_by_tag() {
    var tag_name = $("#server_tag_search_input");
    var server_list =  new Array()
    if (tag_name.val() !=''){
        var api_url = api_server_url + "/api/async/v1/tag/server/" + tag_name.val();
        $.ajax({
            type: "GET",
            url: api_url,
            contentType: "application/json;charset=utf-8",
            dataType: "json",
            // async: false,
            success: function(data) {
                if (data.status == 0){
                    if (data.msg != 0){
                        for (var i=0;i<data.msg.length;i++){
                            server_list.push(data.msg[i]['server_name'])
                        }
                    }
                    set_server_group(server_list)
                }
            },
            error: function(data) {
                alert('获取主机用户名列表失败，原因:'+ data.msg);
            }
        });

    }else{
        set_server_group(get_server_name_list());
    }

}
function reset_servers_group() {
    set_server_group(get_server_name_list());
}
//
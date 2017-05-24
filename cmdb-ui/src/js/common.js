/**
 * Created by pippo on 17-2-17.
 */

var api_server_url = "http://cmdb.wanda.cn";
var name_list = get_server_name_list();
var select_server_list = new Array();

function get_server_name_list() {
    var api_url = "http://cmdb.wanda.cn/api/async/v1/servers/list";
    var name_list = new Array();
    $.ajax({
        type: "GET",
        url: api_url,
        async: false,
        contentType: "application/json;charset=utf-8",
        success: function(data) {
            if (data.status == 0) {
                name_list = data.msg;
            }
        },
        error: function(data, status) {
            alert(status);
        }
    });
    return name_list;
}

function show_server_name(select_name){

    select_name.empty();
    select_name.append("<option selected='selected'  value=0>请选择..</option>");

    for(var i=0;i<name_list.length;i++){
        index = i + 1;
        select_name.append("<option  value=" + index + ">" + name_list[i] + "</option>");
    }
}


//获取对应server的index
function get_server_index(server) {
    for (var i=0;i<select_server_list.length;i++){
        if (select_server_list[i] == server){
            return i;
        }
    }
    return -1
}
//选中server
function set_server_list(buttons){
    buttons.each(function (index,element) {
        element.onclick = function () {
            var index = get_server_index($(this).text());
            if ($(this).hasClass("active")){ //已激活
                $(this).attr("class","btn-default btn-lg");
                $(this).button('reset');
                if (index >= 0){
                    select_server_list.splice(index,1);
                }
            }else{
                $(this).attr("class","btn-success btn-lg");
                $(this).button('toggle');
                if (index == -1){
                    select_server_list.push($(this).text());
                }
            }
        }
    });
}
//获取server 列表
function set_server_group(server_list) {
    var server_group = $("#server_group");

    server_group.empty();
    var inline_str = "<li class=\"container\">" + "<ul class=\"list-inline\">";
    if (server_list.length != 0){
        var list_array = new Array();
        var col_num = 10;
        for(var list_index=0,len=server_list.length;list_index<len;list_index+=col_num){
            list_array.push(server_list.slice(list_index,list_index+col_num));
        }
        for (var i=0;i<list_array.length;i++){
            var line = inline_str;
            for (var j=0;j<list_array[i].length;j++){
                line = line + "<button class=\"btn-default btn-lg\" id=\"server_list_btn_" + list_array[i][j] +"\">"+ list_array[i][j]+ "</button>";
            }
            line = line + "</ul></li>";
            server_group.append("<li class=\"list-group-item\"" + line+ "</li>");
        }
    }else{
        line = inline_str + "<p>不存在该标签服务器</p></ul></li>";
        server_group.append("<li class=\"list-group-item\"" + line+ "</li>");
    }
    set_server_list($("#server_list_container :button"));

}

//获取主机的IP地址
function get_host_ip(server_name) {
    var api_url = api_server_url + "/api/async/v1/server/ip/"+ server_name;
    var host_ip = '';
    $.ajax({
        type: "GET",
        url: api_url,
        async: false,
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function(data) {
            if (data.status == 0) {
                host_ip = data.msg;
            }
        },
        error: function(data, status) {
            alert(data.msg);
        }
    });
    return host_ip;
}

//获取已选择主机列表的IP地址
function  get_hosts_ip() {
    var hosts = new Array();
    for(var i=0;i<select_server_list.length;i ++){
        hosts.push(get_host_ip(select_server_list[i]));
    }
    return hosts;
}

//判断选中服务器系统版本是否一致
function check_servers_os_version_equal() {
    var os_list = new Array();

    if (select_server_list.length < 2){
        return true;
    }

    for(var i=0;i<select_server_list.length;i ++){
        $.ajax({
            type: "GET",
            url: api_server_url + "/api/async/v1/server/info?condition=server_name&&value="+ select_server_list[i],
            async: false,
            contentType: "application/json;charset=utf-8",
            dataType: "json",
            success: function(data) {
                if (data.status == 0){
                    if (data.msg != 0){
                        var os_version = data.msg["system_type"];
                        if ($.inArray(os_version, os_list) == -1){
                            os_list.push(os_version);
                        }
                    }
                }
            },
            error: function(data) {
                alert(data);
            }
        });
    }
    if (os_list.length == 1) {
        return true;
    }else{
        return false;
    }

}
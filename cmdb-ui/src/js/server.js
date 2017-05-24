/**
 * Created by pippo on 2017/3/9.
 */

var pxe_templates= new Array();

$(function() {
    show_server_name($("#tag_server_select"));
    check_manager_ip_exist();
    get_pxe_template();
    get_dhcp_range();
    get_dhcp_range_ip();

});
//tag
function get_current_tags() {
    var server_name = $("#tag_server_select option:selected");
    var api_url = api_server_url + '/api/async/v1/server/info?condition=server_name&&value=' + server_name.text();
    var tag_server_list = $("#tag_server_list");
    tag_server_list.empty();
    $.ajax({
        url: api_url,
        method: 'GET',
        success:function (data) {
            var tag_list = data.msg['tag'].split(',');
            for(i=0;i<tag_list.length;i++){
                index = i + 1 ;
                tag_server_list.append("<li class=\"list-group-item\">"+ tag_list[i] + "</li>");

            }
        }
    });

}
function tag_action() {
    var server_name = $("#tag_server_select option:selected");
    var t_name = $("#tag_name_input").val();
    var action = $("#tag_action_select option:selected");
    if (server_name.val() == 0 || action.val() == 0){
        alert('选择项不正确');
    }
    else {
        if (action.val() == 1) { //添加tag
            var attach_tag_url = api_server_url + "/api/async/v1/tag/server/" + t_name;
            var add_json = JSON.stringify({
                "name": server_name.text()
            });
            $.ajax({
                type: "POST",
                url: attach_tag_url,
                contentType: "application/json;charset=utf-8",
                dataType: "json",
                data: add_json,
                success: function (data) {
                    if (data.status < 0){
                        alert("操作失败")
                    }else{
                        alert('标记成功');
                    }

                    window.location.reload();
                },
                error: function (data) {
                    alert('标记失败，失败原因:'+ data.msg);
                    window.location.reload();
                }
            });
        } else if ( action.val() == 2) { //删除tag
            var del_tag_url = api_server_url + "/api/async/v1/tag/server/" + t_name;
            var del_json = JSON.stringify({
                "name": server_name.text()
            });
            $.ajax({
                type: "PATCH",
                url: del_tag_url,
                contentType: "application/json;charset=utf-8",
                dataType: "json",
                data: del_json,
                success: function (data) {
                    if (data.status < 0){
                        alert("操作失败")
                    }else{
                        alert('标记成功');
                    }
                    window.location.reload();
                },
                error: function (data) {
                    alert(data.msg);
                    window.location.reload();
                }
            });
        }
    }

}
//tag done

//server
function submit_server(){
    var server_name = $("#server_name").val();
    var manager_ip = $("#manager_ip").val();
    var server_ip = $("#server_ip option:selected").val();
    var server_idc = $("#server_idc option:selected").val();

    var pxe_template_val = $("#pxe_template_select option:selected").val();
    var server_group = $("#server_group").val();
    var action = $('#action_select option:selected').val();

    var dhcp_server_id = $("#dhcp_server_select option:selected").val();
    var mac_val = $("#mac_select option:selected").val();
    if (server_name != '' && manager_ip != '' && server_ip != 0 &&
        server_idc != 0 && server_group != '' && pxe_template_val != 0 &&
        dhcp_server_id != 0 && mac_val != 0){
        if (action == 1){
            add_server();
        }else if (action == 2){
            reinstall_server();
        }
    }else {
        alert('选择项错误或者字段为空');
    }

}


function add_server() {
    var server_name = $("#server_name").val();
    var manager_ip = $("#manager_ip").val();
    var mac_address = $("#mac_select option:selected").text();
    var server_ip = $('#server_ip option:selected').text();
    var idc_id = $('#server_idc option:selected').val();
    var server_group = $("#server_group").val();
    var pxe_name = $("#pxe_template_select option:selected").text();
    var pt_id = get_pxe_pt_id(pxe_name);
    var dhcp_server_id = $("#dhcp_server_select option:selected").val();
    var post_json = JSON.stringify({
        "server_name": server_name,
        "manager_ip": manager_ip,
        "server_ip": server_ip,
        "server_group": server_group,
        "idc_id": idc_id,
        "pt_id": pt_id,
        "status":"当前不可用",
        "system_type": pxe_name,
        "dhcp_server_id": dhcp_server_id
    });


    var api_url = api_server_url + "/api/async/v1/servers";
    $.ajax({
        type: "POST",
        url: api_url,
        data: post_json,
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function(data) {
            if (data.status == 0) {
                var server_id = get_server_id(server_name);
                var update_flag = update_dhcp_map(manager_ip, server_ip, mac_address, server_id);
                if (update_flag){
                    add_server_task(server_name, manager_ip, server_ip,mac_address);
                }

            }else{
                alert("新增错误："+ data.msg);
            }
        },
        error: function(data,status) {
            alert("新增错误："+ status);
            window.location.reload();
        }

    });

}

function reinstall_server() {
    var server_name = $("#server_name").val();
    var manager_ip = $("#manager_ip").val();
    var mac_address = $("#mac_select option:selected").text();
    var server_ip = $('#server_ip option:selected').text();
    var idc_id = $('#server_idc option:selected').val();
    var server_group = $("#server_group").val();
    var pxe_name = $("#pxe_template_select option:selected").text();
    var pt_id = get_pxe_pt_id(pxe_name);
    var dhcp_server_id = $("#dhcp_server_select option:selected").val();

    var server_id = get_server_id(server_name);

    var post_json = JSON.stringify({
        "server_name": server_name,
        "manager_ip": manager_ip,
        "server_ip": server_ip,
        "server_group": server_group,
        "idc_id": idc_id,
        "pt_id": pt_id,
        "status":"等待重新安装",
        "system_type": pxe_name,
        "dhcp_server_id": dhcp_server_id
    });
    var update_flag = update_dhcp_map(manager_ip, server_ip, mac_address, server_id);
    if (update_flag){
        var api_url = api_server_url + "/api/async/v1/servers";
        $.ajax({
            type: "PATCH",
            url: api_url,
            data: post_json,
            contentType: "application/json;charset=utf-8",
            dataType: "json",
            success: function(data) {
                if (data.status == 0) {
                    reinstall_server_task(server_name,manager_ip,server_ip, mac_address);
                }else{
                    alert("重装错误："+ data.msg);
                }
            },
            error: function(data,status) {
                alert("重装错误："+ status);
                window.location.reload();
            }

        });
    }

}

function add_server_task(server_name, manager_ip, server_ip, mac_address) {
    var ilo4_user_name = "admin";
    var ilo4_user_passwd = Base64.encode("password");


    var date = datetime_human();
    var current_user = $.cookie('unick');
    var task_name = current_user + '_'+ 'install_new_server_'+ server_name + '_' + datetime_str();

    var task_args = JSON.stringify({
        "server_name": server_name,
        "manager_ip": manager_ip,
        "ilo4_user_name": ilo4_user_name,
        "ilo4_user_passwd": ilo4_user_passwd,
        "server_ip": server_ip,
        "mac_address":mac_address
    });
    var task_type = JSON.stringify({
        "type": "server",
        "action": "add"
    });

    var post_json = JSON.stringify({
        "user_name": current_user,
        "task_name": task_name,
        "task_type": "timely",
        "task_flag": task_type,
        "task_args": task_args,
        "create_time": date,
        "update_time": date
    });

    var api_url = api_server_url + "/api/async/v1/tasks";
    $.ajax({
        type: "POST",
        url: api_url,
        data: post_json,
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function(data, status) {
            if (data.status == 1) {
                alert("任务已添加，请到任务界面查看详细信息");
            }
            window.location.reload();
        },
        error: function(data, status) {
            alert(status);
            window.location.reload();
        }

    });
}

function reinstall_server_task(server_name, manager_ip, server_ip, mac_address) {
    var ilo4_user_name = "admin";
    var ilo4_user_passwd = Base64.encode("password");

    var date = datetime_human();
    var current_user = $.cookie('unick');
    var task_name = current_user + '_'+ 'reship_old_server_'+ server_name + '_' + datetime_str();

    var tark_args = JSON.stringify({
        "server_name": server_name,
        "manager_ip": manager_ip,
        "ilo4_user_name": ilo4_user_name,
        "ilo4_user_passwd": ilo4_user_passwd,
        "server_ip": server_ip,
        "mac_address": mac_address
    });

    var task_type = JSON.stringify({
        "type": "server",
        "action": "reinstall"
    });
    var post_json = JSON.stringify({
        "user_name": current_user,
        "task_name": task_name,
        "task_type": "timely",
        "task_flag": task_type,
        "task_args": tark_args,
        "create_time": date,
        "update_time": date
    });


    var api_url = api_server_url + "/api/async/v1/tasks";
    $.ajax({
        type: "POST",
        url: api_url,
        data: post_json,
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function(data, status) {
            if (data.status == 1) {
                alert("任务已添加，请到任务界面查看详细信息");
            }
            window.location.reload();
        },
        error: function(data, status) {
            alert(status);
            window.location.reload();
        }
    });


}

function check_server_exist() {
    var server_name = $("#server_name").val();
    api_url = api_server_url + "/api/async/v1/server/info?condition=server_name&&value="+ server_name;
    exist = true;
    $.ajax({
        type: "GET",
        url: api_url,
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function(data) {
            //不存在，可添加
            var action_select =$("#action_select");
            action_select.empty();
            action_select.append("<option selected='selected'  value=0>请选择..</option>");

            if (data.status < 0){
                alert(data.msg);
            }else{
                if (data.msg == 0) {
                    $("#manager_ip").attr("readonly",false);
                    $("#manager_ip").val('');
                    $("#mac_select").empty();
                    action_select.append("<option value=1>新装</option>");
                }
                //存在
                else{
                    $("#manager_ip").val(data.msg["manager_ip"]);
                    $("#manager_ip").attr("readonly","readonly");
                    $("#after_manager_ip").attr("disabled",false);
                    action_select.append("<option value=2>重装</option>");
                    //获取mac list
                    get_mac_addr_list();
                }
            }


        },
        error: function(data, status) {
            alert(status);
        }
    });
    return exist;
}

function check_manager_ip_exist(){

    $("#manager_ip").blur(function () {
        var manager_ip = $("#manager_ip").val();
        var api_url = api_server_url + "/api/async/v1/server/info?condition=manager_ip&&value="+ manager_ip;
        $.ajax({
            type: "GET",
            url: api_url,
            contentType: "application/json;charset=utf-8",
            dataType: "json",
            success: function(data) {
                //不存在，可添加
                var action_select =$("#action_select");
                action_select.empty();
                action_select.append("<option selected='selected'  value=0>请选择..</option>");

                if (data.status < 0){
                    alert(data.msg);
                }else{
                    //获取mac list
                    get_mac_addr_list();
                    if (data.msg == 0) {
                        action_select.append("<option value=1>新装</option>");
                    }
                    //存在
                    else{
                        action_select.append("<option value=2>重装</option>");
                    }
                }


            },
            error: function(data, status) {
                alert(status);
            }
        });
    });
}

//dhcp
//获取dhcp分配网段
function get_dhcp_range_ip(){

    var dhcp_server_select = $("#dhcp_server_select");
    dhcp_server_select.blur(function () {
        var dhcp_server_id = dhcp_server_select.val();
       if (dhcp_server_id != 0){
           var api_url = api_server_url + "/api/async/v1/dhcp/range/" + dhcp_server_id;
           $.ajax({
               type: "GET",
               url: api_url,
               async: false,
               contentType: "application/json;charset=utf-8",
               dataType: "json",
               success: function(data) {
                   var range_ip_list = data.msg;
                   $("#server_ip").empty();
                   $("#server_ip").append("<option selected='selected'  value=0>请选择..</option>");
                   for(var i=1;i<range_ip_list.length;i++){
                       $("#server_ip").append("<option  value=" + i + ">" + range_ip_list[i] + "</option>");
                   }
               },
               error: function(data, status) {
                   alert(status);
               }
           });
       }
    });


}
//获取dhcp网段列表
function get_dhcp_range(){

    var api_url = api_server_url + "/api/async/v1/dhcp/servers";
    $.ajax({
        type: "GET",
        url: api_url,
        async: false,
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function(data) {
            var dhcp_list = data.msg;
            var dhcp_server_select = $("#dhcp_server_select");
            dhcp_server_select.empty();
            dhcp_server_select.append("<option selected='selected'  value=0>请选择..</option>");

            for(var i=0;i<data.msg.length;i++){
                dhcp_server_select.append("<option  value=" + dhcp_list[i]['dhcp_server_id'] + ">" +dhcp_list[i]['dhcp_subnet']+ "</option>");
            }
        },
        error: function(data, status) {
            alert(data.msg);
        }
    });
}
function disable(){
    var manager_ip = $("#manager_ip").val();
    if(manager_ip == "172.16.250.23" || manager_ip == "172.16.250.24" || manager_ip == "172.16.250.22" || manager_ip =="172.16.250.31" || manager_ip == "172.16.250.32"
    || manager_ip == "172.16.250.21") {
        $("#after_manager_ip").attr("disabled",false);
        $("#submit_server_btn").attr("disabled", false);
    }else {
        alert('Not Allowed');
        $("#server_ip").empty();
        $("#submit_server_btn").attr("disabled", true);
        $("#after_manager_ip").attr("disabled",true);
    }
}

//获取server_id
function get_server_id(server_name) {
    var server_id = 0;
    var api_url = api_server_url + "/api/async/v1/server/info?condition=server_name&&value="+ server_name;
    $.ajax({
        type: "GET",
        url: api_url,
        async: false,
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function(data) {
            if (data.msg != 0) {
                server_id = data.msg['server_id'];
            }
        },
        error: function(data, status) {
            alert(status);
        }
    });
    return server_id;
}
//server done
//获取pxe模板
function get_pxe_template(){
    var api_url = api_server_url + "/api/async/v1/pxe/names";
    $.ajax({
        type: "GET",
        url: api_url,
        async: false,
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function(data) {
            pxe_templates = data.msg;
            var pxe_select = $("#pxe_template_select");
            pxe_select.empty();
            pxe_select.append("<option selected='selected'  value=0>请选择..</option>");

            for(var i=0;i<data.msg.length;i++){
                index = i + 1;
                pxe_select.append("<option  value=" + index + ">" +data.msg[i]['pxe_name']+ "</option>");
            }
        },
        error: function(data, status) {
            alert(status);
        }
    });

}

//获取pxe pt_id
function get_pxe_pt_id(pxe_name) {
    for (var i=0;i<pxe_templates.length;i++){
        if (pxe_name == pxe_templates[i]['pxe_name']){
            return pxe_templates[i]['pt_id'];
        }
    }
}



//mac
//mac地址获取
function get_mac_addr_list(){
    var manager_ip = $("#manager_ip").val();
    var api_url = api_server_url + "/api/sync/v1/hardware/mac_addr/" + manager_ip;
    var server_btn = $("#submit_server_btn");
    $.ajax({
        type: "GET",
        url: api_url,
        // async: false,
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function(data) {
            if (data.status == 0){
                var mac_select = $("#mac_select");
                mac_select.empty();
                mac_select.append("<option selected='selected'  value=0>请选择..</option>");
                var index = 0;
                for(var i=0;i<data.msg.length;i++){
                    index = i + 1;
                    mac_select.append("<option  value=" + index + ">" +data.msg[i]+ "</option>");
                }
                $("#submit_server_btn").attr('disabled',false);
            }else{
                alert(data.msg);
                $("#submit_server_btn").attr('disabled',true);

            }
        },
        error: function(data, status) {
            alert(status);
        }
    });

}

//获取mac 地址目前绑定IP
function get_mac_map() {
    var mac_addr_select = $("#mac_select option:selected");
    if (mac_addr_select.val() != 0){
        var mac_addr = mac_addr_select.text();
        var api_url = api_server_url + "/api/async/v1/dhcp/map?mac_addr=" + mac_addr;
        $.ajax({
            type: "GET",
            url: api_url,
            async: false,
            contentType: "application/json;charset=utf-8",
            dataType: "json",
            success: function(data) {
                if (data.msg != 0){
                    var content = "该MAC已绑定地址：" + data.msg[0]['server_ip'];
                    $("#mac_select").attr('data-content', content);
                    $("#mac_select").popover('show');
                }else{
                    $("#mac_select").attr('data-content', '该mac 未绑定地址');
                    $("#mac_select").popover('show');
                }

            },
            error: function(data, status) {
                alert(status);
            }
        });
    }

}

function update_dhcp_map(manager_ip, server_ip, mac_address, server_id){

    var update_flag = false;
    var post_json = JSON.stringify({
        "manager_ip": manager_ip,
        "server_ip": server_ip,
        "mac_address": mac_address,
        "server_id": server_id
    });
    var api_url = api_server_url + "/api/async/v1/dhcp/map";
    $.ajax({
        type: "POST",
        url: api_url,
        async: false,
        data: post_json,
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function(data) {
            update_flag = true;
        },
        error: function(data, status) {
            alert(data);
        }
    });
    return update_flag;
}

//mac done
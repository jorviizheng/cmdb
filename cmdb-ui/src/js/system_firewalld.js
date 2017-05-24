/**
 * Created by pippo on 2017/4/20.
 */

//firewall
function set_firewall_zone(){
    var firewall_zone_select = $("#firewall_zone_select");
    var firewall_type_select = $("#firewall_type_select");
    var firewall_btn = $("#firewall_btn");
    firewall_zone_select.empty();
    var result_group = $("#sync_result_show_list");
    result_group.empty();
    var line = "";
    var hosts = get_hosts_ip();

    if ( hosts.length > 1){
        line = "<button type=\"button\" class=\"list-group-item-danger\">防火墙暂不支持批量选择</button>";
        result_group.append(line);
        firewall_type_select.val(0);
        firewall_btn.attr('disabled',true);
    }else if(hosts.length == 0){
        line = "<button type=\"button\" class=\"list-group-item-danger\">未选择服务器，请选择</button>";
        result_group.append(line);
        firewall_type_select.val(0);
        firewall_btn.attr('disabled',true);
    }else{
        firewall_btn.attr('disabled',false);
        var post_json = JSON.stringify({
            'host':hosts
        });
        var api_url = api_server_url + "/api/sync/v1/firewalld/zone";
        $.ajax({
            type: "POST",
            url: api_url,
            data: post_json,
            contentType: "application/json;charset=utf-8",
            dataType: "json",
            async:false,
            success: function(data) {
                if (data.status == 0){
                    for(var i=0;i<data.msg[hosts[0]]['msg'].length;i++){
                        index = i + 1;
                        firewall_zone_select.append("<option  value=" + index + ">" + data.msg[hosts[0]]['msg'][i] + "</option>");
                    }
                    $("#firewall_btn").attr('disabled',false);
                }else{
                    // firewall_zone_select.append("<option  value=" + index + ">" + "获取主机zone失败，失败原因:"+ data.msg[hosts[0]]['msg'] + "</option>");
                    line = "<button type=\"button\" class=\"list-group-item-danger\">获取主机firewall zone失败，原因:"+ data.msg[hosts[0]]['msg'] +"</button>";
                    result_group.append(line);

                    $("#firewall_btn").attr('disabled',true);
                }
            },
            error: function(data) {
                alert(data);
                $("#firewall_btn").attr('disabled',true);
            }
        });
    }
}

function get_firewall_service(){
    var firewall_input = $("#firewall_input");
    var firewall_btn = $("#firewall_btn");
    var result_group = $("#sync_result_show_list");
    var firewall_type_select = $("#firewall_type_select");
    result_group.empty();
    var line = "";
    var hosts = get_hosts_ip();

    var post_json = JSON.stringify({
        'host':hosts
    });
    var api_url = api_server_url + "/api/sync/v1/firewalld/service";
    $.ajax({
        type: "POST",
        url: api_url,
        data: post_json,
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        async: false,
        success: function(data) {
            var host = data.msg[hosts[0]];
            if (data.status == 0){
                var firewall_list = $("#firewall_list");
                firewall_list.empty();

                for(var i=0;i<host['msg'].length;i++){
                    firewall_list.append("<option>"+host['msg'][i]+"</option>");
                }
                $("#firewall_btn").attr('disabled',false);
            }else{

                line = "<button type=\"button\" class=\"list-group-item-danger\">获取主机firewall service失败，原因:"+ host['msg'] +"</button>";
                result_group.append(line);
                $("#firewall_btn").attr('disabled',true);
            }
        },
        error: function(data) {
            var host = data.msg[hosts[0]];
            line = "<button type=\"button\" class=\"list-group-item-danger\">获取主机firewall service失败，原因:"+ host['msg'] +"</button>";
            result_group.append(line);
            $("#firewall_btn").attr('disabled',true);
        }
    });


}


function set_input_placeholder() {
    var firewall_type = $("#firewall_type_select option:selected");
    var firewall_input = $("#firewall_input");
    var result_group = $("#sync_result_show_list");
    var firewall_type_select = $("#firewall_type_select");
    var firewall_btn = $("#firewall_btn");

    result_group.empty();
    var line = "";
    var hosts = get_hosts_ip();

    if ( hosts.length > 1){
        line = "<button type=\"button\" class=\"list-group-item-danger\">防火墙暂不支持批量选择</button>";
        result_group.append(line);
        firewall_type_select.val(0);
        firewall_btn.attr('disabled',true);
    }else if(hosts.length == 0){
        line = "<button type=\"button\" class=\"list-group-item-danger\">未选择服务器，请选择</button>";
        result_group.append(line);
        firewall_type_select.val(0);
        firewall_btn.attr('disabled',true);
    }else {
        firewall_btn.attr('disabled',false);
        if (firewall_type.val() == 0){
            firewall_input.attr('placeholder','');
        }else if (firewall_type.val() == 1){
            firewall_input.attr('placeholder','like http(支持自动提示本服务器上的Firewall service)');
            get_firewall_service();
        }else if (firewall_type.val() == 2){
            firewall_input.attr('placeholder','like 80/tcp or 80-81/tcp or 80/udp or 80-81/udp');
        }else if (firewall_type.val()== 3){
            firewall_input.attr('placeholder','like 192.168.1.0/24');
        }else  if (firewall_type.val() == 4){
            firewall_input.attr('placeholder','直接选择action即可');
            firewall_input.attr("readonly","readonly");
        }
    }
}

function firewall_task() {

    var firewall_type_select = $("#firewall_type_select option:selected");
    var firewall_zone_select = $("#firewall_zone_select option:selected");
    var firewall_action_select = $("#firewalld_action_select option:selected");
    var firewall_input = $("#firewall_input").val();
    var firewall_permanent = "no";
    if ($("#permanent_checkbox").is(':checked')) {
        firewall_permanent = "yes";
    }
    var hosts = get_hosts_ip();
    var result_group = $("#sync_result_show_list");
    result_group.empty();
    var line = "";
    if (hosts.length == 0) {
        line = "<button type=\"button\" class=\"list-group-item-danger\">未选择服务器，请选择</button>";
        result_group.append(line);
        $("#firewall_type_select").val(0);
    } else if (hosts.length > 1) {
        line = "<button type=\"button\" class=\"list-group-item-danger\">防火墙暂不支持批量选择</button>";
        result_group.append(line);
        $("#firewall_type_select").val(0);
    } else {
        if (firewall_type_select.val() != 0
            && firewall_zone_select.val() !=0 && firewall_action_select.val() != 0) {

            if (firewall_input == "" && firewall_type_select.val() != 4){
                alert("规则不能为空");
            }else{


                var ansible_module = 'firewalld';
                var date = datetime_human();
                var user_name = $.cookie('unick');
                var task_name = user_name + '_' + 'ansible' + '_' + ansible_module + '_' + datetime_str();

                var task_args = new Object();
                task_args.host = hosts;
                task_args.module = ansible_module;
                task_args.state = firewall_action_select.text();
                task_args.permanent = firewall_permanent;

                if (firewall_type_select.val() == 1) {
                    task_args.service = firewall_input;
                } else if (firewall_type_select.val() == 2) {
                    task_args.port = firewall_input;
                } else if (firewall_type_select.val() == 3) {
                    task_args.source = firewall_input;
                } else if (firewall_type_select.val() == 4) {
                    task_args.masquerade = firewall_input;

                }

                var task_args_json = JSON.stringify(task_args);

                var task_type_json = JSON.stringify({
                    "type": "ansible"
                });

                var post_json = JSON.stringify({
                    "user_name": user_name,
                    "task_name": task_name,
                    "task_type": "timely",
                    "task_flag": task_type_json,
                    "task_args": task_args_json,
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
                    success: function (data) {
                        if (data.status == 1) {
                            alert("任务已添加，请到任务界面查看详细信息");
                        }
                        window.location.reload();
                    },
                    error: function (data) {
                        alert(data.msg);
                        window.location.reload();
                    }
                });
            }
        }else{
            alert("选择项错误");
        }
    }

}

//firewall done
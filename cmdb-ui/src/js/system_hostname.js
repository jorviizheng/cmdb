/**
 * Created by pippo on 2017/4/21.
 */
//hostname
function get_current_hostname(){
    var hosts = get_hosts_ip();
    var result_group = $("#sync_result_show_list");
    result_group.empty();
    var line = "";
    if (hosts.length > 1){
        line = "<button type=\"button\" class=\"list-group-item-danger\">主机名修改不支持批量选择</button>";
        result_group.append(line);
        $("#hostname_btn").attr('disabled',true);
    }else if(hosts.length == 0){
        line =  "<button type=\"button\" class=\"list-group-item-danger\">未选择服务器，请选择</button>";
        result_group.append(line);
    }else{
        $("#hostname_btn").attr('disabled',false);
        var post_json = JSON.stringify({
            'host':hosts
        });
        $.ajax({
            type: "POST",
            url:  api_server_url + "/api/sync/v1/hostname",
            data: post_json,
            contentType: "application/json;charset=utf-8",
            dataType: "json",
            async: false,
            success: function(data) {
                var host =  data.msg[hosts[0]];
                if (data.status == 0){
                    line =  "<button type=\"button\" class=\"list-group-item-success\">"+ select_server_list[0]+" 主机名为:"+ host['msg'] + "</button>";
                    $("#hostname_btn").attr('disabled',false);
                }else{
                    line =  "<button type=\"button\" class=\"list-group-item-danger\">"+ select_server_list[0] + " 主机名获取失败，失败原因:"+ host['msg'] + "</button>";
                    $("#hostname_btn").attr('disabled',true);
                }
                result_group.append(line);
            },
            error: function(data) {
                alert(data);
                $("#hostname_btn").attr('disabled',true);
            }
        });
    }
}

function hostname_task(){

    var hosts = get_hosts_ip();
    var result_group = $("#sync_result_show_list");
    result_group.empty();
    var line = "";
    if(hosts.length == 0){
        line =  "<button type=\"button\" class=\"list-group-item-danger\">未选择服务器，请选择</button>";
        result_group.append(line);
    }else if (hosts.length > 1) {
        line = "<button type=\"button\" class=\"list-group-item-danger\">主机名修改不支持批量选择</button>";
        result_group.append(line);
    }else{

        var host_name = $("#host_name_input").val();

        if (host_name != ""){
            var ansible_module = 'hostname';
            var date = datetime_human();
            var user_name = $.cookie('unick');
            var task_name = user_name + '_' + 'ansible'+ '_' + ansible_module + '_' + datetime_str();

            var task_args_json = JSON.stringify({
                'host': hosts,
                "host_name": host_name,
                "module": ansible_module
            });
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
            $.ajax({
                type: "POST",
                url: api_server_url + "/api/async/v1/tasks",
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
        }else{
            line = "<button type=\"button\" class=\"list-group-item-danger\">hostname 为空</button>";
            result_group.append(line);
        }
    }

}

// hostname done
/**
 * Created by pippo on 2017/4/24.
 */

var yum_source = new JSON.constructor();
//获取可用yum源
function get_yum_source() {
    var yum_source_select = $("#yum_source_select");
    $.ajax({
        type: "GET",
        url: api_server_url + "/api/sync/v1/yum/source/available",
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        // async: false,
        success: function(data, status) {
            if (data.status == 302) {
                window.location.href = '../pages/login.html';
            }else if(data.status == 0){
                yum_source = data.msg;
                //设置yum源选择框
                var select_str = "<option selected='selected' value=0>请选择..</option>";
                yum_source_select.empty();
                var index = 1;
                yum_source_select.append(select_str);
                for(var key in yum_source){

                    index++;
                    if(key != 'base_url')
                    {
                        yum_source_select.append("<option  value=" + index + ">" + key + "</option>");
                    }
                }
                //设置软件包版本选择框
                set_package_input_list();
            }
        },
        error: function(data) {
            alert(data.msg);
        }
    });
    // return yum_source_list;
}

//source
function yum_source_task() {
    var source_name = $('#yum_source_select option:selected').text();
    var source_action = $('#yum_source_action_select option:selected').val();
    var base_url = yum_source['base_url'] + '/' + source_name;
    var result_group = $("#sync_result_show_list");
    result_group.empty();
    var line = "";

    var hosts = get_hosts_ip();
    if(hosts.length == 0){
        line =  "<button type=\"button\" class=\"list-group-item-danger\">未选择服务器，请选择</button>";
        result_group.append(line);
        $("#yum_source_select").val(0);
    }else if (hosts.length > 1) {
        var os_version_equal = check_servers_os_version_equal();

        if (! os_version_equal){
            line =  "<button type=\"button\" class=\"list-group-item-danger\">已选择服务器系统版本不一致，无法进行批量处理</button>";
            result_group.append(line);
            $("#yum_source_select").val(0);

        }else {
            if ( source_name != "" && source_action !=0){
                var action = "";
                if (source_action == 1){
                    action = "present";
                }else if (source_action == 2){
                    action = "absent";
                }

                var ansible_module = 'yum_repo';

                var date = datetime_human();
                var user_name = $.cookie('unick');
                var task_name = user_name + '_' + 'ansible_yum_source_'+ user_name + '_' + ansible_module + '_' + datetime_str();

                var task_args_json = JSON.stringify({
                    'host': hosts,
                    'name': source_name,
                    'state': action,
                    'description': 'local',
                    'enabled': '1',
                    'gpgcheck': '0',
                    'baseurl': base_url,
                    "module": ansible_module
                });
                var task_type_json = JSON.stringify({
                    "type": "ansible",
                    "action": action
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
                    success: function(data) {
                        if (data.status == 1) {
                            alert("任务已添加，请到任务界面查看详细信息");
                        }
                        window.location.reload();
                    },
                    error: function(data) {
                        alert(data.msg);
                        window.location.reload();
                    }
                });
            }else {
                alert("选择项错误");
                line =  "<button type=\"button\" class=\"list-group-item-danger\">选择项错误</button>";
                result_group.append(line);
                package_btn.attr("disabled",true);
                $("#yum_source_select").val(0);
            }

        }
    }


}
//查询各服务器上软件源安装情况
function check_yum_resource_installed() {

    var source_name = $('#yum_source_select option:selected').text();
    var source_btn = $("#source_btn");

    var result_group = $("#sync_result_show_list");
    result_group.empty();
    var line = "";

    var hosts = get_hosts_ip();
    if(hosts.length == 0){
        line =  "<button type=\"button\" class=\"list-group-item-danger\">未选择服务器，请选择</button>";
        result_group.append(line);
        $("#yum_source_select").val(0);
        source_btn.attr("disabled",true);
    }else{
        var os_version_equal = check_servers_os_version_equal();
        if (! os_version_equal){
            line =  "<button type=\"button\" class=\"list-group-item-danger\">已选择服务器系统版本不一致，无法进行批量处理</button>";
            result_group.append(line);
            source_btn.attr("disabled",true);
            $("#yum_source_select").val(0);
        }else{
            source_btn.attr("disabled",false);
            var post_json = JSON.stringify({
                'host': hosts,
                'source_name': source_name
            });

            $.ajax({
                type: "POST",
                url: api_server_url + "/api/sync/v1/yum/source/installed",
                data: post_json,
                contentType: "application/json;charset=utf-8",
                dataType: "json",
                success: function (data) {

                    for (var i=0;i<select_server_list.length;i++){
                        var host_name = select_server_list[i];
                        var source_info = data.msg[hosts[i]];


                        if (source_info['status'] > 0) {
                            if (source_info["status"] == 4) {
                                line = "<button type=\"button\" class=\"list-group-item-danger\">" + host_name + " 获取失败，原因" + source_info["msg"] + "</button>";
                            } else {
                                //安装过了
                                line = "<button type=\"button\" class=\"list-group-item-danger\">" + host_name + " 未安装源" + source_name + "</button>";
                            }
                        }else if (source_info["status"] == 0){
                            line =  "<button type=\"button\" class=\"list-group-item-success\">" + host_name + " 已安装源:" + source_name+ "</button>";
                        }else {

                        }
                        result_group.append(line);
                    }
                },
                error: function (data) {
                    line =  "<button type=\"button\" class=\"list-group-item-danger\">后台服务错误，稍后尝试</button>";
                    result_group.append(line);
                    package_btn.attr("disabled",true);
                    $('#package_input').val("");
                    window.location.reload();
                }
            });
        }


    }
}

//source done

//package
//设置软件版本选择框
function set_package_version_select(package_name){
    var package_version_select = $("#yum_package_version_select");

    //set package version list
    package_version_select.empty();
    package_version_select.append("<option selected='selected'  value=0>请选择..</option>");
    $.each(yum_source, function (source_key, sources) {
        if(source_key != "base_url"){
            $.each(sources,function (source,version_list) {
                if (source == package_name){
                    for (var version_index=0;version_index<version_list.length;version_index++){
                        if (typeof version_list[version_index] == 'undefined'){
                            package_version_select.append("<option  value=" + version_index + ">" + "latest" + "</option>");
                        }else{
                            package_version_select.append("<option  value=" + version_index + ">" + version_list[version_index]+ "</option>");
                        }
                    }

                }
            })
        }
    });
}
//获取安装包位于哪个软件源中
function get_package_source(package_name) {
    var source_name = "";
    $.each(yum_source, function (source_key, sources) {
        if(source_key != "base_url"){
            $.each(sources,function (source) {
                if (source == package_name){
                    source_name = source_key;
                }
            })
        }
    });
    return source_name;
}

//设置软件输入框的提示
function set_package_input_list() {
    var package_list = $('#package_list');
    package_list.empty();
    $.each(yum_source, function (source_key, sources) {
        if(source_key != "base_url"){
            $.each(sources,function (source) {
                package_list.append("<option>"+ source+"</option>");
            })
        }
    });
}

function yum_package_task() {
    var package_input_name = $('#package_input').val().split('.')[0];
    var package_version = $('#yum_package_version_select option:selected').text();
    var package_action = $('#yum_package_action_select option:selected').val();
    var package_name = "";

    var hosts = get_hosts_ip()
    var result_group = $("#sync_result_show_list");
    result_group.empty();
    var line = "";

    if(hosts.length == 0){
        line ="<button type=\"button\" class=\"list-group-item-danger\">未选择服务器，请选择</button>";
        result_group.append(line);
        $('#package_input').val("");
    }else if (hosts.length > 1) {
        var os_version_equal = check_servers_os_version_equal();

        if (!os_version_equal) {
            line ="<button type=\"button\" class=\"list-group-item-danger\">已选择服务器系统版本不一致，无法进行批量处理</button>";
            result_group.append(line);
            $('#package_input').val("");
        } else {

            if (package_version == "latest"){
                package_name = package_input_name;
            }else{
                package_name = package_input_name + '-' + package_version;
            }

            if (package_name != "" && package_version !="" && package_action != 0) {
                var action = "";
                if (package_action == 1) {
                    action = "present";
                } else if (package_action == 2) {
                    action = "absent";
                } else if (package_action == 3) {
                    action = "last"
                }else{

                }
                var ansible_module = 'yum';

                var date = datetime_human();
                var user_name = $.cookie('unick');
                var task_name = user_name + '_' + 'ansible_yum_package_'+ user_name + '_' + ansible_module + '_' + datetime_str();

                var task_arg_json = JSON.stringify({
                    "package_name": package_name,
                    "host": hosts,
                    "state": action,
                    "module": ansible_module
                });
                var task_type_json = JSON.stringify({
                    "type": "ansible",
                    "action": action
                });

                var post_json = JSON.stringify({
                    "user_name": user_name,
                    "task_name": task_name,
                    "task_type": "timely",
                    "task_flag": task_type_json,
                    "task_args": task_arg_json,
                    "create_time": date,
                    "update_time": date
                });

                $.ajax({
                    type: "POST",
                    url: api_server_url + "/api/async/v1/tasks",
                    data: post_json,
                    contentType: "application/json;charset=utf-8",
                    dataType: "json",
                    success: function (data, status) {
                        if (data.status == 1) {
                            alert("任务已添加，请到任务界面查看详细信息");
                            window.location.reload();
                        }
                    },
                    error: function (data, status) {
                        alert(data.msg);
                        window.location.reload();
                    }
                });
            }else{
                line ="<button type=\"button\" class=\"list-group-item-danger\">选择项错误</button>";
                result_group.append(line);
                $('#package_input').val("");
            }
        }

    }
}

//检测服务器端软件包安装状态
function check_server_package_installed() {

    var package_name = $('#package_input').val();

    //设置版本选择框
    set_package_version_select(package_name);

    var os_version_equal = check_servers_os_version_equal();
    var package_btn = $("#package_btn");
    var result_group = $("#sync_result_show_list");
    result_group.empty();
    var line = "";
    var hosts = get_hosts_ip();
    if(hosts.length == 0){
        line =  "<button type=\"button\" class=\"list-group-item-danger\">未选择服务器，请选择</button>";
        result_group.append(line);
        package_btn.attr("disabled",true);
        $('#package_input').val("");
    }else {
        if (! os_version_equal){
            line =  "<button type=\"button\" class=\"list-group-item-danger\">已选择服务器系统版本不一致，无法进行批量处理</button>";
            result_group.append(line);
            package_btn.attr("disabled",true);
            $('#package_input').val("");
        }else{

            var source_name = get_package_source(package_name);

            if (source_name == ""){
                line =  "<button type=\"button\" class=\"list-group-item-danger\">软件名为空</button>";
                result_group.append(line);
                package_btn.attr("disabled",true);
            }else{
                package_btn.attr("disabled",false);


                var package_json = JSON.stringify({
                    'host':hosts,
                    'package_name': package_name
                });

                $.ajax({
                    type: "POST",
                    url: api_server_url + "/api/sync/v1/yum/package/installed",
                    data: package_json,
                    contentType: "application/json;charset=utf-8",
                    dataType: "json",
                    async:false,
                    success: function(data) {

                        for (var i=0;i<select_server_list.length;i++){
                            var host_name = select_server_list[i];
                            var package_info = data.msg[hosts[i]];
                            if (package_info['status'] > 0){

                                if (package_info["status"] == 4) {
                                    line = "<button type=\"button\" class=\"list-group-item-danger\">" + host_name + " 获取失败，原因" + package_info["msg"] + "</button>";
                                }else{
                                    line =  "<button type=\"button\" class=\"list-group-item-danger\">" + host_name + " 未安装 " + package_name + "</button>";
                                }
                            }else if (package_info["status"] == 0){
                                line =  "<button type=\"button\" class=\"list-group-item-success\">" + host_name + " 已安装版本:" + package_info['msg']['version']+ "</button>";
                            }
                            result_group.append(line);
                        }
                    },
                    error: function() {
                        line =  "<button type=\"button\" class=\"list-group-item-danger\">后台服务错误，稍后尝试</button>";
                        result_group.append(line);
                        package_btn.attr("disabled",true);
                        $('#package_input').val("");
                    }
                });
            }
        }

    }
}


//判断服务器上是否拥有已选择软件包的源
function check_server_has_source() {

    var package_btn = $("#package_btn");

    var package_name = $('#package_input').val();
    var source_name = get_package_source(package_name);
    var result_group = $("#sync_result_show_list");
    result_group.empty();

    var line = "";
    //检查软件包是否可以安装
    var hosts = get_hosts_ip();
    if(hosts.length == 0){
        line =  "<button type=\"button\" class=\"list-group-item-danger\">未选择服务器，请选择</button>";
        result_group.append(line);
    }else{
        var os_version_equal = check_servers_os_version_equal();
        if (! os_version_equal){
            line =  "<button type=\"button\" class=\"list-group-item-danger\">已选择服务器系统版本不一致，无法进行批量处理</button>";
            result_group.append(line);
            package_btn.attr("disabled",true);
        }else{
            package_btn.attr("disabled",false);
            var post_json = JSON.stringify({
                'host': hosts,
                'source_name': '*'
            });

            $.ajax({
                type: "POST",
                url: api_server_url + "/api/sync/v1/yum/source/installed/list",
                data: post_json,
                contentType: "application/json;charset=utf-8",
                dataType: "json",
                success: function(data) {
                    if (data.status == 0){
                        if (data.msg != 0){
                            for (var i=0;i<select_server_list.length;i++){
                                var host_name = select_server_list[i];
                                var installed_source_list = data.msg[hosts[i]]['msg'];
                                var has_source = false;
                                for (var j=0;j<installed_source_list.length;j++){
                                    if (source_name == installed_source_list[j]){
                                        has_source = true;
                                        break;
                                    }
                                }
                                if (has_source){
                                    line =  "<button type=\"button\" class=\"list-group-item-success\">" + host_name + "可安装" + "</button>";
                                }else{
                                    line =  "<button type=\"button\" class=\"list-group-item-danger\">" + host_name + "缺少对应源:" + source_name + "</button>";

                                }
                                result_group.append(line);
                            }
                        }
                    }
                },
                error: function(data) {
                    line =  "<button type=\"button\" class=\"list-group-item-danger\">后台服务错误，稍后尝试</button>";
                    result_group.append(line);
                    package_btn.attr("disabled",true);
                    $('#package_input').val("");
                }
            });
        }
    }



}
//package done
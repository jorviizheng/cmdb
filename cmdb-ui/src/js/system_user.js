/**
 * Created by pippo on 2017/3/31.
 */

$(function() {
    // show_server_name($("#system_del_user_server_name_select"));
    show_server_name($("#system_add_user_server_name_select"));
    show_server_name($("#system_update_user_server_name_select"));



    //用户
    check_system_user_exist();

    check_password();

});

//user
//批量获取用户查询结果
function check_system_user_exist(){

    //新增检查
    $("#system_add_username_input").blur(function(){
        var system_user_name_input = $("#system_add_username_input");
        var hosts = get_hosts_ip();
        var user_group = $("#sync_result_show_list");
        user_group.empty();
        var system_users = get_system_user_list();
        if (system_users!= ""){
            var line = "";
            for(var i=0;i<select_server_list.length;i ++){
                var host_name = select_server_list[i];
                var host_user = system_users[hosts[i]];
                if (host_user['status'] == 4){
                    line =  "<button type=\"button\" class=\"list-group-item-danger\">" + host_name + "获取失败，原因：" + host_user['msg']+ "</button>";
                }else{
                    if (host_user['msg'].length == 0){
                        line =  "<button type=\"button\" class=\"list-group-item-success\">" + host_name + "不存在该用户" + "</button>";
                    }else{
                        var user_exist = false;
                        for(var j=0;j<host_user['msg'].length;j++){
                            if (host_user['msg'][j] == system_user_name_input.val()){
                                user_exist = true;
                            }
                        }
                        if (user_exist){
                            line = "<button type=\"button\" class=\"list-group-item-danger\">" + host_name + "存在该用户" + "</button>";
                        }else{
                            line =  "<button type=\"button\" class=\"list-group-item-success\">" + host_name + "不存在该用户" + "</button>";
                        }

                    }
                }


                user_group.append(line);
            }
        }
    });

    //删除检查
    $("#system_del_username_input").blur(function(){
        var system_user_name_input = $("#system_del_username_input");
        var hosts = get_hosts_ip();
        var user_group = $("#sync_result_show_list");
        user_group.empty();
        var system_users = get_system_user_list();
        if (system_users!= ""){
            var line = "";
            for(var i=0;i<select_server_list.length;i ++){
                var host_name = select_server_list[i];
                var host_user = system_users[hosts[i]];
                if (host_user['msg'].length == 0){
                    line =  "<button type=\"button\" class=\"list-group-item-danger\">" + host_name + "不存在该用户" + "</button>";
                }else{
                    var user_exist = false;
                    for(var j=0;j<host_user['msg'].length;j++){
                        if (host_user['msg'][j] == system_user_name_input.val()){
                            user_exist = true;
                        }
                    }
                    if (user_exist){
                        line = "<button type=\"button\" class=\"list-group-item-success\">" + host_name + "存在该用户" + "</button>";
                    }else{
                        line =  "<button type=\"button\" class=\"list-group-item-danger\">" + host_name + "不存在该用户" + "</button>";
                    }

                }
                user_group.append(line);
            }
        }
    });


    //更新密码检查
    $("#system_update_username_input").blur(function(){
        var system_user_name_input = $("#system_update_username_input");
        var hosts = get_hosts_ip();
        var user_group = $("#sync_result_show_list");
        user_group.empty();
        var system_users = get_system_user_list();
        if (system_users!= ""){
            var line = "";
            for(var i=0;i<select_server_list.length;i ++){
                var host_name = select_server_list[i];
                var host_user = system_users[hosts[i]];
                if (host_user['msg'].length == 0){
                    line =  "<button type=\"button\" class=\"list-group-item-danger\">" + host_name + "不存在该用户" + "</button>";
                }else{
                    var user_exist = false;
                    for(var j=0;j<host_user['msg'].length;j++){
                        if (host_user['msg'][j] == system_user_name_input.val()){
                            user_exist = true;
                        }
                    }
                    if (user_exist){
                        line = "<button type=\"button\" class=\"list-group-item-success\">" + host_name + "存在该用户" + "</button>";
                    }else{
                        line =  "<button type=\"button\" class=\"list-group-item-danger\">" + host_name + "不存在该用户" + "</button>";
                    }

                }

                user_group.append(line);
            }
        }
    });

}

//获取选中服务器上的用户列表
function get_system_user_list(){
    var host = new Array();
    for(var i=0;i<select_server_list.length;i ++){
        host.push(get_host_ip(select_server_list[i]));
    }

    var post_json = JSON.stringify({
        'host':host
    });

    var system_users = '';

    $.ajax({
        type: "POST",
        url: "http://cmdb.wanda.cn/api/sync/v1/system/users",
        data: post_json,
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        async: false,
        success: function(data) {
            system_users = data.msg;
        },
        error: function(data) {
            alert('获取主机用户名列表失败，原因:'+ data.msg);
        }
    });
    return system_users;
}

//密码校验
function check_password_equal(first_input, last_input, btn){
    if (first_input.val() != "" && last_input.val() != ""){
        if (first_input.val() != last_input.val()){
            alert("两次密码不一致");
            btn.attr("disabled",true);
            return false;
        }else{
            btn.attr("disabled",false);
            return true;
        }
    }


}

function check_password(){
    $("#system_add_userpassword_input").blur(function () {
        check_password_equal($("#system_add_userpassword_input"), $("#system_add_userpassword_check_input"), $("#system_add_user_btn"))
    });

    $("#system_add_userpassword_check_input").blur(function () {
        check_password_equal($("#system_add_userpassword_input"), $("#system_add_userpassword_check_input"), $("#system_add_user_btn"))
    });


    $("#system_update_userpassword_input").blur(function () {
        check_password_equal($("#system_update_userpassword_input"), $("#system_update_userpassword_check_input"), $("#system_update_user_btn"))
    });

    $("#system_update_userpassword_check_input").blur(function () {
        check_password_equal($("#system_update_userpassword_input"), $("#system_update_userpassword_check_input"), $("#system_update_user_btn"))
    });
}

//新增user
function add_system_user(){
    var system_user_name = $("#system_add_username_input").val();
    var system_user_password_input = $("#system_add_userpassword_input").val();
    var system_user_password_check_input = $("#system_add_userpassword_check_input").val();
    var hosts = new Array();
    hosts = get_hosts_ip();

    if (hosts.length != 0 && system_user_name != "" &&
        system_user_password_input!=0 &&
        system_user_password_check_input != ""){

        var system_user_password = sha512crypt(system_user_password_input,'$6$rounds=5000$salt');

        var ansible_module = 'user';
        var date = datetime_human();
        var user_name = $.cookie('unick');
        var task_name = user_name + '_' + 'ansible_add_system_user_'+ system_user_name + '_' + ansible_module + '_' + datetime_str();



        var task_args_json = JSON.stringify({
            'host': hosts,
            "name": system_user_name,
            "password":system_user_password,
            "module": ansible_module,
            'state': "present"
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


        var api_url = api_server_url + "/api/async/v1/tasks";
        $.ajax({
            type: "POST",
            url: api_url,
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
    }else{
        alert("未选择服务器或者输入信息为空");
        window.location.reload();
    }
}
//删除用户
function del_system_user(){

    var system_user_name = $("#system_del_username_input").val();
    var hosts = new Array();
    hosts = get_hosts_ip();

    if (hosts.length != 0 && system_user_name != ""){

        var ansible_module = 'user';
        var date = datetime_human();
        var user_name = $.cookie('unick');
        var task_name = user_name + '_' + 'ansible'+ '_del_user_'+ system_user_name + "_"+ ansible_module + '_' + datetime_str();

        var task_args_json = JSON.stringify({
            'host': hosts,
            "name": system_user_name,
            "module": ansible_module,
            'state': "absent"
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


        var api_url = api_server_url + "/api/async/v1/tasks";
        $.ajax({
            type: "POST",
            url: api_url,
            data: post_json,
            contentType: "application/json;charset=utf-8",
            dataType: "json",
            success: function(data) {
                if (data.status == 1) {
                    alert("任务已添加，请到任务界面查看详细信息");
                }
                window.location.reload();
            },
            error: function(data, status) {
                alert(data.msg);
                window.location.reload();
            }
        });
    }else{
        alert("用户名为空或未选择服务器");
        window.location.reload();
    }
}
//更新密码
function update_user_password(){

    var system_user_name = $("#system_update_username_input").val();
    var system_user_password_input = $("#system_update_userpassword_input").val();
    var system_user_password_check_input = $("#system_update_userpassword_check_input").val();

    var hosts = new Array();
    hosts = get_hosts_ip();

    if (hosts.length != 0 && system_user_name != "" &&
        system_user_password_input!=0 &&
        system_user_password_check_input != ""){

        var system_user_password = sha512crypt(system_user_password_input,'$6$rounds=5000$salt');

        var ansible_module = 'user';
        var date = datetime_human();
        var user_name = $.cookie('unick');
        var task_name = user_name + '_' + 'ansible_update_user_'+ system_user_name +'_password_' + ansible_module + '_' + datetime_str();

        var task_args_json = JSON.stringify({
            'host': hosts,
            "name": system_user_name,
            "password":system_user_password,
            "module": ansible_module,
            "state": "update",
            "update_password": "yes"
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


        api_url = "http://cmdb.wanda.cn/api/async/v1/tasks";
        $.ajax({
            type: "POST",
            url: api_url,
            data: post_json,
            contentType: "application/json;charset=utf-8",
            dataType: "json",
            success: function(data) {
                if (data.status == 1) {
                    alert("任务已添加，请到任务界面查看详细信息");
                }
                window.location.reload();
            },
            error: function(data, status) {
                alert(data.msg);
                window.location.reload();
            }
        });
    }else{
        alert("输入错误或未选择服务器");
        window.location.reload();
    }
}
//user done

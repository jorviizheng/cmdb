function get_current_tags(){var e=$("#tag_server_select option:selected"),a=api_server_url+"/api/async/v1/server/info?condition=server_name&&value="+e.text(),t=$("#tag_server_list");t.empty(),$.ajax({url:a,method:"GET",success:function(e){var a=e.msg.tag.split(",");for(i=0;i<a.length;i++)index=i+1,t.append('<li class="list-group-item">'+a[i]+"</li>")}})}function tag_action(){var e=$("#tag_server_select option:selected"),a=$("#tag_name_input").val(),t=$("#tag_action_select option:selected");if(0==e.val()||0==t.val())alert("选择项不正确");else if(1==t.val()){var r=api_server_url+"/api/async/v1/tag/server/"+a,s=JSON.stringify({name:e.text()});$.ajax({type:"POST",url:r,contentType:"application/json;charset=utf-8",dataType:"json",data:s,success:function(e){e.status<0?alert("操作失败"):alert("标记成功"),window.location.reload()},error:function(e){alert("标记失败，失败原因:"+e.msg),window.location.reload()}})}else if(2==t.val()){var n=api_server_url+"/api/async/v1/tag/server/"+a,i=JSON.stringify({name:e.text()});$.ajax({type:"PATCH",url:n,contentType:"application/json;charset=utf-8",dataType:"json",data:i,success:function(e){e.status<0?alert("操作失败"):alert("标记成功"),window.location.reload()},error:function(e){alert(e.msg),window.location.reload()}})}}function submit_server(){var e=$("#server_name").val(),a=$("#manager_ip").val(),t=$("#server_ip option:selected").val(),r=$("#server_idc option:selected").val(),s=$("#pxe_template_select option:selected").val(),n=$("#server_group").val(),i=$("#action_select option:selected").val(),o=$("#dhcp_server_select option:selected").val(),p=$("#mac_select option:selected").val();""!=e&&""!=a&&0!=t&&0!=r&&""!=n&&0!=s&&0!=o&&0!=p?1==i?add_server():2==i&&reinstall_server():alert("选择项错误或者字段为空")}function add_server(){var e=$("#server_name").val(),a=$("#manager_ip").val(),t=$("#mac_select option:selected").text(),r=$("#server_ip option:selected").text(),s=$("#server_idc option:selected").val(),n=$("#server_group").val(),i=$("#pxe_template_select option:selected").text(),o=get_pxe_pt_id(i),p=$("#dhcp_server_select option:selected").val(),c=JSON.stringify({server_name:e,manager_ip:a,server_ip:r,server_group:n,idc_id:s,pt_id:o,status:"当前不可用",system_type:i,dhcp_server_id:p}),_=api_server_url+"/api/async/v1/servers";$.ajax({type:"POST",url:_,data:c,contentType:"application/json;charset=utf-8",dataType:"json",success:function(s){if(0==s.status){update_dhcp_map(a,r,t,get_server_id(e))&&add_server_task(e,a,r,t)}else alert("新增错误："+s.msg)},error:function(e,a){alert("新增错误："+a),window.location.reload()}})}function reinstall_server(){var e=$("#server_name").val(),a=$("#manager_ip").val(),t=$("#mac_select option:selected").text(),r=$("#server_ip option:selected").text(),s=$("#server_idc option:selected").val(),n=$("#server_group").val(),i=$("#pxe_template_select option:selected").text(),o=get_pxe_pt_id(i),p=$("#dhcp_server_select option:selected").val(),c=get_server_id(e),_=JSON.stringify({server_name:e,manager_ip:a,server_ip:r,server_group:n,idc_id:s,pt_id:o,status:"等待重新安装",system_type:i,dhcp_server_id:p});if(update_dhcp_map(a,r,t,c)){var l=api_server_url+"/api/async/v1/servers";$.ajax({type:"PATCH",url:l,data:_,contentType:"application/json;charset=utf-8",dataType:"json",success:function(s){0==s.status?reinstall_server_task(e,a,r,t):alert("重装错误："+s.msg)},error:function(e,a){alert("重装错误："+a),window.location.reload()}})}}function add_server_task(e,a,t,r){var s=Base64.encode("password"),n=datetime_human(),i=$.cookie("unick"),o=i+"_install_new_server_"+e+"_"+datetime_str(),p=JSON.stringify({server_name:e,manager_ip:a,ilo4_user_name:"admin",ilo4_user_passwd:s,server_ip:t,mac_address:r}),c=JSON.stringify({type:"server",action:"add"}),_=JSON.stringify({user_name:i,task_name:o,task_type:"timely",task_flag:c,task_args:p,create_time:n,update_time:n}),l=api_server_url+"/api/async/v1/tasks";$.ajax({type:"POST",url:l,data:_,contentType:"application/json;charset=utf-8",dataType:"json",success:function(e,a){1==e.status&&alert("任务已添加，请到任务界面查看详细信息"),window.location.reload()},error:function(e,a){alert(a),window.location.reload()}})}function reinstall_server_task(e,a,t,r){var s=Base64.encode("password"),n=datetime_human(),i=$.cookie("unick"),o=i+"_reship_old_server_"+e+"_"+datetime_str(),p=JSON.stringify({server_name:e,manager_ip:a,ilo4_user_name:"admin",ilo4_user_passwd:s,server_ip:t,mac_address:r}),c=JSON.stringify({type:"server",action:"reinstall"}),_=JSON.stringify({user_name:i,task_name:o,task_type:"timely",task_flag:c,task_args:p,create_time:n,update_time:n}),l=api_server_url+"/api/async/v1/tasks";$.ajax({type:"POST",url:l,data:_,contentType:"application/json;charset=utf-8",dataType:"json",success:function(e,a){1==e.status&&alert("任务已添加，请到任务界面查看详细信息"),window.location.reload()},error:function(e,a){alert(a),window.location.reload()}})}function check_server_exist(){var e=$("#server_name").val();return api_url=api_server_url+"/api/async/v1/server/info?condition=server_name&&value="+e,exist=!0,$.ajax({type:"GET",url:api_url,contentType:"application/json;charset=utf-8",dataType:"json",success:function(e){var a=$("#action_select");a.empty(),a.append("<option selected='selected'  value=0>请选择..</option>"),e.status<0?alert(e.msg):0==e.msg?($("#manager_ip").attr("readonly",!1),$("#manager_ip").val(""),$("#mac_select").empty(),a.append("<option value=1>新装</option>")):($("#manager_ip").val(e.msg.manager_ip),$("#manager_ip").attr("readonly","readonly"),$("#after_manager_ip").attr("disabled",!1),a.append("<option value=2>重装</option>"),get_mac_addr_list())},error:function(e,a){alert(a)}}),exist}function check_manager_ip_exist(){$("#manager_ip").blur(function(){var e=$("#manager_ip").val(),a=api_server_url+"/api/async/v1/server/info?condition=manager_ip&&value="+e;$.ajax({type:"GET",url:a,contentType:"application/json;charset=utf-8",dataType:"json",success:function(e){var a=$("#action_select");a.empty(),a.append("<option selected='selected'  value=0>请选择..</option>"),e.status<0?alert(e.msg):(get_mac_addr_list(),0==e.msg?a.append("<option value=1>新装</option>"):a.append("<option value=2>重装</option>"))},error:function(e,a){alert(a)}})})}function get_dhcp_range_ip(){var e=$("#dhcp_server_select");e.blur(function(){var a=e.val();if(0!=a){var t=api_server_url+"/api/async/v1/dhcp/range/"+a;$.ajax({type:"GET",url:t,async:!1,contentType:"application/json;charset=utf-8",dataType:"json",success:function(e){var a=e.msg;$("#server_ip").empty(),$("#server_ip").append("<option selected='selected'  value=0>请选择..</option>");for(var t=1;t<a.length;t++)$("#server_ip").append("<option  value="+t+">"+a[t]+"</option>")},error:function(e,a){alert(a)}})}})}function get_dhcp_range(){var e=api_server_url+"/api/async/v1/dhcp/servers";$.ajax({type:"GET",url:e,async:!1,contentType:"application/json;charset=utf-8",dataType:"json",success:function(e){var a=e.msg,t=$("#dhcp_server_select");t.empty(),t.append("<option selected='selected'  value=0>请选择..</option>");for(var r=0;r<e.msg.length;r++)t.append("<option  value="+a[r].dhcp_server_id+">"+a[r].dhcp_subnet+"</option>")},error:function(e,a){alert(e.msg)}})}function disable(){var e=$("#manager_ip").val();"172.16.250.23"==e||"172.16.250.24"==e||"172.16.250.22"==e||"172.16.250.31"==e||"172.16.250.32"==e||"172.16.250.21"==e?($("#after_manager_ip").attr("disabled",!1),$("#submit_server_btn").attr("disabled",!1)):(alert("Not Allowed"),$("#server_ip").empty(),$("#submit_server_btn").attr("disabled",!0),$("#after_manager_ip").attr("disabled",!0))}function get_server_id(e){var a=0,t=api_server_url+"/api/async/v1/server/info?condition=server_name&&value="+e;return $.ajax({type:"GET",url:t,async:!1,contentType:"application/json;charset=utf-8",dataType:"json",success:function(e){0!=e.msg&&(a=e.msg.server_id)},error:function(e,a){alert(a)}}),a}function get_pxe_template(){var e=api_server_url+"/api/async/v1/pxe/names";$.ajax({type:"GET",url:e,async:!1,contentType:"application/json;charset=utf-8",dataType:"json",success:function(e){pxe_templates=e.msg;var a=$("#pxe_template_select");a.empty(),a.append("<option selected='selected'  value=0>请选择..</option>");for(var t=0;t<e.msg.length;t++)index=t+1,a.append("<option  value="+index+">"+e.msg[t].pxe_name+"</option>")},error:function(e,a){alert(a)}})}function get_pxe_pt_id(e){for(var a=0;a<pxe_templates.length;a++)if(e==pxe_templates[a].pxe_name)return pxe_templates[a].pt_id}function get_mac_addr_list(){var e=$("#manager_ip").val(),a=api_server_url+"/api/sync/v1/hardware/mac_addr/"+e;$("#submit_server_btn");$.ajax({type:"GET",url:a,contentType:"application/json;charset=utf-8",dataType:"json",success:function(e){if(0==e.status){var a=$("#mac_select");a.empty(),a.append("<option selected='selected'  value=0>请选择..</option>");for(var t=0,r=0;r<e.msg.length;r++)t=r+1,a.append("<option  value="+t+">"+e.msg[r]+"</option>");$("#submit_server_btn").attr("disabled",!1)}else alert(e.msg),$("#submit_server_btn").attr("disabled",!0)},error:function(e,a){alert(a)}})}function get_mac_map(){var e=$("#mac_select option:selected");if(0!=e.val()){var a=e.text(),t=api_server_url+"/api/async/v1/dhcp/map?mac_addr="+a;$.ajax({type:"GET",url:t,async:!1,contentType:"application/json;charset=utf-8",dataType:"json",success:function(e){if(0!=e.msg){var a="该MAC已绑定地址："+e.msg[0].server_ip;$("#mac_select").attr("data-content",a),$("#mac_select").popover("show")}else $("#mac_select").attr("data-content","该mac 未绑定地址"),$("#mac_select").popover("show")},error:function(e,a){alert(a)}})}}function update_dhcp_map(e,a,t,r){var s=!1,n=JSON.stringify({manager_ip:e,server_ip:a,mac_address:t,server_id:r}),i=api_server_url+"/api/async/v1/dhcp/map";return $.ajax({type:"POST",url:i,async:!1,data:n,contentType:"application/json;charset=utf-8",dataType:"json",success:function(e){s=!0},error:function(e,a){alert(e)}}),s}var pxe_templates=new Array;$(function(){show_server_name($("#tag_server_select")),check_manager_ip_exist(),get_pxe_template(),get_dhcp_range(),get_dhcp_range_ip()});
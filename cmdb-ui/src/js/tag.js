/**
 * Created by pippo on 2017/3/16.
 */

function add_tag() {
    t_name = $("#tag_name_input").val();
    post_json = JSON.stringify({
       't_name': t_name
    });
    api_url = api_server_url + '/api/async/v1/tags';
    $.ajax({
        url: api_url,
        method: 'POST',
        data: post_json,
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        error: function(data, status) {
            alert(status);
        }
    });

}

function delete_tag() {
    t_name = $("#tag_name_input").val();
    api_url = api_server_url + '/api/async/v1/tags' + "?t_name=" + t_name;
    $.ajax({
        url: api_url,
        method: 'DELETE',
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function (data) {
            if (data.code == 1){
                $("#tag_name_input").popover({
                    title:'错误',
                    content: data.msg,
                    placement: 'top',
                    manual: true
                });
                $("#tag_name_input").popover('show');
            }
        },
        error: function(data) {
            $("#tag_name_input").popover({
                title:'错误',
                content: data.msg,
                placement: 'top'
            })
        }
    });

}

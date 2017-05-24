$(document).ready(function() {
    var navbar = $("#navbar_right");
    navbar.empty();
    var user_key_cookie = document.cookie.indexOf("user-key");
    if(user_key_cookie == -1) {
        alert("会话过期，请重新登录");
        navbar.append("<li><a href=\"signup.html\">注册</a></li>");
        navbar.append("<li><a href=\"login.html\">登录</a></li>");
        window.location.href = '../pages/login.html';
    }else{
        $.ajax({
            type: "GET",
            url: api_server_url + "/api/async/v1/user/status",
            success: function(data) {
                if (data.status == 1){
                    alert('会话过期，请重新登录');
                    // $.cookie("user-key",null);
                    window.location.href = '../pages/login.html';
                }else{
                    var login_nav = "<li><a href=\"#\">"+$.cookie('unick')+"</a></li>";
                    navbar.append(login_nav);
                }
            },
            error: function(data) {
                alert('后台服务错误');
                // $.cookie("user-key",null);
                navbar.append("<li><a href=\"signup.html\">注册</a></li>");
                navbar.append("<li><a href=\"login.html\">登录</a></li>");
                window.location.href = '../pages/login.html';
            }
        });
    }
});
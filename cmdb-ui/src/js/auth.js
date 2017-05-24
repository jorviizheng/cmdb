        function signUp() {

            var user_name = $("input[name='userNameEn']").val();
            var user_name_cn = $("input[name='userNameCn']").val();
            var password = Base64.encode($("input[name='passWord']").val());
            var password_check = Base64.encode($("input[name='passWordCheck']").val());
            var email = $("input[name='email']").val();
            var mobile = $("input[name='mobile']").val();
            var date = datetime_human();

            var signJson = JSON.stringify({
                user_name: user_name,
                user_name_cn: user_name_cn,
                user_password: password,
                email: email,
                mobile: mobile,
                date: date
            });
            var apiUrl = "http://cmdb.wanda.cn/api/async/v1/users";

            if (password != password_check) {
                alert('两次密码不一致');
            } else {
                $.ajax({
                    type: "POST",
                    url: apiUrl,
                    data: signJson,
                    contentType: "application/json;charset=utf-8",
                    dataType: "json",
                    success: function(data, status) {
                        if (data.status == 0) {
                            alert(data.msg);
                            window.location.href = '../html/login.html';
                        } else if (data.status == 1) {
                            alert(data.msg);
                        }

                    },
                    error: function(data, status) {
                        alert(status);
                    }
                });
            }

        }

        //logout 
        function logout() {
            apiUrl = "http://cmdb.wanda.cn/api/auth/logout";
            $.ajax({
                type: "POST",
                url: apiUrl
            });
            $.cookie("user-key",null);
            window.location.href = "../html/login.html";
        }

        function login() {
            apiUrl = "http://cmdb.wanda.cn/api/async/v1/user/login";

            var userName = $("input[name='userName']").val();
            var password = Base64.encode($("input[name='passWord']").val());

            var loginJson = JSON.stringify({
                user_name: userName,
                user_password: password
            });
            $.ajax({
                type: "POST",
                url: apiUrl,
                data: loginJson,
                contentType: "application/json;charset=utf-8",
                dataType: "json",
                headers: {
                    'User-Name': userName
                },
                success: function(data, status) {
                    if (data.status == -1) {
                        alert("用户不存在,请注册");
                    } else if (data.status == 0) {
                        $.cookie("unick",userName, { expires: 1 });
                        window.location.href = "index.html";
                    } else if (data.status == 1) {
                        alert(data.msg);
                    }

                },
                error: function(data, status) {
                    alert(status);
                }
            });
        }
# CMDB
##  功能简介
1. 管理惠普服务器临时启动顺序，重启服务器，获取网卡信息等
2. 自动安装服务器系统，提供pxe模版选择，网段和IP地址选择(目前支持centos7和redhat7大版本)
3. 批量配置服务器系统，例如软件安装，用户管理，主机管理
4. 管理DHCP服务
5. 标签化管理服务器
6. 用户鉴权
---
## 相关技术
1. 前端采用bootstrap,通过ajax和后台交互，gulp编译模版
2. 后端使用Python3作为开发语言，tornado框架对外提供web服务
3. 使用postgresql作为数据库
4. 使用redis作为session存储媒介
5. 使用zookeeper作为服务注册中心

---
## 各服务说明

### cmdb-ui
1. cmdb 前端界面，采用bootstrap框架，利用ajax和后端进行交互，采用gulp编译，提供js的版本引用
2. 实现业务逻辑
3. 支持批量操作服务器
4. 可直接通过Nginx搭载,nginx配置文件只需要如下配置即可

**备注：**
    Nginx中server_name 必须和cmdb-ui/src/js/common.js中api_url一致


```
server {
        listen       80;
        server_name  your_domain_name;
        access_log off;
        error_log off;
        rewrite ^/$ /pages/index.html permanent;
 
        location / {
           root /Users/pippo/Project/python/cmdb/cmdb-ui/dist;
           index index.html;
        }

        location /api/async {
                proxy_pass      http://async_api;
                proxy_redirect           off;
                proxy_set_header         Host $host;
                proxy_set_header         X-Real-IP $remote_addr;
                proxy_set_header         X-Forwarded-For $proxy_add_x_forwarded_for;
                client_max_body_size     100m;
                proxy_connect_timeout  90;
                proxy_send_timeout      90;
                proxy_read_timeout      90;
                proxy_buffer_size       4k;
                proxy_buffers          4 32k;
                proxy_busy_buffers_size 64k;
                proxy_temp_file_write_size 64k;
        }
                location /api/sync {
                proxy_pass      http://sync_api;
                proxy_redirect           off;
                proxy_set_header         Host $host;
                proxy_set_header         X-Real-IP $remote_addr;
                proxy_set_header         X-Forwarded-For $proxy_add_x_forwarded_for;
                client_max_body_size     100m;
                proxy_connect_timeout  90;
                proxy_send_timeout      90;
                proxy_read_timeout      90;
                proxy_buffer_size       4k;
                proxy_buffers          4 32k;
                proxy_busy_buffers_size 64k;
                proxy_temp_file_write_size 64k;
        }
```


---
### cmdb-api
1. 用户鉴权
2. 数据库访问

---
### cmdb-sync-provider
1. 调用ansible同步获取服务器上各项信息

---
### cmdb-controller
1. 定时任务
2. 从数据库获取任务状态，根据状态执行对应任务
3. 自动装机任务下，定时检测系统安装是否完成，达到时间上限判定安装失败
4. 根据任务结果回写数据库任务状态和结果

---
### cmdb-ansible
1. 调用ansible api对服务器进行批量操作
2. 接收和返回json数据
3. 可供cmdb-sync-provider,cmdb-auto-provision,cmdb-controller 调用

---
### cmdb-auto-provision
1. 请求ILO4的rest api 获取服务器网卡信息，设置服务器临时启动顺序，重启服务器
2. 从数据库获取DHCP信息，通过ansible服务更新DHCP服务的而配置文件
3. 供cmdb-controller调用


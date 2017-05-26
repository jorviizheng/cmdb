# cmdb-sync-provider
## 功能
1. 供前端实时查询服务器上各项信息
2. 接收和返回json数据

## 接口
### firewalld_handler
1. 获取服务器上firewalld zones
2. 获取服务器上firewalld service

### hardware_handler
1. 获取服务器网卡Mac地址列表

### hostname_handler
1. 查询服务器主机名
2. 设置服务器主机名

### system_user_handler
1. 新增服务器用户
2. 删除服务器用户

### yum_handler
1. 从redis中获取可用的本地yum源
2. 获取服务器上已存在的yum源
3. 检查服务器上是否已安装对应的软件包

# cmdb-auto-provision
## 功能
1. 通过请求ILO4的REST接口控制服务器的启动顺序，重启服务器，获取信息
2. 通过请求ansible服务器更新dhcp服务器上的配置信息并且重启dhcp服务
## 接口
### hardware_handler
提供给cmdb-controller和cmdb-sync-provider查询服务器Mac地址信息
### provision_handler
1. 新装服务器
2. 重装服务器
3. 服务器安装结果检查

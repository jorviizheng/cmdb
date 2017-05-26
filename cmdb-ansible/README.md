# cmdb-ansible
## 功能及说明
1. 调用ansible api 批量配置服务器
2. 提供给cmdb-controller,cmdb-sync-provider调用
3. 添加 StrictHostKeyChecking no 到etc/ssh/ssh_config，用于避免首次连接警告 
4. 目前需要服务器密钥登录，即ansible服务所在服务器，该服务进程用户可以密钥登录需要管理的服务器

## 接口说明
### task_handler
1. 接收json数据，根据json结构中的key判断使用ansible对应模块

### 批量结果获取机制
重写ansible结果返回接口，每台服务器单独一个json结果集


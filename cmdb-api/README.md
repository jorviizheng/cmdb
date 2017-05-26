# cmdb-api
## 功能
1. 读写数据库
2. 用户鉴权

## 数据库说明
数据库：postgresql-9.6

### 数据库初始化
#### 新建角色
```
create role cmdb_admin with login password '9696EE717C4AAB96DC1C58E5342E87DF';#cmdb_admin123
```
#### 表空间

```
create tablespace cmdb owner cmdb_admin location '/var/lib/pgsql/9.6/data_cmdb';
```

#### 数据库

```
create database cmdb owner cmdb_admin  tablespace cmdb;
```

#### 已使用数据表
表名| 用途
---|---|---
server | 存储服务器信息 
dhcp_server | dhcp服务信息
dhcp_map|dhcp中服务器与ip地址映射关系
idc| 机房信息
kickstarts| kickstarts信息
pxe_template| pxe模版信息
tag|标签信息
tag_map|标签和资源映射信息
task|任务信息
task_status|任务状态信息
user|用户信息

#### 未使用数据表
表名| 用途
---|---|---
group | 分组信息
permission| 权限
resource|资源信息
service|服务信息
service_status|服务状态信息

### 接口说明
#### auth_handler

功能 | 是否实现
---|---
用户注册 | 是
用户登录 | 是
用户注销 | 是
用户登录状态判断|是
用户删除|否
用户修改|否

#### server_handler
功能 | 是否实现
---|---
服务器新增 | 是
服务器更新| 是
获取服务器列表|是
获取服务器信息|是
服务器删除 | 否

#### dhcp_handler
功能 | 是否实现
---|---
dhcp服务器列表获取 | 是
dhcp服务查询| 是
dhcp映射关系新增|是
dhcp映射关系更新|是
dhcp映射关系删除 | 是
获取pxe模版信息|是

#### kickstarts_handler
功能 | 是否实现
---|---
获取kickstarts信息 | 是

#### tag_handler
功能 | 是否实现
---|---
获取tag列表 | 是
新增tag| 是
删除tag|是
更新tag|是
根据tag搜索资源|是
新增tag映射 | 是
更新tan映射|是
删除tag映射|是


### 简易ORM
该工程中实现了简易的单表ORM，可进行增删改查
#### 实现原理
1. model和dal中每一个文件都是和数据库中表一一对应
2. 在执行读写前，先查询一次表结构而后通过与传入的json数据中key取交集获得需要操作的字段


## 用户鉴权
### session
1. session 存放在redis中
2. 1天失效时间


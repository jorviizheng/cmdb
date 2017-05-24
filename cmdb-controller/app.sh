#!/usr/bin/env bash
ports=(8082)
log_path="/home/cmdb/logs/task"
backup_num=10
size=256000000
current_path=$(cd `dirname $0`; pwd)

if [ ! -d $log_path ];then
    mkdir -p $log_path
fi


for port in ${ports[@]}
do
     #kill old process
    old_process=$(ps -ef|grep "port=$port"|grep -v grep|awk '{print$2}')
    if [ ! -z $old_process ];then
        kill -9 $old_process
    fi
    python3 ${current_path}/main.py -port=$port -log_file_prefix=$log_path/${port}.log -log_file_num_backups=$backup_num \
    -log_file_max_size=$size &
done

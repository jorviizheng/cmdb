#!/bin/bash
for dir in $(ls /home/cmdb);
do
   if [ -d $dir ];then
   	if [ $dir != "logs" ];then
		nohup /home/cmdb/$dir/app.sh 2>&1 >> /home/cmdb/logs/$dir.out &	
	fi
   fi
done

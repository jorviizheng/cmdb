FROM python:3-onbuild
COPY requirements.txt /usr/src/app/
RUN mkdir -p /logs

EXPOSE 8080

ENV port 8080
ENV log_path "/logs"
ENV backup_num 10
ENV size 256000000
ENTRYPOINT  python3 main.py -port=$port -log_file_prefix=$log_path/api.log -log_file_num_backups=$backup_num -log_file_max_size=$size 

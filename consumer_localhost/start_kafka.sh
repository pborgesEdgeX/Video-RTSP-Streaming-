nohup /kafka_2.12-2.3.0/bin/zookeeper-server-start.sh kafka_2.12-2.3.0/config/zookeeper.properties &
nohup /kafka_2.12-2.3.0/bin/kafka-server-start.sh kafka_2.12-2.3.0/config/server.properties &
service nginx start
uwsgi -s /tmp/uwsgi.sock --chmod-socket=666 --manage-script-name --mount /=app:consumer
/bin/bash
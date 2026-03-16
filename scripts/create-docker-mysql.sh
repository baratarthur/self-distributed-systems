docker run -d \
        --name mysql-dana \
        -p 30306:3306 \
        --cpus=0 \
        --memory=10g \
        -e MYSQL_DATABASE=danadb \
        -e MYSQL_USER=user_dana \
        -e MYSQL_PASSWORD=123456 \
        -e MYSQL_ROOT_PASSWORD=root_password_super_secreta \
        mysql:8.0 \
        --innodb_buffer_pool_size=10G \
        --innodb_log_file_size=256M \
        --innodb_flush_log_at_trx_commit=2 \
        --max_connections=1500 \
        --log_error_verbosity=3 \
        --general_log=1 \
        --general_log_file=/dev/stdout \
        --slow_query_log=1 \
        --slow_query_log_file=/dev/stdout \
        --long_query_time=1


sleep 10;
docker exec -i mysql-dana mysql -u user_dana -p123456 danadb -e "CREATE TABLE IF NOT EXISTS posts (id INT NOT NULL AUTO_INCREMENT, userId INT NOT NULL, likes INT DEFAULT 0, content TEXT, PRIMARY KEY (id));"
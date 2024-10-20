#!/bin/sh

source ./setup.sh

mysqld --user=$USERNAME --datadir=$MYSQL_HOME/data --log-error=$MYSQL_HOME/log/mysql.err --pid-file=$MYSQL_HOME/mysql.pid --socket=$MYSQL_HOME/socket --port=3306 $@ &

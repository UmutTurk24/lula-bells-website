#!/bin/sh

source ./setup.sh

mysqladmin --socket=$MYSQL_HOME/socket shutdown -u root -p

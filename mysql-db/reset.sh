#!/bin/sh

killall mysqld

rm -f socket socket.lock mysql.pid
rm -rf data
rm -rf log

mkdir data
mkdir log

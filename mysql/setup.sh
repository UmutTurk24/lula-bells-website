#!/bin/sh



SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Export the directory as MYHOME
export MYSQL_HOME="$SCRIPT_DIR"
export USERNAME=`whoami`


# Use the official MySQL image from Docker Hub
FROM mysql:8.0

# Create necessary directories and set up working directory
# RUN mkdir -p $MYSQL_HOME/db_data $MYSQL_HOME/log

# Copy initialization SQL file into the container (change_password.sql)
# COPY ./change_password.sql $MYSQL_HOME/

ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD} \
    MYSQL_DATABASE=${MYSQL_DATABASE}

# Expose MySQL port
EXPOSE 3306

# Default command to run MySQL server
CMD ["mysqld"]
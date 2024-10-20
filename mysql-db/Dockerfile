# Use the official MySQL image from Docker Hub
FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD} \
    MYSQL_DATABASE=${MYSQL_DATABASE}

# Expose MySQL port
EXPOSE 3306

# Default command to run MySQL server
CMD ["mysqld"]
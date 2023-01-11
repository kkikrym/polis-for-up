FROM redis
RUN mkdir /etc/redis && mkdir /var/log/redis
RUN apt-get update && apt-get install -y build-essential
COPY redis/redis.conf /etc/redis/redis.conf
RUN chmod 644 /etc/redis/redis.conf
EXPOSE 6379
CMD  ["/usr/local/bin/redis-server", "/etc/redis/redis.conf"]
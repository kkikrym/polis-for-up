FROM nginx:1.23.1
RUN apt-get update && apt-get install -y vim
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stdout /var/log/nginx/error.log

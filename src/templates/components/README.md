How to deploy / set up local environment

mkdir nginx
# create nginx conf file
vi polis.conf
# create .env file for django
vi src/.env
# migrate
sudo docker exec -it python bash
cd /src
make ini


# Regarding the ssl:
# Make sure that the configuration file is put under /etc/letsencrypt/
# Otherwise you have to change the docker-compose.yml file.
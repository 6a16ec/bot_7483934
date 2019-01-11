cp ./MariaDB.repo /etc/yum.repos.d/

yum -y install MariaDB-server

systemctl start mariadb
systemctl start mariadb

sh ./mysql_secure_installation.sh

# https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-on-centos-7
# https://mariadb.com/kb/en/library/yum/
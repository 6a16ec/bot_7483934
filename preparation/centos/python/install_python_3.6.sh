yum -y install epel-release
yum -y install python36

yum -y install https://centos7.iuscommunity.org/ius-release.rpm
yum -y install python36u-pip

pip3.6 install --upgrade pip

update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
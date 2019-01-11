// ???

yum -y install gcc openssl-devel bzip2-devel  libffi-devel

cd /usr/src
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
tar xzf Python-3.7.0.tgz

cd Python-3.7.0
./configure --enable-optimizations
make altinstall

rm -f /usr/src/Python-3.7.0.tgz
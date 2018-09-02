#!/bin/bash
echo $PATH
export PATH="$PATH:/usr/local/bin"
yum update -y
yum install uwsgi curl python36 python36-devel gcc nginx -y

# install python3 pip3 pytho3-dev and virtualenv
# https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04
# http://flask.pocoo.org/docs/1.0/deploying/wsgi-standalone/#proxy-setups

# curl -o bootstrap-salt.sh -L https://bootstrap.saltstack.com
# sh bootstrap-salt.sh git

test -e /usr/local/bin/pip3.6 || curl https://bootstrap.pypa.io/get-pip.py | python3.6
pip3.6 install virtualenv
test -d /opt/onica-hello-world || mkdir -p /opt/onica-hello-world
cd /opt/onica-hello-world
virtualenv onica-hello-world
source onica-hello-world/bin/activate
pip install uwsgi flask
rsync -avp /vagrant/root/ /


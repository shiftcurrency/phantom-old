FROM ubuntu:14.04

MAINTAINER Felix Imobersteg <felix@whatwedo.ch>

#Base settings
ENV DEBIAN_FRONTEND noninteractive
ENV HOME /root

#Install Phantom
RUN \
    apt-get update -y; \
    apt-get -y install msgpack-python python-gevent python-pip python-dev; \
    pip install msgpack-python --upgrade; \
    apt-get clean -y; \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

#Add Phantom source
ADD . /root
VOLUME /root/data

#Set upstart command
CMD cd /root && python phantom.py --ui_ip 0.0.0.0

#Expose ports
EXPOSE 43110
EXPOSE 15441

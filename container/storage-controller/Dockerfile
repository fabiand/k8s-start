FROM fedora:23
MAINTAINER "Tolik Litovsky" <tlitovsk@redhat.com>
ENV container docker

RUN dnf -y install wget qemu-img python3 python3-pip kubernetes-client
RUN dnf -y update && dnf clean all;

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install bottle jinja2

EXPOSE 8084

RUN mkdir /root/manager
COPY manager /root/manager
CMD python3 /root/manager
# docker build --rm -t tlitovsk/storage-controller:latest
FROM fedora:23
MAINTAINER "Tolik Litovsky" <tlitovsk@redhat.com>
ENV container docker

RUN dnf -y install wget qemu-img python3 python3-pip
RUN dnf -y update && dnf clean all;

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install bottle

RUN mkdir -p /mnt

RUN mkdir -p /root/worker
COPY worker /root/worker

EXPOSE 8084

CMD python3 /root/worker
# docker build --rm -t tlitovsk/storage-worker:latest .
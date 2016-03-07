FROM fedora:23
MAINTAINER "Fabian Deutsch" <fabiand@redhat.com>
ENV container docker

RUN dnf install -y libvirt-client kubernetes-client

ADD controller /
ADD start-controller.sh /

CMD ["/start-controller.sh"]

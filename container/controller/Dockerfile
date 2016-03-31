FROM fedora:23
MAINTAINER "Fabian Deutsch" <fabiand@redhat.com>
ENV container docker

RUN dnf install -y libvirt-client kubernetes-client python3-bottle python3-jsonpath-rw python3-jsonpath-rw-ext

COPY controller /controller
ADD start-controller.sh /

CMD ["/start-controller.sh"]

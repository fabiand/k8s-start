FROM fabiand/libvirtd:latest

MAINTAINER "Fabian Deutsch" <fabiand@redhat.com>
ENV container docker

RUN dnf install -y python3-requests python3
RUN dnf install -y libxml2

ADD start.sh /

EXPOSE 16509

CMD ["/start.sh"]

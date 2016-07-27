FROM fedora:23
MAINTAINER "Tolik Litovsky" <tlitovsk@redhat.com>
ENV container docker

RUN yum -y install nfs-utils systemd wget
RUN yum -y update; yum clean all;

RUN echo "/srv/nfs *(rw,no_root_squash)" >> /etc/exports; \
	mkdir -p /srv/nfs ; \
	systemctl enable rpcbind nfs-server

EXPOSE 111/UDP 2049/TCP


CMD ["/usr/sbin/init"]


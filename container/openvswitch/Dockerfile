FROM fedora:23

MAINTAINER "Fabian Deutsch" <fabiand@redhat.com>
ENV container docker

RUN dnf install -y openvswitch

RUN systemctl enable openvswitch.service

ADD start-ovs.sh /

LABEL start="--volume /var/run/openvswitch:/var/run/openvswitch"

CMD ["/start-ovs.sh"]

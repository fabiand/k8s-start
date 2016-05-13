FROM fedora:23

MAINTAINER "Fabian Deutsch" <fabiand@redhat.com>
ENV container docker

RUN dnf install -y python3-requests python3
# Just for client bits
RUN dnf install -y openvswitch

ADD start-network.sh /

LABEL start="--volumes /run/openvswitch:/run/openvswitch"

CMD ["/start-network.sh"]

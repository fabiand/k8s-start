FROM fabiand/libvirtd:latest

MAINTAINER "Fabian Deutsch" <fabiand@redhat.com>
ENV container docker

RUN dnf install -y python3-requests python3
RUN dnf install -y libxml2

# Adding openvswitch to give libvirt the ability to use OVS networks
RUN dnf install -y openvswitch

ADD start-compute.sh /

EXPOSE 16509
EXPOSE 5900
EXPOSE 1923

CMD ["/start-compute.sh"]

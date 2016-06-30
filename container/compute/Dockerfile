FROM fedora:23

MAINTAINER "Fabian Deutsch" <fabiand@redhat.com>
MAINTAINER "Tolik Litovsky" <tlitovsk@redhat.com>
ENV container docker

RUN dnf install -y libvirt-daemon-kvm libvirt-daemon-qemu libvirt-client augeas python3-requests python3 python3-jinja2 python3-bottle libvirt-python3
# Adding openvswitch to give libvirt the ability to use OVS networks
RUN dnf install -y openvswitch

RUN \
echo 'listen_tls = 0'>> /etc/libvirt/libvirtd.conf; \
echo 'listen_tcp = 1'>> /etc/libvirt/libvirtd.conf; \
echo 'auth_tcp = "none"'>> /etc/libvirt/libvirtd.conf; \
echo 'spice_listen = "0.0.0.0"' >> /etc/libvirt/qemu.conf; \
echo 'vnc_listen = "0.0.0.0"'>> /etc/libvirt/qemu.conf; \
echo 'vnc_tls = 0'>> /etc/libvirt/qemu.conf; \
echo 'vnc_sasl = 0'>> /etc/libvirt/qemu.conf; \
echo 'user = "root"'>> /etc/libvirt/qemu.conf; \
echo 'group = "root"'>> /etc/libvirt/qemu.conf; \
echo 'dynamic_ownership = 1'>> /etc/libvirt/qemu.conf;

COPY compute /compute
ADD start-compute.sh /

EXPOSE 16509
EXPOSE 5900
EXPOSE 1923

CMD /start-compute.sh

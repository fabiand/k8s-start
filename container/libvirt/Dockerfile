FROM fedora:23

MAINTAINER "Fabian Deutsch" <fabiand@redhat.com>
ENV container docker

RUN dnf install -y \
  libvirt-daemon-kvm \
  libvirt-daemon-qemu \
  libvirt-daemon-driver-interface \
  libvirt-daemon-driver-network \
  libvirt-daemon-driver-nodedev \
  libvirt-client \
  augeas

RUN augtool set /files/etc/libvirt/libvirtd.conf/listen_tls 0
RUN augtool set /files/etc/libvirt/libvirtd.conf/listen_tcp 1
RUN augtool set /files/etc/libvirt/libvirtd.conf/auth_tcp none

RUN augtool set /files/etc/libvirt/qemu.conf/spice_listen 0.0.0.0
RUN augtool set /files/etc/libvirt/qemu.conf/vnc_listen 0.0.0.0
RUN augtool set /files/etc/libvirt/qemu.conf/vnc_tls 0
RUN augtool set /files/etc/libvirt/qemu.conf/vnc_sasl 0

RUN augtool set /files/etc/libvirt/qemu.conf/user root
RUN augtool set /files/etc/libvirt/qemu.conf/group root
RUN augtool set /files/etc/libvirt/qemu.conf/dynamic_ownership 1

#EXPOSE 16509

CMD ["/usr/sbin/libvirtd"]

#!/usr/bin/bash

set -xe

libvirtd --listen &

symlink_default_nic_to_well_known_name() {
  local DEFAULT_NIC=$(ip route show to 0/0 | cut -d" " -f 5)
  ip link show meth0 || ip link add name meth0 link $DEFAULT_NIC type macvlan
  ip link set meth0 up
  # macvatp does not work in container
}

sleep 3

curl -L -o dom.xml "$DOMAIN_HTTP_URL"

virsh define dom.xml

wait

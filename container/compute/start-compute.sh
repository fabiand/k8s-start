#!/usr/bin/bash

set -xe
libvirtd --listen &

# symlink_default_nic_to_well_known_name_and_create_bridge
DEFAULT_NIC=$(ip route show to 0/0 | cut -d" " -f 5)
BR=bridge0

#{
  ip link set $DEFAULT_NIC up
  ip link show meth0 || ip link add name meth0 link $DEFAULT_NIC type macvlan
  ip link set meth0 up || :
  ip link show $BR || ip link add $BR type bridge
  ip link set meth0 master $BR || :
  ip link set $BR up || :
#}
sleep 3

# IIRC macvlans don't work in containers, but let's try without failing
virsh attach-interface $DOMNAME bridge $BR --model e1000 --current || :

python3 compute


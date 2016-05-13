#!/usr/bin/bash

set -xe

cat <<EOP
python3 -B -

# FIXME Just a brain dump

"""
for action, net in etcd.watch("/networks"):
    if add:
        create_in_ovs_and_libv
    if delete:
        delete_in_libv_and_ovs
"""
EOP

sleep 123456

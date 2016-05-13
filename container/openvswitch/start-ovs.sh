#!/usr/bin/bash

set -xe

touch /var/log/openvswitch/ovsdb-server.log
touch /var/log/openvswitch/ovs-vswitchd.log

tail -f /var/log/openvswitch/*.log

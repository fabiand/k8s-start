#!/usr/bin/bash

set -xe

libvirtd --listen &

symlink_default_nic_to_well_known_name() {
  local DEFAULT_NIC=$(ip route show to 0/0 | cut -d" " -f 5)
  ip link show meth0 || ip link add name meth0 link $DEFAULT_NIC type macvlan
  ip link set meth0 up
  # macvatp does not work in container
}

# Give libvirt time to come up
sleep 3

# A small python script to
# first assume etcd and try to parse the value
# if this fails, then it returns the raw value
# this is helfpul for raw http urls like a http server
python3 -B - <<EOP
import requests
import json

dstfn = "dom.xml"
url = "$DOMAIN_HTTP_URL"

print("Fetching URL %s" % url)
value = requests.get(url).text

try:
    print("Assuming etcd source, trying to parse ...")
    value = json.loads(requests.get(url).text)["node"]["value"]
    print("json looks okay")
except:
    print("Failed to parse json, returning raw data")

print("Writing to %s" % dstfn)
with open(dstfn, "w") as dst:
    dst.write(value)
EOP

virsh define dom.xml

wait

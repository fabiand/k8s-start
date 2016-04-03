#!/usr/bin/bash

set -xe

libvirtd --listen &

DEFAULT_NIC=$(ip route show to 0/0 | cut -d" " -f 5)
symlink_default_nic_to_well_known_name() {
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

# Create the domain
virsh define dom.xml

# IIRC macvlans don't work in containers, but let's try without failing
virsh attach-interface generic direct $DEFAULT_NIC --model e1000 --current || :

# Start the domain
virsh start $(xmllint --xpath "domain/name/text()" dom.xml)

wait

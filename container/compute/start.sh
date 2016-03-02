#!/usr/bin/bash

set -xe

libvirtd --listen &

sleep 3

if [[ -n "$LIBVIRT_DOMAIN_URL" ]]; then
  curl -L -o dom.xml "$LIBVIRT_DOMAIN_URL"
  virsh define dom.xml
fi

wait

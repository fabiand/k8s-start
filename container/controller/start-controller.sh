#!/usr/bin/bash

set -x

export PYTHONPATH=.
export DOM_STORE_GIT_PATH=/var/tmp/ovirt-controller/store/
export LIBVIRT_DOMAIN_URL_BASE=http://git.engineering.redhat.com/git/users/fdeutsch/domxmls.git/plain/
export KUBECTL="$PWD/remote-kubectl"

# FIXME /var/tmp/ovirt-controller/store needs to be initialized

python3 -m controller


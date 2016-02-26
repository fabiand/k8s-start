#!/usr/bin/bash

set -ex

git clone http://gerrit.ovirt.org/ovirt-node-ng.git

cd ovirt-node-ng

curl -O -L http://mirror.centos.org/centos/7/os/x86_64/images/boot.iso

sed -i -e "/CURLOPTS/ d" automation/build-artifacts.sh

libvirtd --listen &

LMC="livemedia-creator --ram 2048 --vcpus 4"
[[ -n "$http_proxy" ]] && LMC="$LMC --proxy $http_proxy"
export LMC
bash -ex automation/build-artifacts.sh || { tail -n40 *.log ; exit 1 ; }

mv -v exported-artifacts /pwd/

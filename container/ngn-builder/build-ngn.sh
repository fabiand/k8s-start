#!/usr/bin/bash

set -ex

git clone http://gerrit.ovirt.org/ovirt-node-ng.git

cd ovirt-node-ng

curl -O -L http://mirror.centos.org/centos/7/os/x86_64/images/boot.iso

sed -i -e "/CURLOPTS/ d" automation/build-artifacts.sh

libvirtd &

bash -ex automation/build-artifacts.sh || { tail -n40 *.log ; exit 1 ; }

make check

find

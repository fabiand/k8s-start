#!/usr/bin/bash

set -ex

git clone http://gerrit.ovirt.org/ovirt-node-ng.git

cd ovirt-node-ng

ln /boot.iso boot.iso
touch boot.iso

sed -i -e "/CURLOPTS/ d" automation/build-artifacts.sh

libvirtd &

bash -ex automation/build-artifacts.sh || { tail -n40 *.log ; exit 1 ; }

find

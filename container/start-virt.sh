#!/usr/bin/bash

set -ex

ping -c1 heise.de

#qemu-img create -f qcow2 dst.img 20G
#qemu-system-x86_64 \
#  -enable-kvm \
#  -m 512 \
#  -cdrom http://jenkins.ovirt.org/job/fabiand_boo_build_testing/lastSuccessfulBuild/artifact/ovirt-ipxe.iso \
#  -hda dst.img \
#  -serial stdio \
#  -vnc :0



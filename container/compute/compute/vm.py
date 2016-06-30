#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim: sw=4 et sts=4
#
# fuzz
#
# Copyright (C) 2016  Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): Fabian Deutsch <fabiand@redhat.com>


import os
import libvirt
import sys


from jinja2 import Environment
from jinja2 import FileSystemLoader

abspath = os.path.abspath(__file__)
file_dir = os.path.dirname(abspath)
print(file_dir)
jinja_env = Environment(
    loader=FileSystemLoader('{}/templates'.format(file_dir)))


def render_dom(vm_params):
    template = jinja_env.get_template('vm.xml.in')

    machine_xml = template.render(
        name=vm_params['name'],
        disks=vm_params['disks'],
        cpus=vm_params['cpus'],
        mem_size_kb=vm_params['memory_size_kb'])

    return machine_xml


class LibvirtVm():

    def __init__(self, vm_desc):
        self._conn = libvirt.open(None)

        if self._conn is None:
            print('Failed to open connection to the hypervisor')
            return
        try:
            ids = self._conn.listDomainsID()
            if vm_desc is None:
                assert len(ids) == 1
                self._domain = self._conn.lookupByID(ids.pop())
            else:
                assert len(ids) == 0
                self._domain = self._conn.createXML(vm_desc)
        except:
            print("Unexpected error:", sys.exc_info()[0])

    def state(self):
        state = 'failed'
        if self._domain is not None:
            state = self._domain.state()
            if state[0] is 1:
                state = 'running'
            else:
                state = 'undefined'
        return state

    def stop(self):
        if self._domain is not None:
            self._domain.destroy()
            #TODO : thread safety
            self._domain = None
            return True
        return False

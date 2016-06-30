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
#

import json

from .runtime import KubeDomainRuntime
from .store import EtcdDomainStore


class Domains():
    def __init__(self, store_klass=EtcdDomainStore,
                 runtime_klass=KubeDomainRuntime):
        self.store = store_klass()
        self.runtime = runtime_klass()

    def list_available(self):
        return self.store.list()

    def list_running(self):
        return self.runtime.list()

    def create(self, domname, dom_spec):
        dom_spec = json.loads(dom_spec)
        assert domname == dom_spec.get("name")
        self.store.add(domname, json.dumps(dom_spec))
        self.runtime.create(domname, dom_spec.get("mounts"))

    def delete(self, domname):
        self.store.remove(domname)
        self.runtime.delete(domname)

    def show(self, domname):
        return self.store.get(domname)

    def connection_uri(self, domname):
        return str(self.runtime.connection_uri(domname))

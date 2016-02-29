#!/usr/bin/python
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

import subprocess
import json
import jsonpath_rw
import xml.etree.ElementTree as ET
import os
import tempfile


def jsonpath(expr, objs):
    return jsonpath_rw.parse(expr).find(objs)


def kubectl(args, expr=None):
    argv = ["kubectl", "-o", "json"] + args
    print(argv)
    return None
    data = subprocess.check_output(argv)
    objs = json.loads(data)
    if expr:
        return jsonpath(expr, objs)
    return objs


class GitDomainStore():
    """Store some data in a git repository
    FIXME git part needs impl.

    >>> store = GitDomainStore()
    >>> store.add("foo", "FOO")
    >>> store.list()
    ['foo']
    """
    GIT_PATH = "/var/tmp/ovirt-controller/store"

    def __init__(self):
        try:
            os.makedirs(self.GIT_PATH)
        except:
            pass

    def list(self):
        return os.listdir(self.GIT_PATH)

    def add(self, domname, data):
        assert domname not in self.list()
        with open(self.GIT_PATH + "/" + domname, "w") as dst:
            dst.write(data)

    def remove(self, domname):
        assert domname in self.list()
        os.unlink(self.GIT_PATH + "/" + domname)

    def get(self, domname):
        with open(self.GIT_PATH + "/" + domname, "r") as src:
            return src.read()


class KubeDomainRuntime():
    VM_RC_SPEC = """
apiVersion: v1
kind: ReplicationController
metadata:
  name: ovirt-compute-rc-{domname}
  labels:
    app: ovirt-compute-rc
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: ovirt-compute
        domain: {domname}
    spec:
      containers:
      - name: controller
        image: docker.io/fabiand/compute:latest
        ports:
        - containerPort: 8080
    """

    rc_selector = ["-l", "app=ovirt-compute-rc"]

    def _k(self, args, expr=None):
        return kubectl(args, expr)

    def list(self):
        matches = kubectl(self.rc_selector + ["get", "rc"],
                          "items[*].metadata.labels.domain")
        return [m.value for m in matches] if matches else []

    def create(self, domname):
        with tempfile.NamedTemporaryFile(mode="wt") as tmp:
            spec = self.VM_RC_SPEC.format(domname=domname)
            print(spec)
            tmp.write(spec)
            tmp.flush()
            self._k(["create", "-f", tmp.name])

    def delete(self, domname):
        self._k(["delete", "rc",
                 "-l", "domain=%s" % domname])


class Domains():
    def __init__(self, store_klass=GitDomainStore,
                 runtime_klass=KubeDomainRuntime):
        self.store = store_klass()
        self.runtime = runtime_klass()

    def list_available(self):
        return self.store.list()

    def list_running(self):
        return self.runtime.list()

    def create(self, domname, domxml):
        assert domname == ET.fromstring(domxml).find("name").text
        self.store.add(domname, domxml)
        self.runtime.create(domname)

    def delete(self, domname):
        self.store.remove(domname)
        self.runtime.delete(domname)

    def show(self, domname):
        return self.store.get(domname)


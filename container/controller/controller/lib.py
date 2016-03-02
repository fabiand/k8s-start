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


def jsonpath(expr, objs):
    return jsonpath_rw.parse(expr).find(objs)


def kubectl(args, expr=None, **kwargs):
    app = os.environ.get("KUBECTL", "kubectl")
    argv = [app] + args
    print(argv)
    data = subprocess.check_output(argv, **kwargs)
    data = data.decode("utf-8")
    print(data)
    if expr:
        objs = json.loads(data)
        return jsonpath(expr, objs)
    return data


class Git():
    """Assumes that origin and master are setup correctly
    """
    path = None

    def __init__(self, path):
        self.path = path
        assert self.path

    def _git(self, args):
        argv = ["git", "-C", self.path] + args
        print(argv)
        return subprocess.check_output(argv)

    def pull(self):
        self._git(["pull"])

    def push(self):
        self._git(["push"])

    def rm(self, fn, force=False):
        self._git(["rm", fn]
                  + (["-f"] if force else []))

    def add(self, fn):
        self._git(["add", fn])

    def commit(self, commitmsg="Auto commit"):
        self._git(["commit", "-s", "-m", commitmsg])


class GitDomainStore():
    """Store some data in a git repository
    FIXME git part needs impl.

    >>> store = GitDomainStore()
    >>> store.add("foo", "FOO")
    >>> store.list()
    ['foo']
    """
    git = None

    def __init__(self, path=os.environ.get("DOM_STORE_GIT_PATH")):
        assert path
        assert os.path.isdir(path)
        assert os.path.isdir(path + "/.git")
        self.git = Git(path)

    def list(self):
        return [fn for fn in os.listdir(self.git.path)
                if not fn.startswith(".") and not fn.startswith("/")]

    def add(self, domname, data):
        assert domname not in self.list()
        self.git.pull()
        fn = self.git.path + "/" + domname
        with open(fn, "w") as dst:
            dst.write(data)
        self.git.add(domname)
        self.git.commit("Added %s" % domname)
        self.git.push()

    def remove(self, domname):
        assert domname in self.list()
        self.git.pull()
        self.git.rm(domname)
        self.git.commit("Removed %s" % domname)
        self.git.push()

    def get(self, domname):
        self.git.pull()
        with open(self.git.path + "/" + domname, "r") as src:
            return src.read()


class KubeDomainRuntime():
    VM_RC_SPEC = """
apiVersion: v1
kind: ReplicationController
metadata:
  name: ovirt-compute-rc-{{domname}}
  labels:
    app: ovirt-compute-rc
    domain: {{domname}}
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: ovirt-compute
        domain: {{domname}}
    spec:
      containers:
      - name: controller
        image: docker.io/fabiand/compute:latest
        securityContext:
          privileged: true
        ports:
        - containerPort: 1923
          name: spice
        - containerPort: 5900
          name: vnc
        - containerPort: 16509
          name: libvirt
        env:
        - name: LIBVIRT_DOMAIN
          value: {{domname}}
        - name: LIBVIRT_DOMAIN_URL
          value: {LIBVIRT_DOMAIN_URL_BASE}/{{domname}}
    """.format(LIBVIRT_DOMAIN_URL_BASE=os.environ["LIBVIRT_DOMAIN_URL_BASE"])

    VM_SVC_SPEC = """
apiVersion: v1
kind: Service
metadata:
  name: libvirt-{{domname}}
  labels:
    app: ovirt-compute-service
    domain: {{domname}}
spec:
  selector:
    app: ovirt-compute
    domain: {{domname}}
  ports:
  - name: libvirt
    port: 16509
  - name: vnc
    port: 5900
    """.format()

    def list(self):
        matches = kubectl(["-l", "app=ovirt-compute-rc",
                          "get", "rc", "-ojson"],
                          "items[*].metadata.labels.domain")
        return [m.value for m in matches] if matches else []

    def create(self, domname):
        def create(spec):
            spec = spec.format(domname=domname)
            print(spec)
            kubectl(["create", "-f", "-"], input=bytes(spec, encoding="utf8"))

        create(self.VM_RC_SPEC)
        create(self.VM_SVC_SPEC)

    def delete(self, domname):
        kubectl(["delete", "rc",
                 "-l", "domain=%s" % domname])

        kubectl(["delete", "svc",
                 "-l", "domain=%s" % domname])

    def describe(self, domname):
        matches = kubectl(["get", "service", "-ojson",
                           "-l", "domain=%s" % domname])
        return matches


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

    def status(self, domname):
        return str(self.runtime.describe(domname))


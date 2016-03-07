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

import subprocess
import os
import json
from pprint import pprint
from .utils import jsonpath


def curl(args, expr=None, **kwargs):
    app = os.environ.get("CURL", "curl")
    argv = [app] + args
    print("curling", argv)
    data = subprocess.check_output(argv, **kwargs)
    data = data.decode("utf-8")
    print("curling got", data)
    if expr:
        objs = json.loads(data)
        return jsonpath(expr, objs)
    return data


class Etcd():
    _url = None

    def __init__(self, url="http://127.0.0.1:4001/v2/keys/"):
        self._url = url

    def _curl(self, path, method="GET", data=None):
        assert method in ["GET", "PUT", "DELETE"]
        url = self._url + path
        cmd = ["-L", "-X", method]
        cmd += [url]
        if method == "PUT" or data:
            assert method == "PUT" and not data is None
            cmd += ["--data-urlencode", "value@-"]
            print("Data", data)
            return curl(cmd, input=bytes(data, encoding="utf8"))
        return curl(cmd)

    def list(self, key=""):
        data = self._curl(key)
        parsed = jsonpath("node.nodes[*].key", json.loads(data))
        return [m.value for m in parsed]

    def get(self, key):
        parsed = self._curl(key)
        ms = jsonpath("node.value", json.loads(parsed))
        return ms[0].value

    def set(self, key, value):
        return self._curl(key, "PUT", data=value)

    def delete(self, key):
        return self._curl(key, "DELETE")


class EtcdDomainStore():
    etcd = None

    def __init__(self, url="http://127.0.0.1:4001/v2/keys/",
                 key_prefix="domains/"):
        self.etcd = Etcd(url + key_prefix)

    def list(self):
        return self.etcd.list()

    def add(self, domname, data):
        return self.etcd.set(domname, data)

    def remove(self, domname):
        return self.etcd.delete(domname)

    def get(self, domname):
        return self.etcd.get(domname)


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
